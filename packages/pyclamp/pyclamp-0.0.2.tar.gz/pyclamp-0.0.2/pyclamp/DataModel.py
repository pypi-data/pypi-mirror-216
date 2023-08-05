"""
Data model for pyCLAMP.

Data structure:
---------------
- Data is stored as nested dictionaries or lists of dictionaries for maximum flexiblity and extensibility.
    - Need new functionality? Just add a new key at whichever level of the heirarchy is appropriate.
    - The data is entirely composed only of dict, list, str, int, float, and numpy ndarray values 
      and thus can be easily serialized to JSON, MAT, etc.
    - The data is entirely self-describing and can be easily explored and manipulated independent of the UI 
      or any other code in this module.
- Traces are organized heirarchically by episode, channel, trace which should cover most experimental recording paradigms.
    - EPISODE: A single recording sweep.
        - CHANNEL: A single recorded signal (e.g., current, voltage, etc.).
            - TRACE: A single data trace.
                - Overlay TRACE: A single data trace associated with a parent trace (e.g., fit, measurement, etc.).
            - EVENT: A labeled x-axis interval.
- For memory efficiency any data arrays that are shared amongst traces (e.g., XData) 
  should all be references/views to the same shared array.
  These should generally be numpy ndarrays.
- In most cases each (EPISODE,CHANNEL) pair will have only a single TRACE 
  and all fits, etc. will be handled with overlaid child traces.
  Multiple TRACEs per (EPISODE,CHANNEL) pair are for things like triggered recordings of variable segments within each sweep.

DATA['Episodes'][i]['Channels'][j]['Traces'][k] = TRACE
DATA['Episodes'][i]['Channels'][j]['Traces'][k]['Traces'][l] = overlay TRACE
DATA['Episodes'][i]['Channels'][j]['Events'][k] = EVENT

DATA = {
    'Type': 'Data'
    'Episodes': [EPISODE, ...]
    'Notes': notes
}

EPISODE = {
    'Type': 'Episode'
    'Channels': [CHANNEL, ...]
}

CHANNEL = {
    'Type': 'Channel'
    'Traces': [TRACE, ...]
    'Events': [EVENT, ...]
}

TRACE = {
    'Type': 'Trace'
    'Name': trace label (defaults to 'Data')
    'XData': ndarray[sample] OR sample interval (defaults to sample indexes)
    'YData': ndarray[sample]
    'XLabel': x-axis label
    'YLabel': y-axis label
    'XUnit': x-axis unit
    'YUnit': y-axis unit
    'XZero': x-axis offset: XData -> XData - XZero
    'YZero': baseline ndarray[sample] OR y-axis offset: YData -> YData - YZero
    'Mask': logical mask: YData -> YData[Mask]
    'Style': STYLE
    'Traces': [TRACE, ...] <- overlay traces associated with this trace (e.g., fit, measurement, etc.)
}

EVENT = {
    'Type': 'Event'
    'Group': event group label (defaults to 0)
    'XStart': x-axis event start
    'XStop': x-axis event stop (defaults to XStart)
    'Text': event info
}

STYLE = {
    'Type': 'Style'
    'Color': (r, g, b) or (r, g, b, a) in 0-255 or 'auto' (defaults to 'auto' => based on colormap)
    'LineStyle': one of ['none', '-', '--', ':', '-.'] (defaults to '-')
    'LineWidth': (defaults to 1)
    'Marker': one of ['none', 'o', 't', 't1', 't2', 't3', 's', 'p', 'h', 'star', '+', 'd', 'x'] (defaults to 'none')
    'MarkerSize': (defaults to 10)
    'MarkerEdgeWidth': (defaults to linewidth)
    'MarkerEdgeColor': (r, g, b) or (r, g, b, a) in 0-255 or 'auto' (defaults to 'auto' => Color)
    'MarkerFaceColor': (r, g, b) or (r, g, b, a) in 0-255 or 'auto' (defaults to 'auto' => MarkerEdgeColor with alpha=0)
}

References from child to parent dict objects are stored separately from the data structure itself.
These are very useful for manipulating the data structure, 
    but are not required and can be derived from the data structure as needed.
Were they to be included in the data structure itself, 
    then they would prevent simple serialization to JSON, MAT, etc.
!!! It is up to you to insure that these references are up-to-date 
    (DataModel.refreshParents() will refresh them if you are not sure).

PARENTS = [(CHILD, PARENT), ...]
"""


__author__ = "Marcel P. Goldschen-Ohm"
__author_email__ = "goldschen-ohm@utexas.edu, marcel.goldschen@gmail.com"


import json
import numpy as np
import scipy as sp


class DataModel():

    def __init__(self, DATA=None):
        if DATA is None:
            DATA = {
                'Type': 'Data',
                'Episodes': [],
                'Notes': ''
            }
        self.setData(DATA)
    
    def setData(self, DATA):
        self.DATA = DATA
        self.refreshParents()

    def refreshParents(self, parent:dict=None):
        """ Refresh the PARENTS dict of child: parent relations. """
        if parent is None:
            parent = self.DATA
            self.PARENTS = [(self.DATA, None)]
        for child in parent.values():
            if isinstance(child, dict):
                self.PARENTS.append((child, parent))
                self.refreshParents(child)
            elif isinstance(child, list):
                children = child
                for child in children:
                    if isinstance(child, dict):
                        self.PARENTS.append((child, parent))
                        self.refreshParents(child)
    
    def parent(self, CHILD):
        try:
            children, parents = list(zip(*self.PARENTS))
            i = children.index(CHILD)
            if i >= 0:
                return parents[i]
            return None
        except:
            return None
    
    def contains(self, OBJ:dict):
        children, parents = list(zip(*self.PARENTS))
        return OBJ in children
    
    def numEpisodes(self):
        """ Return the number of episodes in DATA. """
        if 'Episodes' in self.DATA:
            return len(self.DATA['Episodes'])
        return 0
    
    def numChannels(self, episodeIndexes=None):
        """ Return the (maximum) number of channels in the specified (defaults to all) episodes. """
        nmax_channels = 0
        if 'Episodes' in self.DATA:
            for i, EPISODE in enumerate(self.DATA['Episodes']):
                if episodeIndexes is None or i in episodeIndexes:
                    if 'Channels' in EPISODE:
                        nmax_channels = max(nmax_channels, len(EPISODE['Channels']))
        return nmax_channels
    
    def numTraces(self, episodeIndexes=None, channelIndexes=None):
        """ Return the (maximum) number of traces in the specified (defaults to all) episodes and channels. """
        nmax_traces = 0
        if 'Episodes' in self.DATA:
            for i, EPISODE in enumerate(self.DATA['Episodes']):
                if episodeIndexes is None or i in episodeIndexes:
                    if 'Channels' in EPISODE:
                        for j, CHANNEL in enumerate(EPISODE['Channels']):
                            if channelIndexes is None or j in channelIndexes:
                                if 'Traces' in CHANNEL:
                                    nmax_traces = max(nmax_traces, len(CHANNEL['Traces']))
        return nmax_traces
    
    def traces(self, episodeIndexes=None, channelIndexes=None, traceIndexes=None, traceNames=None, 
                     includeChildTraces=True, includeBaselineTraces=False):
        """ Return a flat list of TRACE dicts. """
        traces = []
        if 'Episodes' in self.DATA:
            for i, EPISODE in enumerate(self.DATA['Episodes']):
                if episodeIndexes is None or i in episodeIndexes:
                    if 'Channels' in EPISODE:
                        for j, CHANNEL in enumerate(EPISODE['Channels']):
                            if channelIndexes is None or j in channelIndexes:
                                if 'Traces' in CHANNEL:
                                    for k, TRACE in enumerate(CHANNEL['Traces']):
                                        if traceIndexes is None or k in traceIndexes:
                                            name = TRACE['Name'] if 'Name' in TRACE else 'Data'
                                            if traceNames is None or name in traceNames:
                                                traces.append(TRACE)
                                                if includeBaselineTraces:
                                                    BASELINE_TRACE = self.makeBaselineTrace(TRACE)
                                                    if BASELINE_TRACE is not None:
                                                        traces.append(BASELINE_TRACE)
                                            if includeChildTraces:
                                                for CHILD_TRACE in self.childTraces(TRACE):
                                                    name = CHILD_TRACE['Name'] if 'Name' in CHILD_TRACE else 'Data'
                                                    if traceNames is None or name in traceNames:
                                                        traces.append(CHILD_TRACE)
        return traces
    
    def childTraces(self, TRACE, depth=0, maxDepth=np.inf):
        """ Return a flat list of TRACE dicts for traces descended from TRACE. """
        traces = TRACE['Traces'] if 'Traces' in TRACE else []
        if depth < maxDepth:
            for CHILD_TRACE in traces:
                traces.extend(self.childTraces(CHILD_TRACE, depth + 1, maxDepth))
        return traces
    
    def parentTrace(self, TRACE):
        PARENT = self.parent(TRACE)
        if PARENT is None or PARENT['Type'] != 'Trace':
            return None
        return PARENT
    
    def addTrace(self, episodeIndex, channelIndex, TRACE):
        if 'Episodes' not in self.DATA:
            self.DATA['Episodes'] = []
        while len(self.DATA['Episodes']) <= episodeIndex:
            self.DATA['Episodes'].append({
                'Type': 'Episode',
                'Channels': []
            })
        EPISODE = self.DATA['Episodes'][episodeIndex]
        while len(EPISODE['Channels']) <= channelIndex:
            EPISODE['Channels'].append({
                'Type': 'Channel',
                'Traces': [],
                'Events': []
            })
        CHANNEL = EPISODE['Channels'][channelIndex]
        if 'Traces' not in CHANNEL:
            CHANNEL['Traces'] = []
        CHANNEL['Traces'].append(TRACE)
        self.refreshParents()
    
    def makeBaselineTrace(self, TRACE):
        """ Return a TRACE dict for TRACE's YZero baseline (this dict is not in the data structure). """
        if 'YZero' not in TRACE:
            return None
        yzero = TRACE['YZero']
        npts = len(TRACE['YData'])
        if type(yzero) in [float, int] and npts > 1:
            yzero = np.full(npts, yzero)
        BASELINE_TRACE = {
            'Name': 'Baseline',
            'YData': yzero,
            'YZero': TRACE['YZero'], # if baseline is applied this will zero this trace
            'Style': {
                'Color': (0, 0, 0, 255),
                'LineStyle': '--'
            },
            '_BaselineOf_': TRACE  # ok because this trace is not part of DATA
        }
        if 'XData' in TRACE:
            BASELINE_TRACE['XData'] = TRACE['XData']
        return BASELINE_TRACE
    
    def traceData(self, TRACE:dict, applyXZero=True, applyYZero=False):
        xdata = TRACE['XData'] if 'XData' in TRACE else None
        ydata = TRACE['YData']
        xzero = TRACE['XZero'] if 'XZero' in TRACE else None
        yzero = TRACE['YZero'] if 'YZero' in TRACE else None
        
        if xdata is None:
            xdata = np.arange(len(ydata))
        elif type(xdata) in [float, int]:
            xdata = np.arange(len(ydata)) * xdata
        
        if not isinstance(ydata, np.ndarray):
            ydata = np.array([ydata])
        
        if xzero is not None and applyXZero:
            xdata = xdata - xzero
        
        if yzero is not None and applyYZero:
            ydata = ydata - yzero
        
        return xdata, ydata, xzero, yzero
    
    def setTraceBaseline(self, TRACE, yzero):
        TRACE['YZero'] = yzero
        for CHILD_TRACE in self.childTraces(TRACE):
            setTraceBaseline(CHILD_TRACE, yzero)
    
    def deleteTraceBaseline(self, TRACE):
        if 'YZero' in TRACE:
            del TRACE['YZero']
        for CHILD_TRACE in self.childTraces(TRACE):
            deleteTraceBaseline(CHILD_TRACE)
    
    def channelNames(self, episodeIndexes=None):
        """ Return a list of channel names. """
        nmax_channels = self.numChannels(episodeIndexes)
        names = [None] * nmax_channels
        if 'Episodes' in self.DATA:
            for i, EPISODE in enumerate(self.DATA['Episodes']):
                if episodeIndexes is None or i in episodeIndexes:
                    if 'Channels' in EPISODE:
                        for j, CHANNEL in enumerate(EPISODE['Channels']):
                            if names[j] is None:
                                if 'Name' in CHANNEL:
                                    names[j] = CHANNEL['Name']
                                elif 'Traces' in CHANNEL:
                                    for TRACE in CHANNEL['Traces']:
                                        if 'YLabel' in TRACE:
                                            names[j] = TRACE['YLabel']
                                            continue
        return names
    
    def traceNames(self, episodeIndexes=None, channelIndexes=None, traceIndexes=None, 
                   traceNames=None, includeChildTraces=True):
        traces = self.traces(episodeIndexes, channelIndexes, traceIndexes, traceNames, 
                             includeChildTraces, includeBaselineTraces=False)
        names = []
        for TRACE in traces:
            name = TRACE['Name'] if 'Name' in TRACE else 'Data'
            if name not in names:
                names.append(name)
        return names
    
    def events(self, episodeIndexes=None, channelIndexes=None, eventGroups=None):
        events = []
        if 'Episodes' in self.DATA:
            for i, EPISODE in enumerate(self.DATA['Episodes']):
                if episodeIndexes is None or i in episodeIndexes:
                    if 'Channels' in EPISODE:
                        for j, CHANNEL in enumerate(EPISODE['Channels']):
                            if channelIndexes is None or j in channelIndexes:
                                if 'Events' in CHANNEL:
                                    for k, EVENT in enumerate(CHANNEL['Events']):
                                        group = EVENT['Group'] if 'Group' in EVENT else 0
                                        if eventGroups is None or group in eventGroups:
                                            events.append(EVENT)
        return events
    
    def deleteEpisode(self, episodeIndex):
        del self.DATA['Episodes'][episodeIndex]
        self.refreshParents()

    def deleteChannel(self, channelIndex):
        for EPISODE in self.DATA['Episodes']:
            del EPISODE['Channels'][channelIndex]
        self.refreshParents()

    def deleteTrace(self, traceIndexOrDict):
        if isinstance(traceIndexOrDict, int):
            traceIndex = traceIndexOrDict
            for EPISODE in DATA['Episodes']:
                for CHANNEL in EPISODE['Channels']:
                    del CHANNEL['Traces'][traceIndex]
        elif isinstance(traceIndexOrDict, dict):
            TRACE = traceIndexOrDict
            PARENT = self.parent(TRACE)
            PARENT['Traces'].remove(TRACE)
        self.refreshParents()
    
    def deleteEvent(self, EVENT):
        PARENT = self.parent(EVENT)
        PARENT['Events'].remove(EVENT)
        self.refreshParents()
    
    def xlabel(self):
        traces = self.traces()
        for TRACE in traces:
            if 'XLabel' in TRACE:
                xlabel = TRACE['XLabel']
                xunit = TRACE['XUnit'] if 'XUnit' in TRACE else None
                return xlabel, xunit
        return None, None

    def ylabel(self, channelIndex):
        traces = self.traces(channelIndexes=[channelIndex])
        for TRACE in traces:
            if 'YLabel' in TRACE:
                ylabel = TRACE['YLabel']
                yunit = TRACE['YUnit'] if 'YUnit' in TRACE else None
                return ylabel, yunit
        return None, None

    def setXLabel(self, xlabel, xunit=None):
        traces = self.traces()
        for TRACE in traces:
            if xlabel is None:
                if 'XLabel' in TRACE:
                    del TRACE['XLabel']
            else:
                TRACE['XLabel'] = xlabel
            if xunit is None:
                if 'XUnit' in TRACE:
                    del TRACE['XUnit']
            else:
                TRACE['XUnit'] = xunit

    def setYLabel(self, channelIndex, ylabel, yunit=None):
        traces = self.traces(channelIndexes=[channelIndex])
        for TRACE in traces:
            if ylabel is None:
                if 'YLabel' in TRACE:
                    del TRACE['YLabel']
            else:
                TRACE['YLabel'] = ylabel
            if yunit is None:
                if 'YUnit' in TRACE:
                    del TRACE['YUnit']
            else:
                TRACE['YUnit'] = yunit
    
    def notes(self):
        if 'Notes' in self.DATA:
            return self.DATA['Notes']
        return ''
    
    def setNotes(self, notes):
        self.DATA['Notes'] = notes
    
    def savemat(self, filepath):
        sp.io.savemat(filepath, {'DATA': self.DATA})

    def loadmat(self, filepath):
        DATA = sp.io.loadmat(filepath, simplify_cells=True)
        self.DATA = DATA['DATA']
        
        # Remove special keys added by loadmat.
        keys = tuple(self.DATA.keys())
        for key in keys:
            if key.startswith('__'):
                del self.DATA[key]
        
        # Ensure lists of dicts for episodes, channels, and traces.
        # This is needed because simplify_cells collapses a list of a single dict to a dict.
        if 'Episodes' in self.DATA:
            if isinstance(self.DATA['Episodes'], dict):
                self.DATA['Episodes'] = [self.DATA['Episodes']]
            for EPISODE in self.DATA['Episodes']:
                if 'Channels' in EPISODE:
                    if isinstance(EPISODE['Channels'], dict):
                        EPISODE['Channels'] = [EPISODE['Channels']]
                    for CHANNEL in EPISODE['Channels']:
                        if 'Traces' in CHANNEL:
                            if isinstance(CHANNEL['Traces'], dict):
                                CHANNEL['Traces'] = [CHANNEL['Traces']]
                            for TRACE in CHANNEL['Traces']:
                                self._ensureChildTracesAreListOfDicts(TRACE)

    def _ensureChildTracesAreListOfDicts(self, TRACE):
        if 'Traces' in TRACE:
            if isinstance(TRACE['Traces'], dict):
                TRACE['Traces'] = [TRACE['Traces']]
            for CHILD_TRACE in TRACE['Traces']:
                self._ensureChildTracesAreListOfDicts(CHILD_TRACE)
    
    def JSON(self, obj=None):
        """ Return data structure with root at obj with all numpy ndarrays converted to their string repr.
        
            i.e., For pretty printing: json.dumps(self.getJSON(), indent=2)
        """
        if obj is None:
            obj = self.DATA
        if isinstance(obj, dict):
            JSON = {}
            for key in obj:
                JSON[key] = self.JSON(obj[key])
            return JSON
        elif isinstance(obj, list):
            return [self.JSON(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return numpyStrRepr(obj)
        else:
            return obj

    def dump(self, filepath=None, indent=2):
        pretty = json.dumps(self.JSON(), indent=indent)
        if filepath is None:
            print(pretty)
        else:
            with open(filepath, 'w') as dumpFile:
                print(pretty, file=dumpFile)
    
    def formatData(self, x, y):
        # x: ndarray[sample] or sample interval or None (sample indexes)
        #    or iterable thereof indexable as [episode], [episode][channel], or [episode][channel][trace]
        # y: ndarray[sample]
        #    or iterable thereof indexable as [episode], [episode][channel], or [episode][channel][trace]
        # returns (x,y) in DATA format
        xErrorMsg = '''x must be ndarray[sample] or sample interval or None (sample indexes) 
        or iterable thereof indexable as [episode], [episode][channel], or [episode][channel][trace]'''
        yErrorMsg = '''y must be ndarray[sample] 
        or iterable thereof indexable as [episode], [episode][channel], or [episode][channel][trace]'''
        if isinstance(y, np.ndarray):
            if not (1 <= y.ndim <= 4):
                raise ValueError(yErrorMsg)
            if y.ndim == 1:
                # [sample] -> [episode][channel][trace][sample]
                y = y.reshape((1, 1, 1, -1))
            elif y.ndim == 2:
                # [episode][sample] -> [episode][channel][trace][sample]
                y = y.reshape((y.shape[0], 1, 1, -1))
            elif y.ndim == 3:
                # [episode][channel][sample] -> [episode][channel][trace][sample]
                y = y.reshape((y.shape[0], y.shape[1], 1, -1))
        DATA = {
            'Type': 'Data',
            'Episodes': [],
            'Notes': ''
        }
        n_episodes = len(y)
        for i in range(n_episodes):
            if isinstance(y[i], np.ndarray):
                if not (1 <= y[i].ndim <= 3):
                    raise ValueError(yErrorMsg)
                if y[i].ndim == 1:
                    # [sample] -> [channel][trace][sample]
                    y[i] = y[i].reshape((1, 1, -1))
                elif y[i].ndim == 2:
                    # [channel][sample] -> [channel][trace][sample]
                    y[i] = y[i].reshape((y[i].shape[0], 1, -1))
            EPISODE = {
                'Type': 'Episode',
                'Channels': []
                }
            n_channels = len(y[i])
            for j in range(n_channels):
                if isinstance(y[i][j], np.ndarray):
                    if not (1 <= y[i][j].ndim <= 2):
                        raise ValueError(yErrorMsg)
                    if y[i][j].ndim == 1:
                        # [sample] -> [trace][sample]
                        y[i][j] = y[i][j].reshape((1, -1))
                CHANNEL = {
                    'Type': 'Channel',
                    'Traces': [],
                    'Events': []
                }
                n_traces = len(y[i][j])
                for k in range(n_traces):
                    if not isinstance(y[i][j][k], np.ndarray):
                        y[i][j][k] = np.array(y[i][j][k])
                    if y[i][j][k].ndim != 1 or y[i][j][k].dtype not in [float, int]:
                        raise ValueError(yErrorMsg)
                    TRACE = {
                        'Type': 'Trace'
                    }
                    if x is not None:
                        if type(x) in [float, int] or (isinstance(x, np.ndarray) and x.ndim == 1):
                            TRACE['XData'] = x
                        elif type(x[i]) in [float, int] or (isinstance(x[i], np.ndarray) and x[i].ndim == 1):
                            if not (len(x) == n_episodes):
                                raise ValueError(xErrorMsg)
                            TRACE['XData'] = x[i]
                        elif type(x[i][j]) in [float, int] or (isinstance(x[i][j], np.ndarray) and x[i][j].ndim == 1):
                            if not (len(x) == n_episodes) or not (len(x[i]) == n_channels):
                                raise ValueError(xErrorMsg)
                            TRACE['XData'] = x[i][j]
                        elif type(x[j][j][k]) in [float, int] or (isinstance(x[i][j][k], np.ndarray) and x[i][j][k].ndim == 1):
                            if not (len(x) == n_episodes) or not (len(x[i]) == n_channels) or not (len(x[i][j]) == n_traces):
                                raise ValueError(xErrorMsg)
                            TRACE['XData'] = x[i][j][k]
                        else:
                            raise ValueError(xErrorMsg)
                        if (type(TRACE['XData']) not in [float, int]) and (len(TRACE['XData']) != len(y[i][j][k])):
                            raise ValueError('x vs. y array length mismatch')
                    TRACE['YData'] = y[i][j][k]
                    CHANNEL['Traces'].append(TRACE)
                EPISODE['Channels'].append(CHANNEL)
            DATA['Episodes'].append(EPISODE)
        return DATA


def numpyStrRepr(array):
    if array.ndim == 1:
        return f'x{array.size} {array.dtype}'
    return 'x'.join([str(s) for s in array.shape]) + f' {array.dtype}'


if __name__ == '__main__':
    dataModel = DataModel()
    dataModel.DATA = dataModel.formatData(x=None, y=np.random.random((3,2,5)))
    dataModel.DATA['Episodes'][0]['Channels'][0]['Traces'][0]['Traces'] = [
        {'Type': 'Trace', 'Name': 'Measure', 'YData': np.random.random(5)},
        {'Type': 'Trace', 'Name': 'Fit', 'YData': np.random.random(5)},
    ]
    dataModel.dump()