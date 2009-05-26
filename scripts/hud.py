#!/usr/bin/python

"""Import all necessary modules"""
import fife
import pychan
from pychan.tools import callbackWithArguments as cbwa

"""Main Hud class"""
class Hud():
    """
    Arguments:
        engine : an instance of the fife engine
    """
    def __init__(self, engine):
        pychan.init(engine, debug = True)
        
        self.hud = pychan.loadXML("gui/hud.xml")

        self.hp = self.hud.findChild(name="HealthPoints")
        self.ap = self.hud.findChild(name="ActionPoints")
        self.actionsBox = self.hud.findChild(name="ActionsBox")
        self.actionsText = []
        self.menu_displayed = False

        self.events_to_map = {"menuButton":self.displayMenu, "saveButton":self.saveGame,
                              "loadButton":self.loadGame}
        self.hud.mapEvents(self.events_to_map) 
        self.hud.show()

        self.main_menu = pychan.loadXML("gui/hud_main_menu.xml")
        self.menu_events = {"resumeButton":self.hideMenu, "saveButton":self.saveGame,
                            "loadButton":self.loadGame, 
                            "optionsButton":self.displayOptions}
        self.main_menu.mapEvents(self.menu_events)

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
        self.actionsText.append(action)
        self.refreshActionsBox()

    def displayOptions(self):
        print "options"

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
