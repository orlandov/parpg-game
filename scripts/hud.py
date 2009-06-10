#!/usr/bin/python

"""Import all necessary modules"""
import shutil
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
        self.actionsBox = self.hud.findChild(name="actionsBox")
        self.actionsText = []
        self.menu_displayed = False
        
        self.initializeHud()
        self.initializeMainMenu()
        self.initializeOptionsMenu()
        self.initializeHelpMenu()

    def initializeHud(self):
        """Initialize and show the main HUD"""
        self.events_to_map = {"menuButton":self.displayMenu, "saveButton":self.saveGame,
                              "loadButton":self.loadGame}
        self.hud.mapEvents(self.events_to_map) 

        screen_width = int(self.settings.readSetting('ScreenWidth'))
        self.hud.findChild(name="mainHudWindow").size = (screen_width, 65)
        self.hud.findChild(name="inventoryButton").position = (screen_width-59, 7)

        ready1 = self.hud.findChild(name='hudReady1')
        ready2 = self.hud.findChild(name='hudReady2')
        ready3 = self.hud.findChild(name='hudReady3')
        ready4 = self.hud.findChild(name='hudReady4')
        actions_scroll_area = self.hud.findChild(name='actionsScrollArea')

        if (screen_width == 1440):
            ready1.position = (screen_width-1235, 7)
            ready2.position = (screen_width-1175, 7)
            ready3.position = (screen_width-215, 7)
            ready4.position = (screen_width-155, 7)
            actions_scroll_area.position = (325, 5)
            actions_width = screen_width - 550

        elif (screen_width == 1280):
            ready1.position = (screen_width-1075, 7)
            ready2.position = (screen_width-1015, 7)
            ready3.position = (screen_width-215, 7)
            ready4.position = (screen_width-155, 7)
            actions_scroll_area.position = (325, 5)
            actions_width = screen_width - 550

        elif (screen_width == 1024):
            ready1.position = (screen_width-820, 7)
            ready2.position = (screen_width-760, 7)
            ready3.position = (screen_width-215, 7)
            ready4.position = (screen_width-155, 7)
            actions_scroll_area.position = (325, 5)
            actions_width = screen_width - 550

        elif (screen_width == 800):
            ready1.position = (screen_width-640, 7)
            ready2.position = (screen_width-580, 7)
            ready3.position = (screen_width-185, 7)
            ready4.position = (screen_width-125, 7)
            actions_scroll_area.position = (280, 5)
            actions_width = screen_width - 475

        else:
            ready1.position = (screen_width-475, 7)
            ready2.position = (screen_width-420, 7)
            ready3.position = (screen_width-175, 7)
            ready4.position = (screen_width-120, 7)
            actions_scroll_area.position = (280, 5)
            actions_width = screen_width - 465

        self.hud.findChild(name="actionsBox").min_size = (actions_width, 0)
        actions_scroll_area.min_size = (actions_width, 55)
        actions_scroll_area.max_size = (actions_width, 55)

        self.hud.show()

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

    def showHUD(self):
        """
        Show the HUD
        """
        self.hud.show()

    def hideHUD(self):
        """
        Hide the HUD
        """
        self.hud.hide()
        
    def initializeMainMenu(self):
        """Initalize the main menu"""
        self.main_menu = pychan.loadXML("gui/hud_main_menu.xml")
        self.menu_events = {"resumeButton":self.hideMenu, "saveButton":self.saveGame,
                            "loadButton":self.loadGame, 
                            "optionsButton":self.displayOptions,
                            "helpButton":self.displayHelp}
        self.main_menu.mapEvents(self.menu_events)

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

    def initializeHelpMenu(self):
        """Initialize the help menu"""

        self.help_dialog = pychan.loadXML("gui/help.xml")
        help_events = {"closeButton":self.help_dialog.hide}
        self.help_dialog.mapEvents(help_events)

        main_help_text = "Put help text here"

        keybindings_text = "A : Add a test action to the actions display[br]I : Toggle the inventory screen[br]F5 : Take a screenshot [br]     (saves to <parpg>/screenshots/)[br]Q : Quit the game"

        self.help_dialog.distributeInitialData({
                "MainHelpText":main_help_text,
                "KeybindText":keybindings_text
                })

    def displayHelp(self):
        """ Display the help screen """
        self.help_dialog.show()

    def initializeOptionsMenu(self):
        """Initalize the options menu"""

        self.options_menu = pychan.loadXML("gui/hud_options.xml")
        self.options_events = {"applyButton":self.applyOptions,
                               "closeButton":self.options_menu.hide,
                               "defaultsButton":self.setToDefaults}

        self.Resolutions = ['640x480', '800x600', '1024x768', '1280x1024', '1440x900']
        self.RenderBackends = ['OpenGL', 'SDL']
        self.renderNumber = 0
        if (str(self.settings.readSetting('RenderBackend')) == "SDL"):
            self.renderNumber = 1
        self.options_menu.distributeInitialData({
                'ResolutionBox': self.Resolutions,
                'RenderBox': self.RenderBackends
                })
        self.options_menu.distributeData({
                'FullscreenBox':int(self.settings.readSetting(name="FullScreen")), 
                'SoundsBox':int(self.settings.readSetting(name="PlaySounds")),
                'ResolutionBox':self.Resolutions.index(str(self.settings.readSetting("ScreenWidth")) + 'x' + str(self.settings.readSetting("ScreenHeight"))),
                'RenderBox': self.renderNumber
                })
        
        self.options_menu.mapEvents(self.options_events)

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
        enable_fullscreen, enable_sound, screen_resolution, render_backend = self.options_menu.collectData('FullscreenBox', 'SoundsBox', 'ResolutionBox', 'RenderBox')

        if (int(enable_fullscreen) != int(self.settings.readSetting('FullScreen'))):
            self.setOption('FullScreen', int(enable_fullscreen))
            self.requireRestart = True
            
        if (int(enable_sound) != int(self.settings.readSetting('PlaySounds'))):
            self.setOption('PlaySounds', int(enable_sound))
            self.requireRestart = True

        if (screen_resolution != self.Resolutions.index(str(self.settings.readSetting("ScreenWidth")) + 'x' + str(self.settings.readSetting("ScreenHeight")))):
            self.setOption('ScreenWidth', int(self.Resolutions[screen_resolution].partition('x')[0]))
            self.setOption('ScreenHeight', int(self.Resolutions[screen_resolution].partition('x')[2]))
            self.requireRestart = True
        
        if (render_backend == 0):
            render_backend = 'OpenGL'
        else:
            render_backend = 'SDL'

        if (render_backend != str(self.settings.readSetting("RenderBackend"))):
            self.setOption('RenderBackend', render_backend)
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

    def setToDefaults(self):
        """ Reset all the options to the options in settings-dist.xml """
        shutil.copyfile('settings-dist.xml', 'settings.xml')
        self.requireRestartDialog()
        self.options_menu.hide()

    def displayOptions(self):
        """
        Display the options menu
        """
        self.options_menu.show()
    
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
        
    def toggleInventory(self):
        """
        Manually toggles the inventory button
        """
        button = self.hud.findChild(name="inventoryButton")
        if (button.toggled == 0):
            button.toggled = 1
        else:
            button.toggled = 0
