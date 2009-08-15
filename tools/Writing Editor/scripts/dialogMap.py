#!/usr/bin/python

#   This file is part of PARPG.

#   PARPG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   PARPG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui, QtCore
from scripts.parser import Parser

class DialogMap(QtGui.QTreeWidget):
    """
    The dialog map which will show the flow of the dialog
    """
    def __init__(self, settings, main_edit, parent):
        """
        Initialize the dialog map
        @type settings: settings.Settings
        @param settings: the settings for the editor
        @type main_edit: QtGui.QTextEdit
        @param main_edit: The main text editor
        @type parent: Any Qt widget
        @param parent: The widgets' parent
        @return: None
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.settings = settings
        self.parent = parent
        self.resize(int(self.settings.res_width), int(self.settings.res_height))
        self.parser = Parser(main_edit.document())

        self.setColumnCount(1)
        self.setEditTriggers(self.NoEditTriggers)
        self.model = QtGui.QTreeWidgetItem()
        self.items = []
        for i in xrange(10):
            item = QtGui.QTreeWidgetItem()
            item.setText(0, str(i))
            item2 = QtGui.QTreeWidgetItem()
            item2.setText(0, str(i + 1))
            item.addChild(item2)
            self.items.append(item)
        self.insertTopLevelItems(0, self.items)
        self.setHeaderLabel("Dialog Map")
