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

import shutil, fife, pychan
from pychan.tools import callbackWithArguments as cbwa


class Hud():
    """Main Hud class"""
    def __init__(self, engine, settings):
        """Initialise the instance.
           @type engine: fife.Engine
           @param engine: An instance of the fife engine
           @type settings: settings.Setting
           @param settings: The settings data
           @return: None"""
        pychan.init(engine, debug = True)
        # TODO: perhaps this should not be hard-coded here
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
        """Initialize and show the main HUD
           @return: None"""
        self.events_to_map = {"menuButton":self.displayMenu,}
        self.hud.mapEvents(self.events_to_map) 
        # set HUD size accoriding to screen size
        screen_width = int(self.settings.readSetting('ScreenWidth'))
        self.hud.findChild(name="mainHudWindow").size = (screen_width, 65)
        self.hud.findChild(name="inventoryButton").position = (screen_width-59, 7)
        # add ready slots
        ready1 = self.hud.findChild(name='hudReady1')
        ready2 = self.hud.findChild(name='hudReady2')
        ready3 = self.hud.findChild(name='hudReady3')
        ready4 = self.hud.findChild(name='hudReady4')
        actions_scroll_area = self.hud.findChild(name='actionsScrollArea')
        # annoying code that is both essential and boring to enter
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
        # and finally add an actions box
        self.hud.findChild(name="actionsBox").min_size = (actions_width, 0)
        actions_scroll_area.min_size = (actions_width, 55)
        actions_scroll_area.max_size = (actions_width, 55)
        # now it should be OK to display it all
        self.hud.show()

    def refreshActionsBox(self):
        """Refresh the actions box so that it displays the contents of
           self.actionsText
           @return: None"""
        self.actionsBox.items = self.actionsText

    def addAction(self, action):
        """Add an action to the actions box.
           @type action: ???
           @param action: ???
           @return: None"""
        self.actionsText.insert(0, action)
        self.refreshActionsBox()

    def showHUD(self):
        """Show the HUD.
           @return: None"""
        self.hud.show()

    def hideHUD(self):
        """Hide the HUD.
           @return: None"""
        self.hud.hide()
        
    def initializeMainMenu(self):
        """Initalize the main menu.
           @return: None"""
        self.main_menu = pychan.loadXML("gui/hud_main_menu.xml")
        self.menu_events = {"resumeButton":self.hideMenu, 
                            "optionsButton":self.displayOptions,
                            "helpButton":self.displayHelp}
        self.main_menu.mapEvents(self.menu_events)

    def displayMenu(self):
        """Displays the main in-game menu.
           @return: None"""
        if (self.menu_displayed == False):
            self.main_menu.show()
            self.menu_displayed = True
        elif (self.menu_displayed == True):
            self.hideMenu()

    def hideMenu(self):
        """Hides the main in-game menu.
           @return: None"""
        self.main_menu.hide()
        self.menu_displayed = False

    def initializeHelpMenu(self):
        """Initialize the help menu
           @return: None"""
        self.help_dialog = pychan.loadXML("gui/help.xml")
        help_events = {"closeButton":self.help_dialog.hide}
        self.help_dialog.mapEvents(help_events)
        main_help_text = "Put help text here"
        k_text = " A : Add a test action to the actions display"
        k_text+="[br] I : Toggle the inventory screen"
        k_text+="[br]F5 : Take a screenshot"
        k_text+="[br]     (saves to <parpg>/screenshots/)"
        k_text+="[br] M : Toggle music on/off"
        k_text+="[br] Q : Quit the game"
        self.help_dialog.distributeInitialData({
                "MainHelpText":main_help_text,
                "KeybindText":k_text
                })

    def displayHelp(self):
        """Display the help screen.
           @return: None"""
        self.help_dialog.show()

    def initializeOptionsMenu(self):
        """Initalize the options menu.
           @return: None"""
        self.options_menu = pychan.loadXML("gui/hud_options.xml")
        self.options_events = {"applyButton":self.applyOptions,
                               "closeButton":self.options_menu.hide,
                               "defaultsButton":self.setToDefaults,
                               "InitialVolumeSlider":self.updateVolumeText}
        self.Resolutions = ['640x480', '800x600',
                            '1024x768', '1280x1024', '1440x900']
        self.RenderBackends = ['OpenGL', 'SDL']
        self.renderNumber = 0
        if (str(self.settings.readSetting('RenderBackend')) == "SDL"):
            self.renderNumber = 1
        initialVolume = float(self.settings.readSetting('InitialVolume'))
        initialVolumeText = str('Initial Volume: %.0f%s' %
                                (int(initialVolume*10), "%"))
        self.options_menu.distributeInitialData({
                'ResolutionBox': self.Resolutions,
                'RenderBox': self.RenderBackends,
                'InitialVolumeLabel' : initialVolumeText
                })
        # TODO: fix bad line length here
        self.options_menu.distributeData({
                'FullscreenBox':int(self.settings.readSetting(name="FullScreen")), 
                'SoundsBox':int(self.settings.readSetting(name="PlaySounds")),
                'ResolutionBox':self.Resolutions.index(str(self.settings.readSetting("ScreenWidth")) + 'x' + str(self.settings.readSetting("ScreenHeight"))),
                'RenderBox': self.renderNumber,
                'InitialVolumeSlider':initialVolume
                })
        self.options_menu.mapEvents(self.options_events)

    def updateVolumeText(self):
        """
        Update the initial volume label to reflect the value of the slider
        """
        volume = float(self.options_menu.collectData("InitialVolumeSlider"))
        volume_label = self.options_menu.findChild(name="InitialVolumeLabel")
        volume_label.text = unicode("Initial Volume: %.0f%s" %
                                    (int(volume*10), "%"))

    def requireRestartDialog(self):
        """Show a dialog asking the user to restart PARPG in order for their
           changes to take effect.
           @return: None"""
        require_restart_dialog = pychan.loadXML('gui/hud_require_restart.xml')
        require_restart_dialog.mapEvents({'okButton':require_restart_dialog.hide})
        require_restart_dialog.show()

    def applyOptions(self):
        """Apply the current options.
           @return: None"""
        # TODO: line lengths here are horrible
        # TODO: add comments
        self.requireRestart = False
        enable_fullscreen, enable_sound, screen_resolution, render_backend, initial_volume = self.options_menu.collectData('FullscreenBox', 'SoundsBox', 'ResolutionBox', 'RenderBox', 'InitialVolumeSlider')
        initial_volume = "%.1f" % initial_volume

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

        if (initial_volume != float(self.settings.readSetting("InitialVolume"))):
            self.setOption('InitialVolume', initial_volume)
            self.requireRestart = True

        self.settings.tree.write('settings.xml')
        if (self.requireRestart):
            self.requireRestartDialog()
        self.options_menu.hide()

    def setOption(self, name, value):
        """Set an option within the xml.
           @type name: ???
           @param name: The name?
           @type value: ???
           @param value: The value?
           @return: None"""
        element = self.settings.root_element.find(name)
        if(element != None):
            if(value != element.text):
                element.text = str(value)
        else:
            print 'Setting,', name, 'does not exist!'

    def setToDefaults(self):
        """Reset all the options to the options in settings-dist.xml.
           @return: None"""
        shutil.copyfile('settings-dist.xml', 'settings.xml')
        self.requireRestartDialog()
        self.options_menu.hide()

    def displayOptions(self):
        """Display the options menu.
           @return: None"""
        self.options_menu.show()
    
    def toggleInventory(self):
        """Manually toggles the inventory button.
           @return: None"""
        button = self.hud.findChild(name="inventoryButton")
        if(button.toggled == 0):
            button.toggled = 1
        else:
            button.toggled = 0

