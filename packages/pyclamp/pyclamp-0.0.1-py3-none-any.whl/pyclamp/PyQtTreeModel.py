"""
PyQt tree model for an arbitrary heirarchy of nested dicts and lists of dicts.

Each row of the tree corresponds to a dict or a list of dicts.

The first column of the tree corresponds to the key associated with the dict or list of dicts in the parent dict or list.
All other columns of the tree correspond to a user specified key for which values in dicts should be displayed.
!!! Only values associated with the specified keys are displayed in the tree.

!!! Only dicts and lists of dicts are treated as tree nodes that can be expanded/collapsed.
!!! Lists of values other than dicts are displayed in a single (row,column) cell.

!!! If a dict key is one of the specified column keys, then its value is always displayed in the corresponding column cell
    and no further recursion of tree nodes is attempted regardless of whether or not the value is a dict or a list of dicts.

Numpy arrays are displayed with a string representation of their shape and dtype similar to that in MATLAB.
"""


__author__ = "Marcel P. Goldschen-Ohm"
__author_email__ = "goldschen-ohm@utexas.edu, marcel.goldschen@gmail.com"


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np


class TreeNode():
    """ Each node corresponds to either a dict or a list of dicts.
    
        Only dicts are treated as objects with data to be displayed in the columns.
        The columns are associated with specified dict keys.
        !!! Lists of values other than dicts are displayed in a single (row,column) cell.
    """

    def __init__(self, key, value, columnKeys, parent=None):
        self.key = key  # key associated with value in parent dict OR index of value in parent list of dicts
        self.value = value  # !!! must be either a dict OR a list of dicts
        self.columnKeys = columnKeys  # dict keys whose associated values are to be displayed in the columns
        self.parent = parent  # parent node
        self.children = []  # child nodes

        if isinstance(value, dict):
            for childKey, childValue in value.items():
                if isinstance(childValue, dict) or self.isListOfDicts(childValue):
                    if childKey not in columnKeys:
                        child = TreeNode(childKey, childValue, columnKeys, self)
                        self.children.append(child)
        elif self.isListOfDicts(value):
            for childKey, childValue in enumerate(value):
                if isinstance(childValue, dict) or self.isListOfDicts(childValue):
                    child = TreeNode(childKey, childValue, columnKeys, self)
                    self.children.append(child)
        
    def isListOfDicts(self, alist:list):
        if not isinstance(alist, list):
            return False
        return len(alist) == 0 or isinstance(alist[0], dict)
    
    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0
        
    def columnCount(self):
        return 1 + len(self.columnKeys)

    def data(self, column:int):
        if not self.parent:
            # root
            if column == 0:
                return None
            if 1 <= column <= len(self.columnKeys):
                return self.columnKeys[column-1]
            return None
        if column == 0:
            return self.key
        if not isinstance(self.value, dict):
            return None
        if 1 <= column <= len(self.columnKeys):
            key = self.columnKeys[column-1]
            try:
                return self.value[key]
            except KeyError:
                return None
        return None
    
    def depth(self):
        depth = 0
        node = self
        while node.parent:
            depth += 1
            node = node.parent
        return depth
    
    def __str__(self):
        indent = '  '
        firstColumnWidth = 42  # this column contains all of the tree level nesting indents
        columnWidth = 15  # these are the data columns
        text = indent * self.depth()
        for column in range(self.columnCount()):
            if column == 0:
                if self.parent is None:
                    text += 'root'
                else:
                    text += str(self.key)
                if len(text) > firstColumnWidth:
                    text = text[:firstColumnWidth-3] + '...'
                elif len(text) < firstColumnWidth: 
                    text += ' ' * (firstColumnWidth - len(text))
                continue
            if self.parent is None:
                data = self.columnKeys[column-1]
            else:
                data = self.data(column)
            if column == 1:
                text += '[ '
            elif column > 1:
                text += '\t'
            if data is None:
                dataStr = ''
            elif isinstance(data, np.ndarray):
                dataStr = numpyStrRepr(data)
            else:
                dataStr = str(data)
            if len(dataStr) > columnWidth:
                dataStr = dataStr[:columnWidth-3] + '...'
            elif len(dataStr) < columnWidth:
                dataStr += ' '*(columnWidth - len(dataStr))
            text += dataStr
            if column == self.columnCount() - 1:
                text += ' ]'
        return text
    
    def dump(self):
        print(str(self))
        for child in self.children:
            child.dump()


class TreeModel(QAbstractItemModel):
    def __init__(self, data, columns, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self.rootNode = TreeNode(None, data, columns)
        self.columns = [''] + columns
    
    def rowCount(self, parentIndex):
        if parentIndex.column() > 0:
            return 0
        if not parentIndex.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parentIndex.internalPointer()
        return len(parentNode.children)
    
    def columnCount(self, parentIndex=None):
        if parentIndex is not None and parentIndex.isValid():
            parentNode = parentIndex.internalPointer()
            return parentNode.columnCount()
        return self.rootNode.columnCount()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()
            
        if not parentIndex.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parentIndex.internalPointer()
        
        node = parentNode.children[row]
        return self.createIndex(row, column, node)
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        
        node = index.internalPointer()
        parentNode = node.parent

        if parentNode is self.rootNode:
            return QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role not in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return None

        node = index.internalPointer()

        value = node.data(index.column())

        if value is None:
            return None
        elif isinstance(value, np.ndarray):
            return numpyStrRepr(value)
        return str(value)
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.rootNode.data(section)


def numpyStrRepr(array):
    if array.ndim == 1:
        return f'x{array.size} {array.dtype}'
    return 'x'.join([str(s) for s in array.shape]) + f' {array.dtype}'


if __name__ == '__main__':
    # Create the application
    import sys
    app = QApplication(sys.argv)

    Company = {
        'Region': {
            'Europe': {
                'Department': {
                    'Research': {
                        'Team': [
                            {
                                'Name': 'Bob',
                                'Data': np.random.random((3,100))
                            },
                            {
                                'Name': 'Susan',
                                'Data': [1, 3, 7, 'a', 'b', True]
                            },
                            {
                                'Name': 'Meredith',
                                'Data': 'facts only please'
                            }
                        ]
                    }
                }
            },
            'Asia': {
                'Department': {
                    'Marketing': {
                        'Team': [
                            {
                                'Name': 'Alice',
                                'Data': {'a': 1, 'b': 2, 'c': 'three'}
                            },
                            {
                                'Name': 'Sam',
                                'Data': 8.2
                            },
                            {
                                'Name': 'Mike',
                                'Data': {
                                    'Name': "Mike's helper",
                                    'Data': "They're great!"
                                }
                            }
                        ]
                    }
                }
            }
        }
    }

    # rootNode = TreeNode(None, Company, ['Name', 'Data'])
    # rootNode.dump()

    model = TreeModel(Company, ['Name', 'Data'])

    view = QTreeView()
    view.setModel(model)
    view.expandRecursively(QModelIndex(), -1)
    for column in range(model.columnCount()):
        view.resizeColumnToContents(column)
    view.show()

    # run application
    status = app.exec()
    sys.exit(status)