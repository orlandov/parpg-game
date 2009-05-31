#!/usr/bin/python

# Make the actions append at the top instead of the bottom

"""Import all necessary modules"""
import fife
import pychan
from pychan.tools import callbackWithArguments as cbwa

"""Main Hud class"""
class Hud():
    """
    Arguments:
        engine : an instance of the fife engine
        settings : an instance of the class Setting from settings.py
    """
    def __init__(self, engine, settings):
        pychan.init(engine, debug = True)
        
        self.hud = pychan.loadXML("gui/hud.xml")

        self.settings = settings
        self.hp = self.hud.findChild(name="HealthPoints")
        self.ap = self.hud.findChild(name="ActionPoints")
        self.actionsBox = self.hud.findChild(name="ActionsBox")
        self.actionsText = []
        self.menu_displayed = False

        """Initialize and show the main HUD"""
        self.events_to_map = {"menuButton":self.displayMenu, "saveButton":self.saveGame,
                              "loadButton":self.loadGame}
        self.hud.mapEvents(self.events_to_map) 
        self.hud.show()
        
        """Initalize the main menu"""
        self.main_menu = pychan.loadXML("gui/hud_main_menu.xml")
        self.menu_events = {"resumeButton":self.hideMenu, "saveButton":self.saveGame,
                            "loadButton":self.loadGame, 
                            "optionsButton":self.displayOptions}
        self.main_menu.mapEvents(self.menu_events)

        """Initalize the options menu"""
        self.options_menu = pychan.loadXML("gui/hud_options.xml")
        self.options_events = {"applyButton":self.applyOptions, "closeButton":self.options_menu.hide}

        self.options_menu.distributeData({'FullscreenBox':int(self.settings.readSetting(name="FullScreen")),
                                          'SoundsBox':int(self.settings.readSetting(name="PlaySounds"))})
        
        self.options_menu.mapEvents(self.options_events)


    def refreshActionsBox(self):
        """ 
        Refresh the actions box so that it displays the contents of self.actionsText
        """
        self.actionsBox.items = self.actionsText


    def addAction(self, action):
        """ 
        Add an action to the actions box.
        All this function really does is append action to self.actionsText and then
        call refreshActionsBox
        """
        self.actionsText.insert(0, action)
        self.refreshActionsBox()

    def requireRestartDialog(self):
        """
        Show a dialog asking the user to restart PARPG for their changes to take effect
        """
        require_restart_dialog = pychan.loadXML('gui/hud_require_restart.xml')
        require_restart_dialog.mapEvents({'okButton':require_restart_dialog.hide})
        require_restart_dialog.show()

    def applyOptions(self):
        """
        Apply the current options
        """
        self.requireRestart = False
        enable_fullscreen, enable_sound = self.options_menu.collectData('FullscreenBox', 'SoundsBox')

        if (int(enable_fullscreen) != int(self.settings.readSetting('FullScreen'))):
            self.setOption('FullScreen', int(enable_fullscreen))
            self.requireRestart = True
            
        if (int(enable_sound) != int(self.settings.readSetting('PlaySounds'))):
            self.setOption('PlaySounds', int(enable_sound))
            self.requireRestart = True

        self.settings.tree.write('settings.xml')
        if (self.requireRestart):
            self.requireRestartDialog()
        self.options_menu.hide()

    def setOption(self, name, value):
        """
        Set an option within the xml
        """
        element = self.settings.root_element.find(name)
        if (element != None):
            if (value != element.text):
                element.text = str(value)
        else:
            print 'Setting,', name, 'does not exist!'

    def displayOptions(self):
        """
        Display the options menu
        """
        self.options_menu.show()

    def displayMenu(self):
        """
        Displays the main in-game menu
        """
        if (self.menu_displayed == False):
            self.main_menu.show()
            self.menu_displayed = True
        elif (self.menu_displayed == True):
            self.hideMenu()

    def hideMenu(self):
        """
        Hides the main in-game menu
        """
        self.main_menu.hide()
        self.menu_displayed = False

    def saveGame(self):
        """
        Open the save game dialog
        """
        print "save"

    def loadGame(self):
        """
        Open the load game dialog
        """
        print "load"

    def setHP(self, value):
        """
        Set the HP display on the HUD to value
        NOTE: This does not in any way affect the character's actual health, only
              what is displayed on the HUD
        """
        self.hp.text = value

    def setAP(self, value):
        """
        Set the AP display on the HUD to value
        NOTE: This does no in any way affect the character's actual AP, only
              what is displayed on the HUD
        """
        self.ap.text = value
        
    def toggleInventory(self):
        """
        Manually toggles the inventory button
        """
        button = self.hud.findChild(name="inventoryButton")
        if (button.toggled == 0):
            button.toggled = 1
        else:
            button.toggled = 0
