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

class AboutWindow(QtGui.QMainWindow):
    """
    The about window
    """
    def __init__(self, parent=None):
        """
        Initialize the windows
        """
        QtGui.QWidget.__init__(self, parent)
        self.setObjectName("aboutWindow")
        self.setWindowTitle("About")
        self.setWindowIcon(QtGui.QIcon("data/images/about.png"))
        self.resize(225,245)
        self.central_widget = QtGui.QWidget(self)
        self.central_widget.setGeometry(QtCore.QRect(0,0,225,245))

        self.info_icon = QtGui.QLabel(self.central_widget)
        self.info_icon.setPixmap(QtGui.QPixmap("data/images/about_large.png")) 
        self.info_icon.setGeometry(QtCore.QRect(48,1,128,128))

        self.credits_text = QtGui.QLabel(self.central_widget)
        ctext = "PARPG Writing Editor written by: Brett Patterson A.K.A Bretzel\n"\
            "Written using the PyQt4 library\n"\
            "Copyright 2009"
        self.credits_text.setText(QtCore.QString(ctext))
        self.credits_text.setWordWrap(True)
        self.credits_text.setGeometry(QtCore.QRect(3,65,225,220))

        self.close_button = QtGui.QPushButton(self.central_widget)
        self.close_button.setText("Close")
        self.close_button.setGeometry(QtCore.QRect(75,215,65,25))

        QtCore.QObject.connect(self.close_button, QtCore.SIGNAL("pressed()"),
                               self.close)

class ChangesWindow(QtGui.QMessageBox):
    """
    The Save, Cancel, Discard Changes window
    """
    def __init__(self, parent=None):
        """
        Creates the message box and then returns the button pressed
        """
        QtGui.QWidget.__init__(self, parent)
        self.setText("The document has been modified.")
        self.setInformativeText("What do you want to do?")
        self.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                                  QtGui.QMessageBox.Cancel)
        self.setDefaultButton(QtGui.QMessageBox.Save)
        self.setWindowTitle("Changes have been made")
        self.setWindowIcon(QtGui.QIcon("data/images/question.png"))

    def run(self):
        ret = self.exec_()
        return ret
        
class PrintDialog(QtGui.QPrintDialog):
    """
    The print dialog
    """
    def __init__(self, printer, parent=None):
        """
        Creates the printer dialog
        """
        QtGui.QWidget.__init__(self, printer, parent)

    def run(self):
        ret = self.exec_()
        return ret

class PrefWindow(QtGui.QMainWindow):
    """
    The preferences window
    """
    def __init__(self, parent, settings):
        """
        Initializes the class
        @type parent: QtGui.QWidget?
        @param parent: the parent widget
        @type settings: scripts.settings.Settings
        @param settings: the settings for the application
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.parent = parent
        self.settings = settings

        self.setObjectName("prefWindow")
        self.setWindowTitle("Preferences")
        self.setWindowIcon(QtGui.QIcon("data/images/preferences.png"))
        self.resize(500,475)
        self.central_widget = QtGui.QWidget(self)
        self.central_widget.setGeometry(QtCore.QRect(0,0,500,350))
        self.button_widget = QtGui.QWidget(self)
        self.button_widget.setGeometry(QtCore.QRect(0,355,500,120))

        self.main_layout = QtGui.QFormLayout()

        self.heading = QtGui.QLabel()
        self.heading.setText("Editor preferences:\n\n")
        self.main_layout.addRow(self.heading, None)

        self.res_width_label = QtGui.QLabel()
        self.res_width_label.setText("Resolution Width:")
        self.res_width = QtGui.QLineEdit()
        self.res_width.setMaxLength(4)
        self.res_width.setMaximumWidth(35)
        self.res_width.setText(self.settings.res_width)
        self.main_layout.addRow(self.res_width_label, self.res_width)
        self.res_height_label = QtGui.QLabel()
        self.res_height_label.setText("Resolution Height: ")
        self.res_height = QtGui.QLineEdit()
        self.res_height.setMaxLength(4)
        self.res_height.setMaximumWidth(35)
        self.res_height.setText(self.settings.res_height)
        self.main_layout.addRow(self.res_height_label, self.res_height)

        self.button_layout = QtGui.QHBoxLayout()
        
        self.button_cancel = QtGui.QPushButton()
        self.button_cancel.setText("Cancel")
        self.button_layout.addWidget(self.button_cancel)
        self.button_layout.insertStretch(1)
        self.button_apply = QtGui.QPushButton()
        self.button_apply.setText("Apply")
        self.button_layout.addWidget(self.button_apply)
        self.button_ok = QtGui.QPushButton()
        self.button_ok.setText("Ok")
        self.button_layout.addWidget(self.button_ok)
        self.button_widget.setLayout(self.button_layout)

        self.central_widget.setLayout(self.main_layout)
        
        self.connectSignals()

    def connectSignals(self):
        """
        Connect all the widgets to their corresponding signals
        @return: None
        """
        QtCore.QObject.connect(self.button_ok, QtCore.SIGNAL("pressed()"),
                               lambda: self.okOptions("data/options.txt"))
        QtCore.QObject.connect(self.button_apply, QtCore.SIGNAL("pressed()"),
                               lambda: self.applyOptions("data/options.txt"))
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL("pressed()"),
                               self.close)
        

    def applyOptions(self, options_file):
        """
        Apply the current options
        @type options_file: string
        @param options_file: the file to write to
        @return: None
        """
        self.settings.res_width = self.res_width.text()
        self.settings.res_height = self.res_height.text()
    
        self.settings.writeSettingsToFile(options_file)
        self.button_apply.setEnabled(False)

        self.parent.resize(int(self.settings.res_width),int(self.settings.res_height))

    def okOptions(self, options_file):
        """
        Apply the current options then close the window
        @type options_file: string
        @param options_file: the file to write to
        @return: None
        """
        self.applyOptions(options_file)
        self.close()

class HelpWindow(QtGui.QMainWindow):
    """
    The help window
    """
    def __init__(self, help_type, settings, parent=None):
        """
        @type help_type: string
        @param help_type: whether the window should be for help with the editor or scripting
                          can be either "editor" or "scripting"
        @type settings: settings.Settings
        @param settings: The editor's settings
        @return: None
        """
        QtGui.QWidget.__init__(self, parent)
        self.settings = settings

        if (help_type == "editor"):
            self.setWindowTitle("Help with the Editor")

        elif (help_type == "scripting"):
            self.setWindowTitle("Help with Scripting")

        else:
            print "Invalid argument for help_type. Should be either \"editor\" or \"scripting\""

        width = int(self.settings.res_width)
        height = int(self.settings.res_height)
        self.resize(width, height)
        self.setWindowIcon(QtGui.QIcon("data/images/help.png"))

        self.central_widget = QtGui.QWidget(self)
        self.central_widget.setGeometry(QtCore.QRect(0,0,width-10,height-50))

        self.main_layout = QtGui.QHBoxLayout()

        self.search_pane = QtGui.QWidget()
        self.search_pane.setMaximumWidth(175)    
        self.search_layout = QtGui.QVBoxLayout()
        self.search_label = QtGui.QLabel()
        self.search_label.setText("Search:")
        self.search_layout.addWidget(self.search_label)

        self.search_bar_layout = QtGui.QHBoxLayout()
        self.search_bar = QtGui.QLineEdit()
        self.search_bar.setMaximumWidth(120)
        self.search_bar_layout.addWidget(self.search_bar)
        self.go_button = QtGui.QPushButton()
        self.go_button.setText("Go")
        self.go_button.setMaximumWidth(30)
        self.search_bar_layout.addWidget(self.go_button)
        self.search_layout.addLayout(self.search_bar_layout)
        self.search_layout.insertStretch(2)

        self.search_view = QtGui.QListView()
        self.search_view.setMinimumHeight(height-150)
        self.search_view.setMinimumWidth(self.search_pane.width())
        self.search_layout.addWidget(self.search_view)
        self.search_pane.setLayout(self.search_layout)
        self.main_layout.addWidget(self.search_pane)

        self.main_help_window = QtGui.QTextEdit()
        self.main_layout.addWidget(self.main_help_window)

        self.central_widget.setLayout(self.main_layout)        
        
        self.connectSignals()

    def connectSignals(self):
        """
        Connect all the widgets to their respective functions
        @return: None
        """
        QtCore.QObject.connect(self.search_bar, QtCore.SIGNAL("returnPressed()"),
                               self.search)
        QtCore.QObject.connect(self.go_button, QtCore.SIGNAL("pressed()"),
                               self.search)
        
    def search(self):
        """
        Search through the documentation for the contents of self.search_bar
        @return: None
        """
        self.search_text = self.search_bar.text()
