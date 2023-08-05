"""
View and analyze time series recordings similar to pCLAMP.


TODO:
- option to not fit overlay traces
- export trace to new window
- trace x/y table
- curve fit option to specify xfit as linspace or logspace
- trace mask
- selection list boxes not always growing vertically to fit content?
- option to show all episodes/traces in background
    - can click to select background trace?
- persistent baseline style?
- filtering?
- wrap trace (e.g., for single channel analysis?), or maybe this is best left to its own special UI?
- fix ylabel overlapping ytick labels due to fixed left axis width
    - if left axes can autosize again will have to left-align axes after each zoom/pan
- test curve fit bounds
- curve fit fixed parameters
- curve fit constraint expressions
- baseline nodes (allow manual adjustment of baseline)
- select a single trace (while displaying multiple)???
- reorder channels???
- reorder trace names???
- aquisition???
"""


__author__ = "Marcel P. Goldschen-Ohm"
__author_email__ = "goldschen-ohm@utexas.edu, marcel.goldschen@gmail.com"


import sys, os, re, ast, copy, json
import numpy as np
import scipy as sp
import lmfit  # for curve fitting
import PyQt6  # for the UI
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import pyqtgraph as pg  # for plots: https://www.pyqtgraph.org
import qtawesome as qta  # for some nice icons: https://github.com/spyder-ide/qtawesome
from .DataModel import *  # !!! defines the data model for pyCLAMP

try:
    # OPTIONAL: For importing HEKA data files.
    # https://github.com/campagnola/heka_reader
    # e.g., Just put heka_reader.py in the same directory as this file.
    from . import heka_reader
except ImportError:
    heka_reader = None


pg.setConfigOption('background', (200, 200, 200))  # Default background for plots.
pg.setConfigOption('foreground', (0, 0, 0))   # Default foreground color for text, lines, axes, etc.


class pyCLAMP(QWidget):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.data = DataModel()

        self.initUI()
        self.updateUI()
        self.setWindowTitle('pyCLAMP')
    
    def dump(self, filepath=None):
        """ For debugging. Dumps a representation of the data to a text file or stdout. """
        if filepath is None:
            filepath, _ = QFileDialog.getSaveFileName(self, "Dump Data", "", "(*.txt)")
        if not filepath:
            return
        self.data.dump(filepath, indent=2)
    
    def open(self, filepath=None):
        if filepath is None:
            filepath, _ = QFileDialog.getOpenFileName(self, "Open Data", "", "MATLAB Data Files (*.mat)")
        if not filepath or not os.path.isfile(filepath):
            return
        self.data.loadmat(filepath)
        self.updateUI()
        path, filename = os.path.split(filepath)
        self.setWindowTitle(filename)
    
    def save(self, filepath=None):
        if filepath is None:
            filepath, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "MATLAB Data Files (*.mat)")
        if not filepath:
            return
        self.data.savemat(filepath)
        path, filename = os.path.split(filepath)
        self.setWindowTitle(filename)
    
    def importHEKA(self, filepath=None):
        """
        Import HEKA data file.

        HEKA format:
        ------------
        Group (Experiment)
            Series (Recording)
                Sweep (Episode)
                    Trace (Data Series for Channel A)
                    Trace (Data Series for Channel B)
        """
        if heka_reader is None:
            return
        if filepath is None:
            filepath, _ = QFileDialog.getOpenFileName(self, "Open HEKA File", "", "HEKA Data Files (*.dat)")
        if not filepath or not os.path.isfile(filepath):
            return
        bundle = heka_reader.Bundle(filepath)
        numHekaGroups = len(bundle.pul)
        if numHekaGroups == 0:
            return
        elif numHekaGroups == 1:
            hekaGroupIndex = 0
        elif numHekaGroups > 1:
            # choose a group (experiment) to load
            hekaGroupNames = [bundle.pul[i].Label for i in range(numHekaGroups)]
            hekaGroupNamesListWidget = QListWidget()
            hekaGroupNamesListWidget.addItems(hekaGroupNames)
            hekaGroupNamesListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
            hekaGroupNamesListWidget.setSelected(hekaGroupNamesListWidget.item(0), True)
            dlg = QDialog()
            dlg.setWindowTitle("Choose Recording")
            buttonBox = QDialogButtonBox()
            buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
            buttonBox.accepted.connect(dlg.accept)
            buttonBox.rejected.connect(dlg.reject)
            dlg.setWindowModality(Qt.ApplicationModal)
            if dlg.exec_():
                hekaGroupIndex = hekaGroupNamesListWidget.selectedIndexes()[0].row()
            else:
                return
        DATA = {
            'Type': 'Data',
            'Episodes': [],
            'Notes': ''
        }
        numHekaSeries = len(bundle.pul[hekaGroupIndex])
        for hekaSeriesIndex in range(numHekaSeries):
            numHekaSweeps = len(bundle.pul[hekaGroupIndex][hekaSeriesIndex])
            for hekaSweepIndex in range(numHekaSweeps):
                episode = hekaSweepIndex
                numHekaTraces = len(bundle.pul[hekaGroupIndex][hekaSeriesIndex][hekaSweepIndex])
                for hekaTraceIndex in range(numHekaTraces):
                    channel = hekaTraceIndex
                    trace = bundle.pul[hekaGroupIndex][hekaSeriesIndex][hekaSweepIndex][hekaTraceIndex]
                    TRACE = {
                        'XData': trace.XInterval,
                        'YData': bundle.data[(hekaGroupIndex, hekaSeriesIndex, hekaSweepIndex, hekaTraceIndex)] + trace.YOffset,
                        'XLabel': 'Time',
                        'YLabel': trace.Label,
                        'XUnit': trace.XUnit,
                        'YUnit': trace.YUnit
                    }
                    if trace.XStart != 0:
                        TRACE['XZero'] = trace.XStart
                    if 'Episodes' not in DATA:
                        DATA['Episodes'] = []
                    while len(DATA['Episodes']) <= episode:
                        DATA['Episodes'].append({
                            'Type': 'Episode',
                            'Channels': []
                        })
                    EPISODE = DATA['Episodes'][episode]
                    if 'Channels' not in EPISODE:
                        EPISODE['Channels'] = []
                    while len(EPISODE['Channels']) <= channel:
                        EPISODE['Channels'].append({
                            'Type': 'Channel',
                            'Traces': [],
                            'Events': []
                        })
                    CHANNEL = EPISODE['Channels'][channel]
                    if 'Traces' not in CHANNEL:
                        CHANNEL['Traces'] = []
                    CHANNEL['Traces'].append(TRACE)
        self.data.setData(DATA)
        self.updateUI()
        path, filename = os.path.split(filepath)
        self.setWindowTitle(filename)
    
    def initUI(self):
        self.initMainMenu()
        self.initToolbar()
        
        # channel plots layout
        self._channelPlotsLayout = QVBoxLayout()
        self._channelPlotsLayout.setContentsMargins(0, 0, 0, 0)
        self._channelPlotsLayout.setSpacing(0)

        # main layout
        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(3, 3, 3, 3)
        self._mainLayout.setSpacing(0)
        self._mainLayout.addWidget(self._toolbar)
        self._mainLayout.addLayout(self._channelPlotsLayout)
    
    def initMainMenu(self):
        self._fileMenu = QMenu('&File')
        self._fileMenu.addAction('&Open', self.open)
        self._fileMenu.addSection(' ')
        self._fileMenu.addAction('Import HEKA', self.importHEKA)
        self._fileMenu.addSection(' ')
        self._fileMenu.addAction('&Save', self.save)

        self._debugMenu = QMenu('Debug')
        self._debugMenu.addAction('Dump', self.dump)

        self._mainMenu = QMenu()
        self._mainMenu.addMenu(self._fileMenu)
        self._mainMenu.addSection(' ')
        self._mainMenu.addMenu(self._debugMenu)

        # self._mainMenu.addSection(' ')
        # self._mainMenu.addAction(qta.icon('fa.table'), 'Data Table')
        # self._mainMenu.addSection(' ')
        # self._mainMenu.addAction(qta.icon('fa.terminal'), 'Python Console')
    
    def initToolbar(self):
        # main menu button
        self._mainMenuButton = QToolButton()
        self._mainMenuButton.setIcon(qta.icon('mdi6.menu'))
        self._mainMenuButton.setToolTip('Main Menu')
        self._mainMenuButton.setPopupMode(QToolButton.InstantPopup)
        self._mainMenuButton.setMenu(self._mainMenu)
        
        # episode selection
        self._episodeSelectionBox = MultiIndexSpinBox()
        self._episodeSelectionBox.setToolTip('Selected Episode(s)')
        self._episodeSelectionBox.valuesChanged.connect(self.updateChannelPlots)

        # channel selection
        self._channelSelectionList = ListWidget()
        self._channelSelectionList.setSelectionMode(QAbstractItemView.MultiSelection)
        self._channelSelectionList.itemSelectionChanged.connect(self.onChannelSelectionChanged)
        self._channelSelectionList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        
        # trace selection
        self._traceSelectionBox = MultiIndexSpinBox()
        self._traceSelectionBox.setToolTip('Selected Trace(s)')
        self._traceSelectionBox.valuesChanged.connect(self.updateChannelPlots)

        # trace name selection
        self._traceNameSelectionList = ListWidget()
        self._traceNameSelectionList.setSelectionMode(QAbstractItemView.MultiSelection)
        self._traceNameSelectionList.itemSelectionChanged.connect(self.onTraceNameSelectionChanged)
        self._traceNameSelectionList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # baseline
        self._showBaselineCheckBox = QCheckBox('Show Baseline')
        self._showBaselineCheckBox.setChecked(True)
        self._showBaselineCheckBox.stateChanged.connect(self.updateChannelPlots)
        self._applyBaselineCheckBox = QCheckBox('Apply Baseline')
        self._applyBaselineCheckBox.setChecked(False)
        self._applyBaselineCheckBox.stateChanged.connect(self.updateChannelPlots)

        # events
        self._showEventsCheckBox = QCheckBox('Show Events')
        self._showEventsCheckBox.setChecked(True)
        self._showEventsCheckBox.stateChanged.connect(self.updateChannelPlots)

        # show all episode traces in background
        self._showAllPrimaryTracesInBackgroundCheckBox = QCheckBox('Show All Traces in Background')
        self._showAllPrimaryTracesInBackgroundCheckBox.setChecked(False)
        self._showAllPrimaryTracesInBackgroundCheckBox.stateChanged.connect(self.updateChannelPlots)

        # visible objects selection
        self._visibilityMenu = QMenu()
        
        self._visibilityMenu.addSection('Channels')
        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(25, 5, 5, 15)
        vbox.setSpacing(5)
        vbox.addWidget(self._channelSelectionList)
        action = QWidgetAction(wrapper)
        action.setDefaultWidget(wrapper)
        self._visibilityMenu.addAction(action)
        
        self._visibilityMenu.addSection('Trace Names')
        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(25, 5, 5, 15)
        vbox.setSpacing(5)
        vbox.addWidget(self._traceNameSelectionList)
        action = QWidgetAction(wrapper)
        action.setDefaultWidget(wrapper)
        self._visibilityMenu.addAction(action)
        
        self._visibilityMenu.addSection('Options')
        # self._visibilityMenu.addSection('Baseline')
        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(25, 0, 0, 0)
        vbox.setSpacing(5)
        vbox.addWidget(self._showBaselineCheckBox)
        action = QWidgetAction(wrapper)
        action.setDefaultWidget(wrapper)
        self._visibilityMenu.addAction(action)
        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(25, 0, 0, 15)
        vbox.setSpacing(5)
        vbox.addWidget(self._applyBaselineCheckBox)
        action = QWidgetAction(wrapper)
        action.setDefaultWidget(wrapper)
        self._visibilityMenu.addAction(action)
        
        # self._visibilityMenu.addSection(' ')
        # self._visibilityMenu.addSection('Events')
        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(25, 0, 0, 15)
        vbox.setSpacing(5)
        vbox.addWidget(self._showEventsCheckBox)
        action = QWidgetAction(wrapper)
        action.setDefaultWidget(wrapper)
        self._visibilityMenu.addAction(action)

        # self._visibilityMenu.addSection(' ')
        self._moreVisibilityOptionsMenu = QMenu('More Options')

        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(25, 0, 0, 15)
        vbox.setSpacing(5)
        vbox.addWidget(self._showAllPrimaryTracesInBackgroundCheckBox)
        action = QWidgetAction(wrapper)
        action.setDefaultWidget(wrapper)
        self._moreVisibilityOptionsMenu.addAction(action)

        self._visibilityMenu.addMenu(self._moreVisibilityOptionsMenu)

        self._visibilityButton = QToolButton()
        self._visibilityButton.setIcon(qta.icon('ph.eye'))
        self._visibilityButton.setToolTip('Select Visible Objects')
        self._visibilityButton.setPopupMode(QToolButton.InstantPopup)
        self._visibilityButton.setMenu(self._visibilityMenu)

        # notes
        self._notesButton = QToolButton()
        self._notesButton.setIcon(qta.icon('ph.notepad-light'))
        self._notesButton.setToolTip('Notes')
        self._notesButton.clicked.connect(self.editNotes)

        # toolbar
        self._toolbar = QToolBar()
        self._mainMenuButtonAction = self._toolbar.addWidget(self._mainMenuButton)
        self._episodeSelectionBoxAction = self._toolbar.addWidget(self._episodeSelectionBox)
        self._traceSelectionBoxAction = self._toolbar.addWidget(self._traceSelectionBox)
        self._visibilityButtonAction = self._toolbar.addWidget(self._visibilityButton)
        self._notesButtonAction = self._toolbar.addWidget(self._notesButton)
    
    def sizeHint(self):
        return QSize(800, 600)
    
    def updateUI(self):
        # episode selection
        n_episodes = self.data.numEpisodes()
        self._episodeSelectionBoxAction.setVisible(n_episodes > 1)
        self._episodeSelectionBox.setMaximum(max(0, n_episodes - 1))

        # channel selection
        self.updateChannelSelectionList()

        # trace selection
        nmax_traces = self.data.numTraces()
        self._traceSelectionBoxAction.setVisible(nmax_traces > 1)
        self._traceSelectionBox.setMaximum(max(0, nmax_traces - 1))
        
        # trace name selection
        self.updateTraceNameSelectionList()
        
        # channel plots
        self.updateChannelPlots()

    def updateChannelPlots(self):
        # visible episodes
        n_episodes = self.data.numEpisodes()
        if self._episodeSelectionBoxAction.isVisible():
            visibleEpisodes = self._episodeSelectionBox.values()
        else:
            visibleEpisodes = np.arange(n_episodes)

        # visible channels
        nmax_channels = self.data.numChannels()
        if nmax_channels == 1:
            visibleChannels = np.arange(nmax_channels)
        else:
            visibleChannels = self.selectedChannels()

        # visible traces
        nmax_traces = self.data.numTraces()
        if nmax_traces == 1:
            visibleTraces = np.arange(1)
        else:
            visibleTraces = self._traceSelectionBox.values()
        
        # visible trace names
        visibleTraceNames = self.selectedTraceNames()
        if not visibleTraceNames:
            visibleTraceNames = ['Data']

        # existing channel plot widgets
        channelPlots = []
        for i in range(self._channelPlotsLayout.count()):
            item = self._channelPlotsLayout.itemAt(i).widget()
            if isinstance(item, PlotWidget):
                channelPlots.append(item)

        # update each channel plot (create new plot widgets as needed)
        for j in range(nmax_channels):
            # channel plot widget
            if len(channelPlots) > j:
                channelPlot = channelPlots[j]
            else:
                channelPlot = PlotWidget()
                self._channelPlotsLayout.addWidget(channelPlot, stretch=1)
                channelPlots.append(channelPlot)
            
            # store channel/episode info in channel plot widget
            channelPlot.pyCLAMP = self
            channelPlot.channelIndex = j
            channelPlot.episodeIndexes = visibleEpisodes
            
            # show/hide channel plot
            channelPlot.setVisible(j in visibleChannels)
            
            # don't bother updating plots for non-visible channels
            if not channelPlot.isVisible():
                continue

            # existing event items
            eventItems = [item for item in channelPlot.getViewBox().allChildren() if isinstance(item, EventItem)]

            # plot all visible events for this channel
            count = 0
            if self._showEventsCheckBox.isChecked():
                events = self.data.events(episodeIndexes=visibleEpisodes, channelIndexes=[j], eventGroups=None)
            else:
                events = []
            for EVENT in events:
                try:
                    xstart = EVENT['XStart']
                    xstop = EVENT['XStop'] if 'XStop' in EVENT else xstart
                    text = EVENT['Text'] if 'Text' in EVENT else ''
                except:
                    continue
                
                # add event to plot
                if len(eventItems) > count:
                    # update existing event item
                    eventItem = eventItems[count]
                else:
                    # add new event item
                    eventItem = EventItem()
                    channelPlot.getViewBox().addItem(eventItem)
                    eventItems.append(eventItem)
                
                eventItem.setEvent(EVENT)
                eventItem.pyCLAMP = self

                count += 1
                
            # remove extra event items
            while len(eventItems) > count:
                eventItem = eventItems.pop()
                channelPlot.getViewBox().removeItem(eventItem)
                eventItem.deleteLater()
            
            # existing channel plot curve items
            traceItems = [item for item in channelPlot.listDataItems() if isinstance(item, PlotDataItem)]
                
            # plot all visible traces for this channel
            count = 0
            colorIndex = 0
            traces = self.data.traces(episodeIndexes=visibleEpisodes, channelIndexes=[j], traceIndexes=visibleTraces, 
                     traceNames=visibleTraceNames, includeChildTraces=True, includeBaselineTraces=self.showBaseline())
            for TRACE in traces:
                try:
                    xdata, ydata, xzero, yzero = self.data.traceData(TRACE, applyXZero=True, applyYZero=self.applyBaseline())
                except:
                    continue
                
                # add trace to plot
                if len(traceItems) > count:
                    # update existing plot trace
                    traceItem = traceItems[count]
                    traceItem.setData(x=xdata, y=ydata)
                else:
                    # add new plot trace
                    traceItem = PlotDataItem(x=xdata, y=ydata)
                    channelPlot.addItem(traceItem)
                    traceItems.append(traceItem)
                
                # remove ref to TRACE dict while setting name and style
                # to avoid uneeded updates to TRACE
                traceItem.TRACE = None

                # trace name
                name = TRACE['Name'] if 'Name' in TRACE else 'data'
                traceItem.setName(name)
                
                # style trace
                STYLE = TRACE['Style'] if 'Style' in TRACE else {}
                colorIndex = traceItem.setSTYLE(STYLE, colorIndex)
                
                # store refs to TRACE dict and self in plot trace item
                traceItem.TRACE = TRACE
                traceItem.pyCLAMP = self

                # axis labels (based on first trace with axis labels)
                if j == visibleChannels[-1]:
                    if count == 0 or channelPlot.getAxis('bottom').labelText == '':
                        xlabel = TRACE['XLabel'] if 'XLabel' in TRACE else None
                        xunit = TRACE['XUnit'] if 'XUnit' in TRACE else None
                        channelPlot.getAxis('bottom').setLabel(text=xlabel, units=xunit)
                if count == 0 or channelPlot.getAxis('left').labelText == '':
                    ylabel = TRACE['YLabel'] if 'YLabel' in TRACE else None
                    yunit = TRACE['YUnit'] if 'YUnit' in TRACE else None
                    channelPlot.getAxis('left').setLabel(text=ylabel, units=yunit)

                count += 1
            
            # default axis labels and restrict xlabel to bottom plot only
            if j != visibleChannels[-1]:
                channelPlot.getAxis('bottom').setLabel(text='', units=None)
            elif channelPlot.getAxis('bottom').labelText == '':
                channelPlot.getAxis('bottom').setLabel(text='Sample')
            if channelPlot.getAxis('left').labelText == '':
                channelPlot.getAxis('left').setLabel(text=f'Channel {j}')
                
            # remove extra plot traces
            while len(traceItems) > count:
                traceItem = traceItems.pop()
                channelPlot.removeItem(traceItem)
                traceItem.deleteLater()
        
        # remove extra plots
        while len(channelPlots) > nmax_channels:
            j = len(channelPlots) - 1
            self._channelPlotsLayout.takeAt(j)
            channelPlot = channelPlots.pop()
            channelPlot.deleteLater()

        # left align visible channel plot axes
        visibleChannelPlots = [plot for plot in channelPlots if plot.isVisible()]
        if visibleChannelPlots:
            leftAxisWidths = [plot.getAxis('left').width() for plot in visibleChannelPlots]
            leftAxisWidth = np.max(leftAxisWidths)
            for plot in visibleChannelPlots:
                plot.getAxis('left').setWidth(leftAxisWidth)

        # link x-axis across channel plots
        for j in range(1, len(channelPlots)):
            channelPlots[j].setXLink(channelPlots[0])

    def selectedChannels(self):
        selectedChannels = [index.row() for index in self._channelSelectionList.selectedIndexes()]
        if not selectedChannels:
            nmax_channels = self.data.numChannels()
            selectedChannels = np.arange(nmax_channels)
        return selectedChannels

    def selectedTraceNames(self):
        selectedTraceNames = [item.text() for item in self._traceNameSelectionList.selectedItems()]
        if not selectedTraceNames:
            selectedTraceNames = [self._traceNameSelectionList.item(i).text() for i in range(self._traceNameSelectionList.count())]
        return selectedTraceNames
    
    def updateChannelSelectionList(self):
        selectedChannels = [index.row() for index in self._channelSelectionList.selectedIndexes()]
        channelNames = self.data.channelNames()
        for j in range(len(channelNames)):
            channelNames[j] = f'{j}: {channelNames[j]}'
        self._channelSelectionList.itemSelectionChanged.disconnect()
        self._channelSelectionList.clear()
        self._channelSelectionList.addItems(channelNames)
        for i in selectedChannels:
            if 0 <= i < self._channelSelectionList.count():
                self._channelSelectionList.item(i).setSelected(True)
        self._channelSelectionList.itemSelectionChanged.connect(self.onChannelSelectionChanged)

    def updateTraceNameSelectionList(self):
        selectedTraceNames = [item.text() for item in self._traceNameSelectionList.selectedItems()]
        traceNames = self.data.traceNames()
        self._traceNameSelectionList.itemSelectionChanged.disconnect()
        self._traceNameSelectionList.clear()
        self._traceNameSelectionList.addItems(traceNames)
        for i in range(self._traceNameSelectionList.count()):
            if self._traceNameSelectionList.item(i).text() in selectedTraceNames:
                self._traceNameSelectionList.item(i).setSelected(True)
        self._traceNameSelectionList.itemSelectionChanged.connect(self.onTraceNameSelectionChanged)
    
    def onChannelSelectionChanged(self):
        self.updateUI()
    
    def onTraceNameSelectionChanged(self):
        self.updateUI()
    
    def showBaseline(self):
        return self._showBaselineCheckBox.isChecked()
    
    def applyBaseline(self):
        return self._applyBaselineCheckBox.isChecked()
    
    def setShowBaseline(self, showBaseline):
        self._showBaselineCheckBox.setChecked(showBaseline)
        self.updateChannelPlots()
    
    def setApplyBaseline(self, applyBaseline):
        self._applyBaselineCheckBox.setChecked(applyBaseline)
        self.updateChannelPlots()
    
    def UNUSED_toggleShowBaseline(self):
        self.setShowBaseline(not self.showBaseline())
    
    def UNUSED_toggleApplyBaseline(self):
        self.setApplyBaseline(not self.applyBaseline())
    
    def editNotes(self):
        notes = self.data.notes()

        dlg = QDialog()
        form = QFormLayout(dlg)

        textEdit = QTextEdit()
        textEdit.setPlainText(notes)
        form.addRow('Notes', textEdit)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        form.addRow(btns)

        dlg.setWindowModality(Qt.ApplicationModal)
        if dlg.exec_() != QDialog.Accepted:
            return
        
        notes = textEdit.toPlainText()
        self.data.setNotes(notes)


pyClampWindows = []


def newPyClampWindow():
    global pyClampWindows
    window = pyCLAMP()
    window.show()
    window.updateUI()
    pyClampWindows.append(window)
    return window


class MultiIndexSpinBox(QSpinBox):
    """ QSpinBox allowing multiple space or comma-separated indexes or index ranges.
    
        Index ranges can be specified as first-last or start:stop[:step].
        Example:
            1 2 5-7 9 10:20:2 25 30:40 40 42 
    """

    valuesChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QSpinBox.__init__(self, *args, **kwargs)

        self._values = [self.value()]

        self._alwaysSort = True
    
    def sizeHint(self):
        size = QSpinBox.sizeHint(self)
        size.setWidth(150)
        return size
    
    def values(self):
        return [value for value in self._values if self.minimum() <= value <= self.maximum()]
    
    def setValues(self, values):
        if self._alwaysSort:
            values = sorted(values)
        self._values = values

        # value does not really matter much as we only care about self._values
        # however, for both up/down buttons to be enabled, value must not be at min or max
        self.setValue(min(self.minimum() + 1, self.maximum()))

        # !!! this is what you want to pay attention to, NOT self.valueChanged
        self.valuesChanged.emit()
    
    def setValuesFromText(self, text, validate=False):
        self.setValues(self.valuesFromText(text, validate))
    
    def valuesFromText(self, text, validate=False):
        text = text.strip()
        if text == '':
            return list(range(self.minimum(), self.maximum() + 1))
        fields = re.split('[,\s]+', text)
        values = []
        for field in fields:
            try:
                field = field.strip()
                if field == '':
                    continue
                if ':' in field:
                    sliceArgs = [int(arg) if len(arg.strip()) else None for arg in field.split(':')]
                    sliceObj = slice(*sliceArgs)
                    sliceIndexes = list(range(*sliceObj.indices(self.maximum() + 1)))
                    values.extend(sliceIndexes)
                elif '-' in field:
                    start, end = field.split('-')
                    values.extend(list(range(int(start), int(end)+1)))
                else:
                    values.append(int(field))
            except:
                if validate:
                    raise ValueError(f'Invalid text: {field}')
                else:
                    continue
        values = [value for value in values if self.minimum() <= value <= self.maximum()]
        return values
    
    def textFromValues(self, values):
        valueRanges = []
        for i, value in enumerate(values):
            if (len(valueRanges) == 0) or (value != valueRanges[-1][-1] + 1):
                valueRanges.append([value])
            else:
                valueRanges[-1].append(value)
        texts = []
        for valueRange in valueRanges:
            if len(valueRange) == 1:
                texts.append(str(valueRange[0]))
            else:
                texts.append(str(valueRange[0]) + '-' + str(valueRange[-1]))
        text = ' '.join(texts)
        return text
    
    def cleanText(self):
        # allows for trailing space
        text = self.text()
        if self.prefix():
            text = text[len(self.prefix()):]
        if self.suffix():
            text = text[:-len(self.suffix())]
        return text
    
    def validate(self, text, pos):
        try:
            self.valuesFromText(self.cleanText(), validate=True)
        except:
            return QValidator.Intermediate, text, pos
        return QValidator.Acceptable, text, pos
    
    def textFromValue(self, value):
        # ignore value, just use self.values()
        text = self.textFromValues(self.values())
        if self.cleanText().endswith(' '):
            text += ' '
        return text
    
    def valueFromText(self, text):
        # return value is irrelevant, just set the values
        self.setValuesFromText(self.cleanText())
        return self.value() # irrelevant
    
    def stepBy(self, steps):
        values = self.values()
        if len(values) == 0:
            value = self.minimum() if steps >= 0 else self.maximum()
        elif len(values) == 1:
            value = min(max(self.minimum(), values[0] + steps), self.maximum())
        else:
            value = values[0] if steps >= 0 else values[-1]
        self.setValues([value])
    
    def alwaysSort(self) -> bool:
        return self._alwaysSort
    
    def setAlwaysSort(self, alwaysSort: bool):
        self._alwaysSort = alwaysSort


class ListWidget(QListWidget):
    """ QListWidget that resizes to fit content. """
    def __init__(self,  *args, **kwargs):
        QListWidget.__init__(self,  *args, **kwargs)
    
    def sizeHint(self):
        n_items = self.model().rowCount()
        width = self.sizeHintForColumn(0)
        height = int(self.sizeHintForRow(0) * (n_items + 0.5))
        return QSize(width, height)
    
    def minimumSizeHint(self):
        return self.sizeHint()


class PlotWidget(pg.PlotWidget):
    """ pg.PlotWidget with custom view box. """

    def __init__(self,  *args, **kwargs):
        kwargs['viewBox'] = ViewBox()
        pg.PlotWidget.__init__(self, *args, **kwargs)

        self.pyCLAMP = None
        self.channelIndex = 0
        self.episodeIndexes = []

        # colormap (for default line colors)
        # MATLAB line colormap
        self.colormap = [
            (  0, 114, 189),
            (217,  83,  25),
            (237, 177,  32),
            (126,  47, 142),
            (119, 172,  48),
            ( 77, 190, 238),
            (162,  20,  47)
        ]
        # # Matplotlib tab10 colormap
        # self.colormap = [
        #     ( 31, 119, 180),
        #     (255, 127,  14),
        #     ( 44, 160,  44),
        #     (214,  39,  40),
        #     (148, 103, 189),
        #     (140,  86,  75),
        #     (227, 119, 194),
        #     (127, 127, 127),
        #     (188, 189,  34),
        #     ( 23, 190, 207)
        # ]
        self.colorIndex = 0


class ViewBox(pg.ViewBox):
    """ pg.ViewBox with custom context menu for measuring and curve fitting. """

    def __init__(self,  *args, **kwargs):
        pg.ViewBox.__init__(self, *args, **kwargs)

        self.initContextMenu()

        self._lastMousePressPositionInAxesCoords = {}
        self._isDrawingROIs = False
        self._isAddingEvents = False
    
    def getPlotItem(self):
        return self.parentWidget()
    
    def getPlotWidget(self):
        return self.getViewWidget()
    
    def mousePressEvent(self, event):
        self._lastMousePressPositionInAxesCoords[event.button()] = self.mapSceneToView(self.mapToScene(event.pos()))
        if self._isDrawingROIs:
            if event.button() != Qt.LeftButton:
                self.stopDrawingROIs()
            event.accept()
            return
        elif self._isAddingEvents:
            if event.button() == Qt.LeftButton:
                # add an event here
                x = self._lastMousePressPositionInAxesCoords[Qt.LeftButton].x()
                try:
                    plot = self.getPlotWidget()
                    j = plot.channelIndex
                    for i in plot.episodeIndexes:
                        CHANNEL = plot.pyCLAMP.DATA['Episodes'][i]['Channels'][j]
                        if 'Events' not in CHANNEL:
                            CHANNEL['Events'] = []
                        CHANNEL['Events'].append({'XStart': x})
                    plot.pyCLAMP.updateChannelPlots()
                except:
                    pass
            else:
                self._isAddingEvents = False
            event.accept()
            return
        pg.ViewBox.mousePressEvent(self, event)
    
    def mouseReleaseEvent(self, event):
        if self._isDrawingROIs:
            if event.button() == Qt.LeftButton:
                self._ROI = None
                event.accept()
                return
        pg.ViewBox.mouseReleaseEvent(self, event)
    
    def mouseMoveEvent(self, event):
        if self._isDrawingROIs:
            if event.buttons() & Qt.LeftButton:
                startPosInAxes = self._lastMousePressPositionInAxesCoords[Qt.LeftButton]
                posInAxes = self.mapSceneToView(self.mapToScene(event.pos()))
                if self._ROIOrientation == "vertical":
                    limits = sorted([startPosInAxes.x(), posInAxes.x()])
                elif self._ROIOrientation == "horizontal":
                    limits = sorted([startPosInAxes.y(), posInAxes.y()])
                if self._ROI is None:
                    self._ROI = ROIItem(orientation=self._ROIOrientation, values=limits)
                    self.addItem(self._ROI)
                else:
                    self._ROI.setRegion(limits)
                event.accept()
                return
        pg.ViewBox.mouseMoveEvent(self, event)
    
    def initContextMenu(self):
        self._ROIsMenu = QMenu("ROIs")
        self._ROIsMenu.addAction("Show All", self.showROIs)
        self._ROIsMenu.addAction("Hide All", self.hideROIs)
        self._ROIsMenu.addSection(" ")
        self._ROIsMenu.addAction("Delete All", self.deleteROIs)

        self._measureMenu = QMenu("Measure in each ROI")
        self._measureMenu.addAction("Mean", lambda: self.measure(measurementType="Mean"))
        self._measureMenu.addAction("Median", lambda: self.measure(measurementType="Median"))
        self._measureMenu.addAction("Min", lambda: self.measure(measurementType="Min"))
        self._measureMenu.addAction("Max", lambda: self.measure(measurementType="Max"))
        self._measureMenu.addAction("AbsMax", lambda: self.measure(measurementType="Absmax"))
        self._measureMenu.addAction("Variance", lambda: self.measure(measurementType="Var"))
        self._measureMenu.addAction("Standard Deviation", lambda: self.measure(measurementType="Std"))

        self._eventsMenu = QMenu("Events")
        self._eventsMenu.addAction("Show All", self.showEvents)
        self._eventsMenu.addAction("Hide All", self.hideEvents)
        self._eventsMenu.addSection(" ")
        self._eventsMenu.addAction("Delete All", self.deleteEvents)

        # append to default context menu
        self.menu.addAction('Edit Axis Labels', self.editAxisLabels)
        self.menu.addSection('ROIs')
        self.menu.addAction('Draw X-Axis ROIs (right-click to stop)', lambda: self.startDrawingROIs(orientation='vertical'))
        self.menu.addMenu(self._ROIsMenu)
        self.menu.addMenu(self._measureMenu)
        self.menu.addSection('Fits')
        self.menu.addAction('Curve Fit all visible traces in plot', self.curveFit)
        self.menu.addSection('Events')
        self.menu.addAction('Add Events  (right-click to stop)', self.addEvents)
        self.menu.addMenu(self._eventsMenu)
        self.menu.addSection('Other')  # for appended menus from other objects
    
    def editAxisLabels(self):
        pyCLAMP = self.getPlotWidget().pyCLAMP
        axisLabelsDialog(pyCLAMP, pyCLAMP.data)
        pyCLAMP.updateUI()
    
    def startDrawingROIs(self, orientation="vertical"):
        self._isDrawingROIs = True
        self._ROIOrientation = orientation
        self._ROI = None

    def stopDrawingROIs(self):
        self._isDrawingROIs = False
        self._ROI = None
    
    def ROIs(self):
        return [item for item in self.allChildren() if isinstance(item, ROIItem)]
    
    def hideROIs(self):
        for ROI in self.ROIs():
            ROI.setVisible(False)
    
    def showROIs(self):
        for ROI in self.ROIs():
            ROI.setVisible(True)
    
    def deleteROIs(self):
        for ROI in self.ROIs():
            self.removeItem(ROI)
            ROI.deleteLater()
    
    def measure(self, measurementType, plotDataItems=None):
        try:
            UI = self.getPlotWidget().pyCLAMP
        except:
            return
        
        if plotDataItems is None:
            plotDataItems = [item for item in self.allChildren() if isinstance(item, PlotDataItem)]
        elif isinstance(plotDataItems, PlotDataItem):
            # make sure it is a list
            plotDataItems = [plotDataItems]
        if not plotDataItems:
            return

        # measure only within each non-hidden ROI (otherwise whole curve)
        xROIs = [ROI for ROI in self.ROIs() if ROI.isVisible() and ROI.orientation == "vertical"]
        xRegions = [ROI.getRegion() for ROI in xROIs]

        measurementTraces = []
        parentTraces = []
        measurementTraceItems = []
        for plotDataItem in plotDataItems:
            try:
                # try and get source data if available
                parentTrace = plotDataItem.TRACE
                if '_BaselineOf_' in parentTrace:
                    # do not measure baselines
                    continue
                xdata, ydata, xzero, yzero = UI.data.traceData(parentTrace, applyXZero=True, applyYZero=UI.applyBaseline())
            except:
                # use data in plotDataItem
                # !!! WARNING !!! this may not be the same as the source data due to downsampling, etc.
                # xdata = plotDataItem.xData
                # ydata = plotDataItem.yData
                continue
            
            xmeasure = []
            ymeasure = []
            xlims = xRegions if xRegions else [(xdata[0], xdata[-1])]
            for xlim in xlims:
                xmin, xmax = xlim
                inROIMask = (xdata >= xmin) & (xdata <= xmax)
                xinROI = xdata[inROIMask]
                yinROI = ydata[inROIMask]
                xROICenter = xinROI[int(len(xinROI) / 2)]
                if measurementType == "Mean":
                    xm = xROICenter
                    ym = np.mean(yinROI)
                elif measurementType == "Median":
                    xm = xROICenter
                    ym = np.median(yinROI)
                elif measurementType == "Min":
                    i = np.argmin(yinROI)
                    xm = xinROI[i]
                    ym = yinROI[i]
                elif measurementType == "Max":
                    i = np.argmax(yinROI)
                    xm = xinROI[i]
                    ym = yinROI[i]
                elif measurementType == "Absmax":
                    i = np.argmax(np.abs(yinROI))
                    xm = xinROI[i]
                    ym = yinROI[i]
                elif measurementType == "Std":
                    xm = xROICenter
                    ym = np.std(yinROI)
                elif measurementType == "Var":
                    xm = xROICenter
                    ym = np.var(yinROI)
                xmeasure.append(xm)
                ymeasure.append(ym)
            
            if not ymeasure:
                continue
            else:
                xmeasure = np.array(xmeasure)
                ymeasure = np.array(ymeasure)
                order = np.argsort(xmeasure)
                xmeasure = xmeasure[order]
                ymeasure = ymeasure[order]

            # add measurement scatter curve to plot
            measurementTRACEItem = PlotDataItem(x=xmeasure, y=ymeasure, pen=None,#pg.mkPen(color=(255, 0, 0), width=3), 
                symbol='o', symbolSize=10, symbolPen=pg.mkPen(color=(255, 0, 0), width=3), symbolBrush=(255, 0, 0, 0))
            self.getPlotWidget().addItem(measurementTRACEItem)
            measurementTraceItems.append(measurementTRACEItem)

            # measurement TRACE
            try:
                parentTrace = plotDataItem.TRACE
                xzero, yzero = None, None
                if 'XZero' in parentTrace:
                    xzero = parentTrace['XZero']
                    xmeasure += xzero  # assume XZero has already been applied to xdata
                if 'YZero' in parentTrace:
                    yzero = parentTrace['YZero']
                    if type(yzero) not in [float, int]:
                        yzero = np.interp(xmeasure, xdata, yzero)
                    if UI.applyBaseline():
                        ymeasure += yzero
                measurementTrace = {
                    'XData': xmeasure,
                    'YData': ymeasure
                }
                if xzero is not None:
                    measurementTrace['XZero'] = xzero
                if yzero is not None:
                    measurementTrace['YZero'] = yzero
                for key in ['XLabel', 'YLabel', 'XUnit', 'YUnit']:
                    if key in parentTrace:
                        measurementTrace[key] = parentTrace[key]
                STYLE = parentTrace['Style'] if 'Style' in parentTrace else {}
                STYLE['LineStyle'] = 'none'
                STYLE['Marker'] = 'o'
                STYLE['MarkerSize'] = 10
                if 'MarkerEdgeWidth' not in STYLE:
                    STYLE['MarkerEdgeWidth'] = 2
                measurementTrace['Style'] = STYLE
                measurementTraces.append(measurementTrace)
                parentTraces.append(parentTrace)
            except:
                pass
        
        if not measurementTraces:
            for item in measurementTraceItems:
                item._delete()
            return
        
        dlg = QDialog(self.getPlotWidget())
        dlg.setWindowTitle('Keep measurement?')
        form = QFormLayout(dlg)
        
        nameEdit = QLineEdit(measurementType)
        form.addRow('Name', nameEdit)

        openInNewWindowCheckBox = QCheckBox('Open measurement in a new window')
        openInNewWindowCheckBox.setChecked(False)
        form.addRow(openInNewWindowCheckBox)

        mergeMeasurementsCheckBox = QCheckBox('Merge measurements into a single trace')
        mergeMeasurementsCheckBox.setChecked(False)
        form.addRow(None, mergeMeasurementsCheckBox)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        form.addRow(btns)

        dlg.setWindowModality(Qt.ApplicationModal)
        if dlg.exec_() != QDialog.Accepted:
            for item in measurementTraceItems:
                item._delete()
            return
        
        name = nameEdit.text().strip()
        for measurementTrace in measurementTraces:
            measurementTrace['Name'] = name
        
        if openInNewWindowCheckBox.isChecked():
            for item in measurementTraceItems:
                item._delete()
            newWindow = newPyClampWindow()
            if mergeMeasurementsCheckBox.isChecked():
                # concatenate all measurement traces into a single trace
                allxdata = np.empty((0,))
                allydata = np.empty((0,))
                for measurementTrace in measurementTraces:
                    xdata, ydata, xzero, yzero = UI.data.traceData(measurementTrace, applyXZero=True, applyYZero=True)
                    allxdata = np.concatenate([allxdata, xdata])
                    allydata = np.concatenate([allydata, ydata])
                measurementTrace = measurementTraces[0]
                measurementTrace['XData'] = allxdata
                measurementTrace['YData'] = allydata
                if 'XZero' in measurementTrace:
                    del measurementTrace['XZero']
                if 'YZero' in measurementTrace:
                    del measurementTrace['YZero']
                measurementTrace['Style']['LineStyle'] = '-'
                newWindow.data.addTrace(0, 0, measurementTrace)
            else:
                for i, measurementTrace in enumerate(measurementTraces):
                    newWindow.data.addTrace(i, 0, measurementTrace)
            newWindow.updateUI()
            return

        # add each measurement trace to its parent trace
        for measurementTrace, parentTrace in zip(measurementTraces, parentTraces):
            if 'Traces' not in parentTrace:
                parentTrace['Traces'] = []
            parentTrace['Traces'].append(measurementTrace)

        UI.updateUI()
    
    def curveFit(self, options: dict=None, plotDataItems=None):
        try:
            pyCLAMP = self.getPlotWidget().pyCLAMP
        except:
            return
        
        if options is None:
            options = {}
            try:
                if self._lastFitType:
                    options['fitType'] = self._lastFitType
            except:
                pass
            try:
                if self._lastEquation:
                    options['equation'] = self._lastEquation
            except:
                pass
            options = self.curveFitDialog(options)
            if options is None:
                return
        
        if plotDataItems is None:
            plotDataItems = [item for item in self.allChildren() if isinstance(item, PlotDataItem)]
        elif isinstance(plotDataItems, PlotDataItem):
            # make sure it is a list
            plotDataItems = [plotDataItems]
        if not plotDataItems:
            return

        # measure only within each non-hidden ROI (otherwise whole curve)
        if options['optimizeWithinROIsOnly'] or options['fitWithinROIsOnly']:
            xROIs = [ROI for ROI in self.ROIs() if ROI.isVisible() and ROI.orientation == "vertical"]
            xRegions = [ROI.getRegion() for ROI in xROIs]
            options['ROIXLims'] = xRegions
        else:
            xRegions = []
        
        # fit equation
        if 'equation' in options:
            equation = options['equation']
            fitModel = lmfit.models.ExpressionModel(equation, independent_vars=['x'])
            for param in fitModel.param_names:
                initialValue = options['params'][param]['value']
                vary = options['params'][param]['vary']
                lowerBound, upperBound = options['params'][param]['bounds']
                if initialValue is None:
                    if not vary:
                        QErrorMessage(self.getPlotWidget()).showMessage(f'Parameter {param} is fixed but has no initial value.')
                        return
                    initialValue = 1
                if initialValue < lowerBound:
                    initialValue = lowerBound
                if initialValue > upperBound:
                    initialValue = upperBound
                hint = {}
                hint['value'] = initialValue
                if lowerBound != -np.inf:
                    hint['min'] = lowerBound
                if upperBound != np.inf:
                    hint['max'] = upperBound
                fitModel.set_param_hint(param, **hint)
            params = fitModel.make_params()
            self._lastEquation = equation
        
        self._lastFitType = options['fitType']

        fitTraces = []
        parentTraces = []
        fitTraceItems = []
        for plotDataItem in plotDataItems:
            try:
                # try and get source data if available
                TRACE = plotDataItem.TRACE
                if '_BaselineOf_' in TRACE:
                    # do not measure baselines
                    continue
                xdata, ydata, xzero, yzero = pyCLAMP.data.traceData(TRACE, applyXZero=True, applyYZero=pyCLAMP.applyBaseline())
            except:
                # use data in plotDataItem
                # !!! WARNING !!! this may not be the same as the source data due to downsampling, etc.
                # xdata = plotDataItem.xData
                # ydata = plotDataItem.yData
                continue
            
            # ROIs mask
            if xRegions:
                inROIsMask = np.zeros(len(xdata), dtype=bool)
                for xlim in xRegions:
                    xmin, xmax = xlim
                    inROIsMask[(xdata >= xmin) & (xdata <= xmax)] = True
            
            # restrict optimization to ROIs?
            if options['optimizeWithinROIsOnly'] and xRegions:
                xopt, yopt = xdata[inROIsMask], ydata[inROIsMask]
            else:
                xopt, yopt = xdata, ydata
            
            # restrict fit output to ROIs?
            if options['fitWithinROIsOnly'] and xRegions:
                xfit = xdata[inROIsMask]
            else:
                xfit = xdata
            
            fitTRACE = {}
            if options['fitType'] == 'Mean':
                yfit = np.full(len(xfit), np.mean(yopt))
                fitTRACE['Fit'] = {
                    'Type': 'Mean'
                }
            elif options['fitType'] == 'Median':
                yfit = np.full(len(xfit), np.median(yopt))
                fitTRACE['Fit'] = {
                    'Type': 'Median'
                }
            elif options['fitType'] == 'Polynomial':
                degree = options['degree']
                coef = np.polyfit(xopt, yopt, degree)
                yfit = np.polyval(coef, xfit)
                fitTRACE['Fit'] = {
                    'Type': 'Polynomial',
                    'Degree': degree,
                    'Coefficients': coef
                }
            elif options['fitType'] == 'Spline':
                n_segments = options['numSegments']
                segmentLength = max(1, int(len(yopt) / n_segments))
                knots = xopt[segmentLength:-segmentLength:segmentLength]
                if len(knots) < 2:
                    knots = xopt[[1, -2]]
                knots, coef, degree = sp.interpolate.splrep(xopt, yopt, t=knots)
                yfit = sp.interpolate.splev(xfit, (knots, coef, degree), der=0)
                fitTRACE['Fit'] = {
                    'Type': 'Spline',
                    'NumSegments': n_segments,
                    'Knots': knots,
                    'Coefficients': coef,
                    'Degree': degree
                }
            elif 'equation' in options:
                equation = options['equation']
                result = fitModel.fit(yopt, params, x=xopt)
                # print(result.fit_report())
                yfit = fitModel.eval(result.params, x=xfit)
                fitTRACE['Fit'] = {
                    'Equation': equation,
                    'Params': result.params.valuesdict()
                }
            else:
                continue

            # add fit curve to plot
            fitTRACEItem = PlotDataItem(x=xfit, y=yfit, pen=pg.mkPen(color=(255, 0, 0), width=3))
            self.getPlotWidget().addItem(fitTRACEItem)
            fitTraceItems.append(fitTRACEItem)

            # fit TRACE
            try:
                TRACE = plotDataItem.TRACE
                if xfit is xdata:
                    xfit = TRACE['XData'] if 'XData' in TRACE else None
                if xfit is not None:
                    fitTRACE['XData'] = xfit
                if 'YZero' in TRACE:
                    yzero = TRACE['YZero']
                    if xRegions:
                        if isinstance(yzero, np.ndarray) and len(yzero) == len(ydata):
                            yzero = yzero[inROIsMask]
                    fitTRACE['YZero'] = yzero
                    if pyCLAMP.applyBaseline():
                        yfit += yzero
                fitTRACE['YData'] = yfit
                fitTraces.append(fitTRACE)
                parentTraces.append(TRACE)
            except:
                pass
        
        if not fitTraces:
            for item in fitTraceItems:
                item._delete()
            return
        
        dlg = QDialog(self.getPlotWidget())
        dlg.setWindowTitle('Keep fit?')
        form = QFormLayout(dlg)
        
        defaultName = options['equation'] if 'equation' in options else options['fitType']
        nameEdit = QLineEdit(defaultName)
        form.addRow('Name', nameEdit)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        form.addRow(btns)

        dlg.setWindowModality(Qt.ApplicationModal)
        if dlg.exec_() != QDialog.Accepted:
            for item in fitTraceItems:
                item._delete()
            return
        
        name = nameEdit.text().strip()

        for fitTRACE, TRACE in zip(fitTraces, parentTraces):
            fitTRACE['Name'] = name
            for key in ['XLabel', 'YLabel', 'XUnit', 'YUnit']:
                if key in TRACE:
                    fitTRACE[key] = TRACE[key]
            STYLE = TRACE['Style'] if 'Style' in TRACE else {}
            lineWidth = STYLE['LineWidth'] if 'LineWidth' in STYLE else 1
            fitTRACE['Style'] = {
                'LineStyle': '-',
                'LineWidth': lineWidth,
                'Marker': 'none'
            }
            if 'Traces' not in TRACE:
                TRACE['Traces'] = []
            TRACE['Traces'].append(fitTRACE)

        pyCLAMP.updateUI()

    def curveFitDialog(self, options: dict=None):
        if options is None:
            options = {}
        if 'equation' not in options:
            try:
                options['equation'] = self._lastCurveFitEquation
            except:
                pass
        
        dlg = CurveFitDialog(options, self.getPlotWidget())

        dlg.setWindowModality(Qt.ApplicationModal)
        if dlg.exec_() != QDialog.Accepted:
            return None
        return dlg.options()
    
    def events(self):
        return [item for item in self.allChildren() if isinstance(item, EventItem)]
    
    def hideEvents(self):
        for event in self.events():
            event.setVisible(False)
    
    def showEvents(self):
        for event in self.events():
            event.setVisible(True)
    
    def deleteEvents(self):
        for event in self.events():
            self.removeItem(event)
            event.deleteLater()
    
    def addEvents(self):
        self._isAddingEvents = True


class CurveFitDialog(QDialog):
    def __init__(self, options, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        if options is None:
            options = {}

        self.fitTypes = {
            'Mean': '', 
            'Median': '', 
            'Line': 'a * x + b', 
            'Polynomial': '', 
            'Spline': '', 
            'Exponential Decay': 'a * exp(-b * x) + c', 
            'Exponential Rise': 'a * (1 - exp(-b * x)) + c', 
            'Hill Equation': 'a / (1 + (K / x)**n)', 
            'Custom': ''
            }
        self.fitTypeSelectionBox = QListWidget()
        self.fitTypeSelectionBox.addItems(self.fitTypes.keys())
        self.fitTypeSelectionBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.fitTypeSelectionBox.currentItemChanged.connect(self.onEquationSelected)

        self.optimizeWithinROIsOnlyCheckBox = QCheckBox('Optimize within visible ROIs only')
        self.optimizeWithinROIsOnlyCheckBox.setChecked(True)

        self.fitWithinROIsOnlyCheckBox = QCheckBox('Fit within visible ROIs only')
        self.fitWithinROIsOnlyCheckBox.setChecked(False)

        self.equationEdit = QLineEdit()
        self.equationEdit.textEdited.connect(self.onEquationChanged)
        self._customEquation = ''

        self.paramNames = []
        self.paramInitialValueEdits = {}
        self.paramFixedCheckBoxes = {}
        self.paramLowerBoundEdits = {}
        self.paramUpperBoundEdits = {}

        self.paramsGrid = QGridLayout()
        self.paramsGrid.addWidget(QLabel('Parameter'), 0, 0)
        self.paramsGrid.addWidget(QLabel('Initial Value'), 0, 1)
        self.paramsGrid.addWidget(QLabel('Fixed'), 0, 2)
        self.paramsGrid.addWidget(QLabel('Lower Bound'), 0, 3)
        self.paramsGrid.addWidget(QLabel('Upper Bound'), 0, 4)

        self.equationGroupBox = QGroupBox('Equation')
        vbox = QVBoxLayout(self.equationGroupBox)
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.setSpacing(5)
        vbox.addWidget(self.equationEdit)
        vbox.addLayout(self.paramsGrid)

        self.polynomialDegreeSpinBox = QSpinBox()
        self.polynomialDegreeSpinBox.setValue(2)

        self.polynomialGroupBox = QGroupBox('Polynomial')
        form = QFormLayout(self.polynomialGroupBox)
        form.setContentsMargins(5, 5, 5, 5)
        form.setSpacing(5)
        form.addRow('Degree', self.polynomialDegreeSpinBox)

        self.splineNumSegmentsSpinBox = QSpinBox()
        self.splineNumSegmentsSpinBox.setValue(10)

        self.splineGroupBox = QGroupBox('Spline')
        form = QFormLayout(self.splineGroupBox)
        form.setContentsMargins(5, 5, 5, 5)
        form.setSpacing(5)
        form.addRow('# Segments', self.splineNumSegmentsSpinBox)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(5)
        vbox.addWidget(self.optimizeWithinROIsOnlyCheckBox)
        vbox.addWidget(self.fitWithinROIsOnlyCheckBox)
        vbox.addWidget(self.equationGroupBox)
        vbox.addWidget(self.polynomialGroupBox)
        vbox.addWidget(self.splineGroupBox)
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(5)
        hbox.addWidget(self.fitTypeSelectionBox)
        hbox.addLayout(vbox)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(btns)

        if 'fitType' in options:
            index = list(self.fitTypes.keys()).index(options['fitType'])
            if index is not None and index != -1:
                self.fitTypeSelectionBox.setCurrentRow(index)
                self.onEquationSelected()
            if options['fitType'] == 'Custom' and 'equation' in options:
                self.equationEdit.setText(options['equation'])
                self._customEquation = options['equation']
    
    def sizeHint(self):
        self.fitTypeSelectionBox.setMinimumWidth(self.fitTypeSelectionBox.sizeHintForColumn(0))
        return QSize(600, 400)
    
    def onEquationSelected(self):
        fitType = self.fitTypeSelectionBox.currentItem().text()
        if fitType == 'Mean':
            self.equationGroupBox.setVisible(False)
            self.polynomialGroupBox.setVisible(False)
            self.splineGroupBox.setVisible(False)
        elif fitType == 'Median':
            self.equationGroupBox.setVisible(False)
            self.polynomialGroupBox.setVisible(False)
            self.splineGroupBox.setVisible(False)
        elif fitType == 'Polynomial':
            self.equationGroupBox.setVisible(False)
            self.polynomialGroupBox.setVisible(True)
            self.splineGroupBox.setVisible(False)
        elif fitType == 'Spline':
            self.equationGroupBox.setVisible(False)
            self.polynomialGroupBox.setVisible(False)
            self.splineGroupBox.setVisible(True)
        else:
            self.equationGroupBox.setVisible(True)
            self.polynomialGroupBox.setVisible(False)
            self.splineGroupBox.setVisible(False)
            if fitType == 'Custom':
                self.equationEdit.setText(self._customEquation)
            else:
                equation = self.fitTypes[fitType]
                self.equationEdit.setText(equation)
            self.onEquationChanged()

    def onEquationChanged(self):
        equation = self.equationEdit.text()
        if equation not in list(self.fitTypes.values()):
            self._customEquation = equation
        try:
            fitModel = lmfit.models.ExpressionModel(equation, independent_vars=['x'])
            self.paramNames = fitModel.param_names
        except:
            self.paramNames = []
        for name in self.paramNames:
            if name not in self.paramInitialValueEdits:
                self.paramInitialValueEdits[name] = QLineEdit()
            if name not in self.paramFixedCheckBoxes:
                self.paramFixedCheckBoxes[name] = QCheckBox()
            if name not in self.paramLowerBoundEdits:
                self.paramLowerBoundEdits[name] = QLineEdit()
            if name not in self.paramUpperBoundEdits:
                self.paramUpperBoundEdits[name] = QLineEdit()
        self.updateParamsGrid()
    
    def clearParamsGrid(self):
        for row in range(1, self.paramsGrid.rowCount()):
            for col in range(self.paramsGrid.columnCount()):
                item = self.paramsGrid.itemAtPosition(row, col)
                if item:
                    widget = item.widget()
                    self.paramsGrid.removeItem(item)
                    widget.setParent(None)
                    widget.setVisible(False)
    
    def updateParamsGrid(self):
        self.clearParamsGrid()
        for i, name in enumerate(self.paramNames):
            self.paramsGrid.addWidget(QLabel(name), i + 1, 0)
            self.paramsGrid.addWidget(self.paramInitialValueEdits[name], i + 1, 1)
            self.paramsGrid.addWidget(self.paramFixedCheckBoxes[name], i + 1, 2)
            self.paramsGrid.addWidget(self.paramLowerBoundEdits[name], i + 1, 3)
            self.paramsGrid.addWidget(self.paramUpperBoundEdits[name], i + 1, 4)
            self.paramInitialValueEdits[name].setVisible(True)
            self.paramFixedCheckBoxes[name].setVisible(True)
            self.paramLowerBoundEdits[name].setVisible(True)
            self.paramUpperBoundEdits[name].setVisible(True)
    
    def options(self):
        options = {}
        fitType = self.fitTypeSelectionBox.currentItem().text()
        if fitType == 'Mean':
            options['fitType'] = 'Mean'
        elif fitType == 'Median':
            options['fitType'] = 'Median'
        elif fitType == 'Polynomial':
            options['fitType'] = 'Polynomial'
            options['degree'] = self.polynomialDegreeSpinBox.value()
        elif fitType == 'Spline':
            options['fitType'] = 'Spline'
            options['numSegments'] = self.splineNumSegmentsSpinBox.value()
        else:
            options['equation'] = self.equationEdit.text()
            if options['equation'] in list(self.fitTypes.values()):
                index = list(self.fitTypes.values()).index(options['equation'])
                options['fitType'] = list(self.fitTypes.keys())[index]
            else:
                options['fitType'] = 'Custom'
            options['params'] = {}
            for name in self.paramNames:
                try:
                    value = float(self.paramInitialValueEdits[name].text())
                except:
                    value = None
                vary = not self.paramFixedCheckBoxes[name].isChecked()
                try:
                    lowerBound = float(self.paramLowerBoundEdits[name].text())
                except:
                    lowerBound = -np.inf
                try:
                    upperBound = float(self.paramUpperBoundEdits[name].text())
                except:
                    upperBound = np.inf
                options['params'][name] = {
                    'value': value,
                    'vary': vary,
                    'bounds': (lowerBound, upperBound)
                }
        options['optimizeWithinROIsOnly'] = self.optimizeWithinROIsOnlyCheckBox.isChecked()
        options['fitWithinROIsOnly'] = self.fitWithinROIsOnlyCheckBox.isChecked()
        return options


class PlotDataItem(pg.PlotDataItem):
    """ Clickable pg.PlotDataItem with context menu. """

    def __init__(self, *args, **kwargs):
        pg.PlotDataItem.__init__(self, *args, **kwargs)
        
        # !!! a negative z-value makes right-click context menu not work
        self.setZValue(2)

        self.pyCLAMP = None
        self.TRACE = None
        self.menu = None
    
    def _delete(self):
        try:
            self.pyCLAMP.data.deleteTrace(self.TRACE)
            self.pyCLAMP.updateUI()
        except:
            self.getViewBox().removeItem(self)
            self.deleteLater()

    def hasCurve(self):
        pen = pg.mkPen(self.opts['pen'])
        return pen.style() != Qt.PenStyle.NoPen
    
    def hasScatter(self):
        return 'symbol' in self.opts and self.opts['symbol'] is not None
    
    def shape(self):
        # shape is a QPainterPath
        if self.hasCurve():
            return self.curve.shape()
        elif self.hasScatter():
            return self.scatter.shape()

    def boundingRect(self):
        return self.shape().boundingRect()
    
    def mouseClickEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.hasCurve():
                if self.curve.mouseShape().contains(event.pos()):
                    if self.raiseContextMenu(event):
                        event.accept()
                        return
            elif self.hasScatter():
                if len(self.scatter.pointsAt(event.pos())) > 0:
                    if self.raiseContextMenu(event):
                        event.accept()
                        return
    
    def raiseContextMenu(self, event):
        menu = self.getContextMenus()
        
        # Let the scene add on to the end of our context menu (this is optional)
        # menu.addSection('View')
        # menu = self.scene().addParentContextMenus(self, menu, event)
        
        pos = event.screenPos()
        menu.popup(QPoint(int(pos.x()), int(pos.y())))
        return True
    
    def getContextMenus(self, event=None):
        name = self.name()
        if name is None:
            name = 'Data'
        
        self.menu = QMenu()
        self.menu.addSection('Trace: ' + name)
        self.menu.addAction('Rename', self.editNameDialog)
        self.menu.addAction('Edit Style', self.editStyleDialog)
        try:
            parentTRACE = self.pyCLAMP.data.parentTrace(self.TRACE)
            if parentTRACE is not None:
                self.menu.addSection(' ')
                self.menu.addAction('Set as Baseline of Parent', self.setAsBaselineOfParent)
            if 'YZero' in self.TRACE:
                self.menu.addSection(' ')
                self.menu.addAction('Remove Baseline', self.removeBaseline)
        except Exception as err:
            print('PlotDataItem.getContextMenus:', err)
        try:
            if 'XData' in self.TRACE:
                self.menu.addSection(' ')
                self.menu.addAction('Set XData to Samples', self.setXDataToSamples)
        except Exception as err:
            print('PlotDataItem.getContextMenus:', err)
        self.menu.addSection(' ')
        self.menu.addAction('Delete', self._delete)
        return self.menu
    
    def name(self):
        try:
            return self.TRACE['Name'] if 'Name' in self.TRACE else 'Data'
        except:
            return self.opts['Name'] if 'Name' in self.opts else 'Data'
    
    def setName(self, name):
        try:
            if name is None:
                if 'Name' in self.TRACE:
                    del self.TRACE['Name']
            else:
                self.TRACE['Name'] = name
        except:
            pass

        self.opts['Name'] = name
    
    def itemSTYLE(self):
        STYLE = {}

        pen = pg.mkPen(self.opts['pen'])
        symbolPen = pg.mkPen(self.opts['symbolPen'])
        symbolBrush = pg.mkBrush(self.opts['symbolBrush'])

        color = pen.color()
        STYLE['Color'] = color.red(), color.green(), color.blue(), color.alpha()

        lineStyles = {
            Qt.PenStyle.NoPen: 'none',
            Qt.PenStyle.SolidLine: '-',
            Qt.PenStyle.DashLine: '--',
            Qt.PenStyle.DotLine: ':',
            Qt.PenStyle.DashDotLine: '-.'
        }
        STYLE['LineStyle'] = lineStyles[pen.style()]
        STYLE['LineWidth'] = pen.widthF()
        STYLE['Marker'] = self.opts['symbol']
        STYLE['MarkerSize'] = self.opts['symbolSize']
        STYLE['MarkerEdgeWidth'] = symbolPen.widthF()

        color = symbolPen.color()
        STYLE['MarkerEdgeColor'] = color.red(), color.green(), color.blue(), color.alpha()

        color = symbolBrush.color()
        STYLE['MarkerFaceColor'] = color.red(), color.green(), color.blue(), color.alpha()

        return STYLE
    
    def STYLE(self):
        try:
            return self.TRACE['Style'] if 'Style' in self.TRACE else {}
        except:
            return self.itemSTYLE()
    
    def setSTYLE(self, STYLE: dict, colorIndex=None):
        try:
            if STYLE is None:
                if 'Style' in self.TRACE:
                    del self.TRACE['Style']
            else:
                self.TRACE['Style'] = STYLE
        except:
            pass

        if STYLE is None:
            STYLE = {}
        
        currentSTYLE = self.itemSTYLE()

        # color
        color = STYLE['Color'] if 'Color' in STYLE else 'auto'
        if color == 'auto':
            if colorIndex is not None:
                plot = self.getViewBox().getPlotWidget()
                colormap = plot.colormap
                color = colormap[colorIndex % len(colormap)]
                colorIndex += 1
            else:
                color = currentSTYLE['Color']

        # line
        lineStyle = STYLE['LineStyle'] if 'LineStyle' in STYLE else '-'
        # convert to Qt line style
        if not isinstance(lineStyle, int):
            lineStyles = {
                'none': Qt.PenStyle.NoPen, 
                '-': Qt.PenStyle.SolidLine, 
                '--': Qt.PenStyle.DashLine, 
                ':': Qt.PenStyle.DotLine, 
                '-.': Qt.PenStyle.DashDotLine
            }
            lineStyle = lineStyles[lineStyle]

        lineWidth = STYLE['LineWidth'] if 'LineWidth' in STYLE else 1
        
        if lineStyle is None:
            linePen = None
        else:
            linePen = pg.mkPen(color=color, width=lineWidth, style=lineStyle)
        self.setPen(linePen)

        # symbol
        marker = STYLE['Marker'] if 'Marker' in STYLE else 'none'
        if marker == 'none':
            marker = None
        self.setSymbol(marker)
        
        markerSize = STYLE['MarkerSize'] if 'MarkerSize' in STYLE else 10
        self.setSymbolSize(markerSize)

        markerEdgeWidth = STYLE['MarkerEdgeWidth'] if 'MarkerEdgeWidth' in STYLE else lineWidth
        
        markerEdgeColor = STYLE['MarkerEdgeColor'] if 'MarkerEdgeColor' in STYLE else 'auto'
        if markerEdgeColor == 'auto':
            markerEdgeColor = color
        
        symbolPen = pg.mkPen(color=markerEdgeColor, width=markerEdgeWidth)
        self.setSymbolPen(symbolPen)

        markerFaceColor = STYLE['MarkerFaceColor'] if 'MarkerFaceColor' in STYLE else 'auto'
        if markerFaceColor == 'auto':
            markerFaceColor = markerEdgeColor[:3] + (0,)
        
        self.setSymbolBrush(markerFaceColor)
        
        return colorIndex
    
    def editNameDialog(self):
        name = self.name()
        if name is None:
            name = ''
        name, ok = QInputDialog.getText(self.getViewBox().getPlotWidget(), "Trace Name", "Name:", text=name)
        if not ok:
            return
        name = name.strip()
        if name == '':
            name = None
        self.setName(name)
        try:
            self.pyCLAMP.updateTraceNameSelectionList()
        except:
            pass
    
    def editStyleDialog(self):
        STYLE = self.STYLE()
        STYLE = styleDialog(self.getViewBox().getPlotWidget(), STYLE)
        if STYLE is not None:
            self.setSTYLE(STYLE)
    
    def setAsBaselineOfParent(self):
        try:
            parentTRACE = self.pyCLAMP.data.parentTrace(self.TRACE)
            if parentTRACE is not None:
                self.pyCLAMP.data.setTraceBaseline(parentTRACE, self.TRACE['YData'])
                self.pyCLAMP.deleteTrace(self.TRACE)
        except:
            pass
    
    def removeBaseline(self):
        try:
            if '_BaselineOf_' in self.TRACE:
                TRACE = self.TRACE['_BaselineOf_']
            else:
                TRACE = self.TRACE
            self.pyCLAMP.data.deleteTraceBaseline(TRACE)
            self.pyCLAMP.updateChannelPlots()
        except:
            pass
    
    def setXDataToSamples(self):
        try:
            if 'XData' in self.TRACE:
                del self.TRACE['XData']
            self.pyCLAMP.updateChannelPlots()
        except:
            pass


class ROIItem(pg.LinearRegionItem):
    """ pg.LinearRegionItem with context menu for ROI. """

    def __init__(self, *args, **kwargs):
        pg.LinearRegionItem.__init__(self, *args, **kwargs)
        
        # !!! a negative z-value makes right-click context menu not work
        self.setZValue(1)

        self.menu = None
    
    def _delete(self):
        self.getViewBox().removeItem(self)
        self.deleteLater()
    
    def mouseClickEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.boundingRect().contains(event.pos()):
                if self.raiseContextMenu(event):
                    event.accept()
    
    def raiseContextMenu(self, event):
        menu = self.getContextMenus()
        
        # Let the scene add on to the end of our context menu (this is optional)
        # menu.addSection('View')
        # menu = self.scene().addParentContextMenus(self, menu, event)
        
        pos = event.screenPos()
        menu.popup(QPoint(int(pos.x()), int(pos.y())))
        return True
    
    def getContextMenus(self, event=None):
        self.menu = QMenu()
        self.menu.addSection('ROI')
        self.menu.addAction('Edit', self.editDialog)
        self.menu.addSection(' ')
        self.menu.addAction('Hide', lambda: self.setVisible(False))
        self.menu.addSection(' ')
        self.menu.addAction('Delete', self._delete)
        return self.menu
    
    def editDialog(self):
        dlg = QDialog(self.getViewBox().getPlotWidget())
        form = QFormLayout(dlg)

        limits = self.getRegion()
        minEdit = QLineEdit(f'{limits[0]:.6f}')
        maxEdit = QLineEdit(f'{limits[1]:.6f}')
        form.addRow('Min', minEdit)
        form.addRow('Max', maxEdit)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        form.addRow(btns)

        dlg.setWindowModality(Qt.ApplicationModal)
        if dlg.exec_() != QDialog.Accepted:
            return
        
        limits = sorted([float(minEdit.text()), float(maxEdit.text())])
        self.setRegion(limits)


class EventItem(pg.LinearRegionItem):
    """ Immovable pg.LinearRegionItem with default styling, label, and context menu for EVENT. """
    
    def __init__(self, *args, **kwargs):
        pg.LinearRegionItem.__init__(self, orientation='vertical', movable=False, 
            brush=pg.mkBrush(QColor(175, 175, 175, 64)),
            pen=pg.mkPen(QColor(0, 0, 0, 64), width=1),
            *args, **kwargs)
        
        self.lines[0].label = EventInfLineLabel(self.lines[0], text='?', movable=False, position=1, anchors=[(0,0), (0,0)])
        self.lines[0].label.setColor((0, 0, 0, 128))
        self.lines[0].label.eventItem = self  # for context menu
        
        # !!! a negative z-value makes right-click context menu not work
        self.setZValue(0)
        
        self.pyCLAMP = None
        self.EVENT = None
    
    def _delete(self):
        try:
            self.pyCLAMP.data.deleteEvent(self.EVENT)
            self.pyCLAMP.updateUI()
        except:
            self.getViewBox().removeItem(self)
            self.deleteLater()
    
    def setEvent(self, EVENT):
        if EVENT is None:
            self.EVENT = None
            return
        
        # prevents uneeded updates to EVENT dict while setting region and text
        self.EVENT = None

        try:
            xstart = EVENT['XStart']
            xstop = EVENT['XStop'] if 'XStop' in EVENT else xstart
            text = EVENT['Text'] if 'Text' in EVENT else ''
            self.setRegion((xstart, xstop))
            self.setText(text)
        except:
            return
        
        self.EVENT = EVENT
    
    def setRegion(self, region):
        pg.LinearRegionItem.setRegion(self, region)
        try:
            start, stop = region
            self.EVENT['XStart'] = start
            if start == stop:
                if 'XStop' in self.EVENT:
                    del self.EVENT['XStop']
            else:
                self.EVENT['XStop'] = stop
        except:
            pass
    
    def text(self):
        try:
            return self.EVENT['Text']
        except:
            return self.lines[0].label.format

    def setText(self, text):
        try:
            if text is None:
                if 'Text' in self.EVENT:
                    del self.EVENT['Text']
            else:
                self.EVENT['Text'] = text
        except:
            pass
        if text is None or text == '':
            # ensure text is never empty
            # otherwise, label will not be visible and zero-width events cannot be right-clicked
            text = 'event'
        self.lines[0].label.setFormat(text)

    def mouseClickEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.boundingRect().contains(event.pos()):
                if self.raiseContextMenu(event):
                    event.accept()
    
    def raiseContextMenu(self, event):
        menu = self.getContextMenus()
        
        # Let the scene add on to the end of our context menu (this is optional)
        # menu.addSection('View')
        # menu = self.scene().addParentContextMenus(self, menu, event)
        
        pos = event.screenPos()
        menu.popup(QPoint(int(pos.x()), int(pos.y())))
        return True
    
    def getContextMenus(self, event=None):
        self.menu = QMenu()
        self.menu.addSection('Event')
        self.menu.addAction('Edit', self.editDialog)
        self.menu.addSection(' ')
        self.menu.addAction('Delete', self._delete)
        return self.menu
    
    def editDialog(self):
        dlg = QDialog(self.getViewBox().getPlotWidget())
        form = QFormLayout(dlg)

        start, stop = self.getRegion()
        startEdit = QLineEdit(f'{start:.6f}')
        if stop == start:
            stopEdit = QLineEdit()
        else:
            stopEdit = QLineEdit(f'{stop:.6f}')
        form.addRow('XStart', startEdit)
        form.addRow('XStop', stopEdit)

        text = self.text()
        textEdit = QTextEdit()
        if text is not None:
            textEdit.setPlainText(text)
        form.addRow('Text', textEdit)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        form.addRow(btns)

        dlg.setWindowModality(Qt.ApplicationModal)
        if dlg.exec_() != QDialog.Accepted:
            return
        
        start = float(startEdit.text())
        stop = float(stopEdit.text()) if stopEdit.text() != '' else start
        self.setRegion(sorted([start, stop]))

        text = textEdit.toPlainText()
        self.setText(text)


class EventInfLineLabel(pg.InfLineLabel):
    """ pg.InfLineLabel with context menu for EVENT. """

    def __init__(self, *args, **kwargs):
        pg.InfLineLabel.__init__(self, *args, **kwargs)

        self.eventItem = None
    
    def mouseClickEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.eventItem is not None:
                if self.eventItem.raiseContextMenu(event):
                    event.accept()


class ColorButton(QGroupBox):
    def __init__(self, color=QColor('transparent')):
        QGroupBox.__init__(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.colorButton = QPushButton()
        self.colorButton.clicked.connect(self.pickColor)
        self._colorWasPicked = False
        layout.addWidget(self.colorButton)

        self.setColor(color)
    
    def color(self) -> QColor:
        pal = self.colorButton.palette()
        return pal.brush(QPalette.Button).color()

    def setColor(self, color):
        if isinstance(color, str):
            color = str2qcolor(color)
        pal = self.colorButton.palette()
        pal.setBrush(QPalette.Button, QBrush(color))
        self.colorButton.setPalette(pal)
        self.colorButton.setGraphicsEffect(QGraphicsOpacityEffect(opacity=color.alphaF()))
    
    def pickColor(self):
        color = QColorDialog.getColor(self.color(), None, "Select Color", options=QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.setColor(color)
            self._colorWasPicked = True
    
    def colorWasPicked(self) -> bool:
        return self._colorWasPicked
    

def axisLabelsDialog(parentWidget, data):
    dlg = QDialog(parentWidget)
    grid = QGridLayout(dlg)
    # grid.addWidget(QLabel('Axis'), 0, 0)
    grid.addWidget(QLabel('Label'), 0, 1)
    grid.addWidget(QLabel('Unit'), 0, 2)

    xlabel, xunit = data.xlabel()
    xlabelEdit = QLineEdit(xlabel if xlabel is not None else '')
    xunitEdit = QLineEdit(xunit if xunit is not None else '')
    grid.addWidget(QLabel('X-axis'), 1, 0)
    grid.addWidget(xlabelEdit, 1, 1)
    grid.addWidget(xunitEdit, 1, 2)

    ylabelEdits = []
    yunitEdits = []
    nmax_channels = data.numChannels()
    for j in range(nmax_channels):
        ylabel, yunit = data.ylabel(j)
        ylabelEdits.append(QLineEdit(ylabel if ylabel is not None else ''))
        yunitEdits.append(QLineEdit(yunit if yunit is not None else ''))
        grid.addWidget(QLabel(f'Y-axis for Channel {j}'), 2+j, 0)
        grid.addWidget(ylabelEdits[j], 2+j, 1)
        grid.addWidget(yunitEdits[j], 2+j, 2)
    
    btns = QDialogButtonBox()
    btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    btns.accepted.connect(dlg.accept)
    btns.rejected.connect(dlg.reject)
    grid.addWidget(btns, grid.rowCount(), 0, 1, grid.columnCount())

    dlg.setWindowModality(Qt.ApplicationModal)
    if dlg.exec_() != QDialog.Accepted:
        return
    
    xlabel = xlabelEdit.text()
    if xlabel == '':
        xlabel = None
    xunit = xunitEdit.text()
    if xunit == '':
        xunit = None
    data.setXLabel(xlabel, xunit)
    for j in range(nmax_channels):
        ylabel = ylabelEdits[j].text()
        if ylabel == '':
            ylabel = None
        yunit = yunitEdits[j].text()
        if yunit == '':
            yunit = None
        data.setYLabel(j, ylabel, yunit)


def styleDialog(parentWidget, STYLE:dict, defaultColor=QColor('transparent')):
    dlg = QDialog(parentWidget)
    form = QFormLayout(dlg)

    lineStyle = STYLE['LineStyle'] if 'LineStyle' in STYLE else '-'
    # Qt.PenStyle.NoPen = 0
    # Qt.PenStyle.SolidLine = 1
    # Qt.PenStyle.DashLine = 2
    # Qt.PenStyle.DotLine = 3
    # Qt.PenStyle.DashDotLine = 4
    lineStyleComboBox = QComboBox()
    lineStyleComboBox.addItems(['No Line', 'Solid Line', 'Dash Line', 'Dot Line', 'Dash Dot Line'])
    lineStyles = ['none', '-', '--', ':', '-.']
    lineStyleComboBox.setCurrentIndex(lineStyles.index(lineStyle))
    form.addRow('Line Style', lineStyleComboBox)

    lineWidth = STYLE['LineWidth'] if 'LineWidth' in STYLE else 1
    lineWidthSpinBox = QDoubleSpinBox()
    lineWidthSpinBox.setMinimum(0)
    lineWidthSpinBox.setValue(lineWidth)
    form.addRow('Line Width', lineWidthSpinBox)

    color = STYLE['Color'] if 'Color' in STYLE else defaultColor
    if color == 'auto':
        color = defaultColor
    color = pg.mkColor(color)  # convert to QColor if needed
    colorButton = ColorButton(color)
    defaultColorButton = QPushButton('Default')
    defaultColorButton.setToolTip('Use current color in colormap')
    defaultColorButton.clicked.connect(lambda: colorButton.setColor(defaultColor))
    colorLayout = QHBoxLayout()
    colorLayout.setContentsMargins(0, 0, 0, 0)
    colorLayout.setSpacing(5)
    colorLayout.addWidget(colorButton)
    colorLayout.addWidget(defaultColorButton)
    form.addRow('Color', colorLayout)

    marker = STYLE['Marker'] if 'Marker' in STYLE else 'none'
    markerComboBox = QComboBox()
    markers = ['none', 'o', 't', 't1', 't2', 't3', 's', 'p', 'h', 'star', '+', 'd', 'x']
    markerComboBox.addItems([
        'None', 'Circle', 'Triangle Down', 'Triangle Up', 'Triangle Right', 'Triangle Left', 'Square', 
        'Pentagon', 'Hexagon', 'Star', 'Plus', 'Prism', 'Cross'])
    markerComboBox.setCurrentIndex(markers.index(marker))
    form.addRow('Marker', markerComboBox)

    markerSize = STYLE['MarkerSize'] if 'MarkerSize' in STYLE else 10
    markerSizeSpinBox = QDoubleSpinBox()
    markerSizeSpinBox.setMinimum(0)
    markerSizeSpinBox.setValue(markerSize)
    form.addRow('Marker Size', markerSizeSpinBox)

    markerEdgeWidth = STYLE['MarkerEdgeWidth'] if 'MarkerEdgeWidth' in STYLE else lineWidth
    markerEdgeWidthSpinBox = QDoubleSpinBox()
    markerEdgeWidthSpinBox.setMinimum(0)
    markerEdgeWidthSpinBox.setValue(markerEdgeWidth)
    form.addRow('Marker Edge Width', markerEdgeWidthSpinBox)

    markerEdgeColor = STYLE['MarkerEdgeColor'] if 'MarkerEdgeColor' in STYLE else defaultColor
    if markerEdgeColor == 'auto':
        markerEdgeColor = defaultColor
    markerEdgeColor = pg.mkColor(markerEdgeColor)  # convert to QColor if needed
    markerEdgeColorButton = ColorButton(markerEdgeColor)
    defaultMarkerEdgeColorButton = QPushButton('Default')
    defaultMarkerEdgeColorButton.setToolTip('Same as color')
    defaultMarkerEdgeColorButton.clicked.connect(lambda: markerEdgeColorButton.setColor(defaultColor))
    markerEdgeColorLayout = QHBoxLayout()
    markerEdgeColorLayout.setContentsMargins(0, 0, 0, 0)
    markerEdgeColorLayout.setSpacing(5)
    markerEdgeColorLayout.addWidget(markerEdgeColorButton)
    markerEdgeColorLayout.addWidget(defaultMarkerEdgeColorButton)
    form.addRow('Marker Edge Color', markerEdgeColorLayout)

    markerFaceColor = STYLE['MarkerFaceColor'] if 'MarkerFaceColor' in STYLE else defaultColor
    if markerFaceColor == 'auto':
        markerFaceColor = defaultColor
    markerFaceColor = pg.mkColor(markerFaceColor)  # convert to QColor if needed
    markerFaceColorButton = ColorButton(markerFaceColor)
    defaultMarkerFaceColorButton = QPushButton('Default')
    defaultMarkerFaceColorButton.setToolTip('Transparent')
    defaultMarkerFaceColorButton.clicked.connect(lambda: markerFaceColorButton.setColor(defaultColor))
    markerFaceColorLayout = QHBoxLayout()
    markerFaceColorLayout.setContentsMargins(0, 0, 0, 0)
    markerFaceColorLayout.setSpacing(5)
    markerFaceColorLayout.addWidget(markerFaceColorButton)
    markerFaceColorLayout.addWidget(defaultMarkerFaceColorButton)
    form.addRow('Marker Face Color', markerFaceColorLayout)

    btns = QDialogButtonBox()
    btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    btns.accepted.connect(dlg.accept)
    btns.rejected.connect(dlg.reject)
    form.addRow(btns)

    dlg.setWindowModality(Qt.ApplicationModal)
    if dlg.exec_() != QDialog.Accepted:
        return None
    
    # update STYLE from dialog
    STYLE['LineStyle'] = lineStyles[lineStyleComboBox.currentIndex()]
    STYLE['LineWidth'] = lineWidthSpinBox.value()

    color = colorButton.color()
    if color == defaultColor:
        STYLE['Color'] = 'auto'
    else:
        STYLE['Color'] = color.red(), color.green(), color.blue(), color.alpha()
    
    STYLE['Marker'] = markers[markerComboBox.currentIndex()]
    STYLE['MarkerSize'] = markerSizeSpinBox.value()
    STYLE['MarkerEdgeWidth'] = markerEdgeWidthSpinBox.value()

    markerEdgeColor = markerEdgeColorButton.color()
    if markerEdgeColor == defaultColor:
        STYLE['MarkerEdgeColor'] = 'auto'
    else:
        STYLE['MarkerEdgeColor'] = markerEdgeColor.red(), markerEdgeColor.green(), markerEdgeColor.blue(), markerEdgeColor.alpha()

    markerFaceColor = markerFaceColorButton.color()
    if markerFaceColor == defaultColor:
        STYLE['MarkerFaceColor'] = 'auto'
    else:
        STYLE['MarkerFaceColor'] = markerFaceColor.red(), markerFaceColor.green(), markerFaceColor.blue(), markerFaceColor.alpha()

    return STYLE


if __name__ == '__main__':
    # Create the application
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')

    # Create widget
    ui = newPyClampWindow()

    # ui.data.DATA = ui.data.formatData(x=None, y=np.random.random((5,2,100)))
    # ui.data.DATA['Episodes'][0]['Channels'][0]['Traces'][0]['Name'] = 'test'
    # ui.data.DATA['Episodes'][0]['Channels'][0]['Traces'][0]['YZero'] = 0.5
    # ui.data.DATA['Episodes'][0]['Channels'][0]['Events'] = [
    #     {
    #         'Type': 'Event',
    #         'Group': 'group',
    #         'XStart': 50,
    #         'XStop': 60,
    #         'Text': 'event 1'
    #     },
    #     {
    #         'Type': 'Event',
    #         'Group': 'group',
    #         'XStart': 20,
    #         'Text': 'event 2'
    #     }
    # ]
    # ui.data.refreshParents()

    # ui.dump('DATA.txt')

    # Show widget and run application
    ui.show()
    ui.updateUI()
    status = app.exec()
    sys.exit(status)