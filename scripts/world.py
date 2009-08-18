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

import fife, time
import pychan
from sounds import SoundEngine
from scripts.parpgfilebrowser import PARPGFileBrowser
from datetime import date
from scripts.common.eventlistenerbase import EventListenerBase
from settings import Setting
from scripts import inventory, hud
from scripts.popups import *
from scripts.context_menu import ContextMenu
from pychan.tools import callbackWithArguments as cbwa
from map import Map

TDS = Setting()

# this file should be the meta-file for all FIFE-related code
# engine.py handles is our data model, whilst this is our view
# in order to not replicate data, some of our data model will naturally
# reside on this side of the fence (PC xpos and ypos, for example).
# we should aim to never replicate any data as this leads to maintainance
# issues (and just looks plain bad).
# however, any logic needed to resolve this should sit in engine.py

class World(EventListenerBase):
    """World holds the data needed by fife to render the engine
       The engine keeps a copy of this class"""
    def __init__(self, engine):
        """Constructor for engine
           @type engine: fife.Engine
           @param engine: A fife.Engine instance
           @return: None"""
        super(World, self).__init__(engine, regMouse = True, regKeys = True)
        # self.engine is a fife.Engine object, not an Engine object
        self.engine = engine
        self.eventmanager = engine.getEventManager()
        self.quitFunction = None
        self.inventoryShown = False 
        
        # self.data is an engine.Engine object, but is set in run.py
        self.data = None
        self.mouseCallback = None
        self.obj_hash={}
        # self.map is a Map object, set to none here
        self.activeMap = None
        self.maps = {}
        self.hud = hud.Hud(self.engine, TDS)
        self.hud.events_to_map["inventoryButton"] = cbwa(self.displayInventory, True)
        self.hud.events_to_map["saveButton"] = self.saveGame
        self.hud.events_to_map["loadButton"] = self.loadGame
        hud_ready_buttons = ["hudReady1", "hudReady2", "hudReady3", "hudReady4"]
        for item in hud_ready_buttons:
            self.hud.events_to_map[item] = cbwa(self.hud.readyAction, item)
        self.hud.hud.mapEvents(self.hud.events_to_map)
        self.hud.menu_events["newButton"] = self.newGame
        self.hud.menu_events["quitButton"] = self.quitGame
        self.hud.menu_events["saveButton"] = self.saveGame
        self.hud.menu_events["loadButton"] = self.loadGame
        self.hud.main_menu.mapEvents(self.hud.menu_events)
        self.action_number = 1
        # setup the inventory
        # make slot 'A1' and 'A3' container daggers
        inv_data = {'A1':'dagger01', 'A3':'dagger01'}
        self.inventory = inventory.Inventory(self.engine, inv_data, self.refreshReadyImages)
        self.inventory.events_to_map['close_button'] = self.closeInventoryAndToggle
        self.inventory.inventory.mapEvents(self.inventory.events_to_map)
        self.refreshReadyImages()
        
        self.context_menu = ContextMenu (self.engine, [], (0,0))
        self.context_menu.hide()
        self.boxOpen = False
        self.boxCreated = False
        
        # init the sound
        self.sounds = SoundEngine(engine)
        
        # don't force restart if skipping to new section
        if (TDS.readSetting("PlaySounds") == "1"):
            if(self.sounds.music_init == False):
                self.sounds.playMusic("/music/preciouswasteland.ogg")
                
    def loadMap(self, mapname, filename):
        """Loads a map an stores it under the given name in the maps list.
        """
        map = Map(self.engine)
        map.load(filename)
        self.maps[mapname] = map
    
    def setActiveMap(self, mapname):
        """Sets the active map that is to be rendered.
        """
        self.activeMap = self.maps[mapname]
        self.activeMap.makeActive()

    def displayObjectText(self, obj, text):
        """Display on screen the text of the object over the object.
           @type obj: fife.instance
           @param obj: object to draw over
           @type text: text
           @param text: text to display over object
           @return: None"""
        obj.say(str(text), 1000)

    def refreshReadyImages(self):
        """Make the Ready slot images on the HUD be the same as those 
           on the inventory
           @return: None"""
        self.setImages(self.hud.hud.findChild(name="hudReady1"),
                       self.inventory.inventory.findChild(name="Ready1").up_image)
        self.setImages(self.hud.hud.findChild(name="hudReady2"),
                       self.inventory.inventory.findChild(name="Ready2").up_image)
        self.setImages(self.hud.hud.findChild(name="hudReady3"),
                       self.inventory.inventory.findChild(name="Ready3").up_image)
        self.setImages(self.hud.hud.findChild(name="hudReady4"),
                       self.inventory.inventory.findChild(name="Ready4").up_image)

    def setImages(self, widget, image):
        """Set the up, down, and hover images of an Imagebutton.
           @type widget: pychan.widget
           @param widget: widget to set
           @type image: string
           @param image: image to use
           @return: None"""
        widget.up_image = image
        widget.down_image = image
        widget.hover_image = image

    def closeInventoryAndToggle(self):
        """Close the inventory screen.
           @return: None"""
        self.inventory.closeInventory()
        self.hud.toggleInventory()
        self.inventoryShown = False

    def displayInventory(self, callFromHud):
        """Pause the game and enter the inventory screen, or close the
           inventory screen and resume the game. callFromHud should be true
           (must be True?) if you call this function from the HUD script
           @type callFromHud: boolean
           @param callFromHud: Whether this function is being called 
                               from the HUD script
           @return: None"""
        if (self.inventoryShown == False):
            self.inventory.showInventory()
            self.inventoryShown = True
        else:
            self.inventory.closeInventory()
            self.inventoryShown = False
        if (callFromHud == False):
            self.hud.toggleInventory()

    # all key / mouse event handling routines go here
    def keyPressed(self, evt):
        """Whenever a key is pressed, fife calls this routine.
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        key = evt.getKey()
        keyval = key.getValue()

        if(keyval == key.Q):
            # we need to quit the game
            self.quitGame()
        if(keyval == key.T):
            self.toggle_renderer('GridRenderer')
        if(keyval == key.F1):
            # display the help screen and pause the game
            self.displayHelp()
        if(keyval == key.F5):
            # logic would say we use similar code to above and toggle
            # logic here does not work, my friend :-(
            self.cord_render.setEnabled(not self.cord_render.isEnabled())
        if(keyval == key.F7):
            # F7 saves a screenshot to fife/clients/parpg/screenshots
            t = "screenshots/screen-%s-%s.png" % (date.today().strftime('%Y-%m-%d'),
                                                  time.strftime('%H-%M-%S'))
            print "PARPG: Saved:",t
            self.engine.getRenderBackend().captureScreen(t)
        if(keyval == key.F10):
            # F10 shows/hides the console
            self.engine.getGuiManager().getConsole().toggleShowHide()
        if(keyval == key.I):
            # I opens and closes the inventory
            self.displayInventory(callFromHud=False)
        if(keyval == key.A):
            # A adds a test action to the action box
            # The test actions will follow this format: Action 1, Action 2, etc.
            self.hud.addAction("Action " + str(self.action_number))
            self.action_number += 1
        if(keyval == key.ESCAPE):
            # Escape brings up the main menu
            self.hud.displayMenu()
        if(keyval == key.M):
            self.sounds.toggleMusic()

    def mouseReleased(self, evt):
        """If a mouse button is released, fife calls this routine.
           We want to wait until the button is released, because otherwise
           pychan captures the release if a menu is opened.
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        self.context_menu.hide() # hide the context menu in case it is displayed
        scr_point = fife.ScreenPoint(evt.getX(), evt.getY())
        if(evt.getButton() == fife.MouseEvent.LEFT):
            self.data.handleMouseClick(self.getCoords(scr_point))      
        elif(evt.getButton() == fife.MouseEvent.RIGHT):
            # is there an object here?
            instances = self.activeMap.cameras['main'].getMatchingInstances(scr_point, self.activeMap.agent_layer)
            info = None
            for inst in instances:
                # check to see if this is an active item
                if(self.data.objectActive(inst.getId())):            
                    # yes, get the data
                    info = self.data.getItemActions(inst.getId())
                    break
                
            # take the menu items returned by the engine or show a default menu if no items    
            data = info or [["Walk", "Walk here", self.onWalk, self.getCoords(scr_point)]]
            # show the menu
            self.context_menu = ContextMenu(self.engine, data, (scr_point.x,scr_point.y))

    def onWalk(self, click):
        """Callback sample for the context menu.
        """
        self.context_menu.hide()
        self.data.gameState.PC.run(click)

    def mouseMoved(self, evt):
        """Called when the mouse is moved
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        click = fife.ScreenPoint(evt.getX(), evt.getY())
        i=self.activeMap.cameras['main'].getMatchingInstances(click, self.activeMap.agent_layer)
        # no object returns an empty tuple
        if(i != ()):
            for obj in i:
                # check to see if this in our list at all
                if(self.data.objectActive(obj.getId())):
                    # yes, so outline    
                    self.activeMap.outline_render.addOutlined(obj, 0, 137, 255, 2)
                    # get the text
                    item = self.data.objectActive(obj.getId())
                    if(item):
                        self.displayObjectText(obj, item.name)
        else:
            # erase the outline
            self.activeMap.outline_render.removeAllOutlines()

    def getCoords(self, click):
        """Get the map location x, y cords from the screen co-ords
           @type click: fife.ScreenPoint
           @param click: Screen co-ords
           @rtype: fife.Location
           @return: The map co-ords"""
        coord = self.activeMap.cameras["main"].toMapCoordinates(click, False)
        coord.z = 0
        location = fife.Location(self.activeMap.agent_layer)
        location.setMapCoordinates(coord)
        return location

    def clearMenu(self):
        """ Hides the context menu. Just nice to have it as a function.
            @return: None"""
        if hasattr(self, "context_menu"):
            self.context_menu.vbox.hide()
            delattr(self, "context_menu")

    def newGame(self):
        """Called when user request to start a new game.
           @return: None"""
        print 'new game'

    def quitGame(self):
        """Called when user requests to quit game.
           @return: None"""
        if(self.quitFunction != None):
            window = pychan.widgets.Window(title=unicode("Quit?"))

            hbox = pychan.widgets.HBox()
            are_you_sure = "Are you sure you want to quit?"
            label = pychan.widgets.Label(text=unicode(are_you_sure))
            yes_button = pychan.widgets.Button(name="yes_button", 
                                               text=unicode("Yes"))
            no_button = pychan.widgets.Button(name="no_button",
                                              text=unicode("No"))

            window.addChild(label)
            hbox.addChild(yes_button)
            hbox.addChild(no_button)
            window.addChild(hbox)

            events_to_map = {"yes_button":self.quitFunction,
                             "no_button":window.hide}
            
            window.mapEvents(events_to_map)
            window.show()

    def saveGame(self):
        """ Called when the user wants to save the game.
            @return: None"""
        self.save_browser = PARPGFileBrowser(self.engine,
                                        self.data.save,
                                        savefile=True,
                                        guixmlpath="gui/savebrowser.xml",
                                        extensions = ('.dat'))
        self.save_browser.showBrowser()
            

    def loadGame(self):
        """ Called when the user wants to load a game.
            @return: None"""
        self.load_browser = PARPGFileBrowser(self.engine,
                                        self.data.load,
                                        savefile=False,
                                        guixmlpath='gui/loadbrowser.xml',
                                        extensions=('.dat'))
        self.load_browser.showBrowser()


    def createBoxGUI(self, title):
        """
        Creates a window to display the contents of a box

        @type title: string
        @param title: The title for the window
        @return: None
        """
        if ((self.boxCreated == True) and (self.boxOpen == False)):
            # if it has already been created, just show it
            self.box_container.showContainer()
            self.boxOpen = True
        else:
            # otherwise create it then show it
            data = ["dagger01", "empty", "empty", "empty", "empty",
                    "empty", "empty", "empty", "empty"]
            self.box_container = ContainerGUI(self.engine, unicode(title), data)
            def close_and_delete():
                self.box_container.hideContainer()
                self.boxOpen = False
            events = {'takeAllButton':close_and_delete,
                      'closeButton':close_and_delete}
            self.box_container.container_gui.mapEvents(events)
            self.box_container.showContainer()
            self.boxOpen = True
            self.boxCreated = True

    def createExamineBox(self, title, desc):
        self.examineBox = ExaminePopup(self.engine, title, desc)
        self.examineBox.showPopUp()

    def pump(self):
        """Routine called during each frame. Our main loop is in ./run.py
           We ignore this main loop (but FIFE complains if it is missing)."""
        pass
