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

import fife
import time
from datetime import date
from scripts.common.eventlistenerbase import EventListenerBase
from loaders import loadMapFile
from agents.hero import Hero
from agents.npc import NPC
from settings import Setting
from scripts import inventory
from scripts import hud
from scripts.context_menu import ContextMenu
from pychan.tools import callbackWithArguments as cbwa

TDS = Setting()

# this file should be the meta-file for all FIFE-related code
# engine.py handles is our data model, whilst this is our view
# in order to not replicate data, some of our data model will naturally
# reside on this side of the fence (PC xpos and ypos, for example).
# we should aim to never replicate any data as this leads to maintainance
# issues (and just looks plain bad).
# however, any logic needed to resolve this should sit in engine.py

class Map(fife.MapChangeListener):
    def __init__(self, fife_map):
        fife.MapChangeListener.__init__(self)
        self.map = fife_map

class World(EventListenerBase):
    """World holds the data needed by fife to render the engine
       The engine keeps a copy of this class"""
    def __init__(self, engine):
        """Constructor for engine
           TODO: Comment these variables"""
        super(World, self).__init__(engine, regMouse = True, regKeys = True)
        # self.engine is a fife.Engine object, not an Engine object
        self.engine = engine
        self.eventmanager = engine.getEventManager()
        self.model = engine.getModel()
        self.view = self.engine.getView()
        self.quitFunction = None
        self.inventoryShown = False
        # self.data is an engine.Engine object, but is set in run.py
        self.data = None
        self.mouseCallback = None
        self.obj_hash={}
        # self.map is a Map object, set to none here
        self.map = None
        self.hud = hud.Hud(self.engine, TDS)
        self.hud.events_to_map["inventoryButton"] = cbwa(self.displayInventory, True)
        self.hud.hud.mapEvents(self.hud.events_to_map)
        self.hud.menu_events["quitButton"] = self.quitGame
        self.hud.main_menu.mapEvents(self.hud.menu_events)
        self.action_number = 1

        self.inventory = inventory.Inventory(self.engine, self.refreshReadyImages)
        self.inventory.events_to_map['close_button'] = self.closeInventoryAndToggle
        self.inventory.inventory.mapEvents(self.inventory.events_to_map)
        self.refreshReadyImages()

    def reset(self):
        """Reset the map to default settings"""
        # We have to delete the map in Fife.
        # TODO: I'm killing the PC now, but later we will have to save the PC
        if self.map:
            self.model.deleteMap(self.map)
        self.transitions = []
        """ self.PC and self.npcs are never used, and can be accessed through
            the self.data object...commented out for the time being
            Also, why are there duplicated lines?"""
        #self.PC = None
        #self.npcs = []
        self.map,self.agent_layer = None,None
        # We have to clear the cameras in the view as well, or we can't reuse
        # camera names like 'main'
        self.view.clearCameras()
        self.cameras = {}
        #self.PC = None
        #self.npcs = []
        self.cur_cam2_x,self.initial_cam2_x,self.cam2_scrolling_right = 0,0,True
        self.target_rotation = 0

    def load(self, filename):
        """Load a map given the filename
           TODO: a map should only contain static items and floor tiles
           Everything else should be loaded from the engine, because it
           is subject to change"""
        self.reset()

        self.map = loadMapFile(filename, self.engine)
        self.maplistener = Map(self.map)

        # there must be a PC object on the objects layer!
        self.agent_layer = self.map.getLayer('ObjectLayer')
        # it's possible there's no transition layer
        size = len('TransitionLayer')
        for layer in self.map.getLayers():
            # could be many layers, but hopefully no more than 3
            if(layer.getId()[:size] == 'TransitionLayer'):
                self.transitions.append(self.map.getLayer(layer.getId()))

        # init the camera
        for cam in self.view.getCameras():
            self.cameras[cam.getId()] = cam
        self.view.resetRenderers()
        self.target_rotation = self.cameras['main'].getRotation()
        self.cord_render = self.cameras['main'].getRenderer('CoordinateRenderer')
        self.outline_render = fife.InstanceRenderer.getInstance(self.cameras['main'])
        
        # set the render text
        rend = fife.FloatingTextRenderer.getInstance(self.cameras['main'])
        text = self.engine.getGuiManager().createFont('fonts/rpgfont.png',
                                                          0, str(TDS.readSetting("FontGlyphs", strip=False)))
        rend.changeDefaultFont(text)

    def addPC(self, agent):
        """Add the player character to the map"""
        # actually this is real easy, we just have to
        # attach the main camera to the PC
        self.cameras['main'].attach(agent)
    
    def addObject(self, xpos, ypos, gfx, name):
        """Add an object or an NPC to the map
           It makes no difference to fife which is which"""
        obj = self.agent_layer.createInstance(
                self.model.getObject(str(gfx), "PARPG"),
                fife.ExactModelCoordinate(xpos,ypos,0.0), str(name))
        obj.setRotation(0)
        fife.InstanceVisual.create(obj)
        # save it for later use
        self.obj_hash[name]=obj

    def displayObjectText(self, obj, text):
        """Display on screen the text of the object over the object"""
        obj.say(str(text), 1000)

    def refreshReadyImages(self):
        """Make the Ready slot images on the HUD be the same as those on the inventory"""
        self.setImages(self.hud.hud.findChild(name="hudReady1"),
                       self.inventory.inventory.findChild(name="Ready1").up_image)
        self.setImages(self.hud.hud.findChild(name="hudReady2"),
                       self.inventory.inventory.findChild(name="Ready2").up_image)
        self.setImages(self.hud.hud.findChild(name="hudReady3"),
                       self.inventory.inventory.findChild(name="Ready3").up_image)
        self.setImages(self.hud.hud.findChild(name="hudReady4"),
                       self.inventory.inventory.findChild(name="Ready4").up_image)

    def setImages(self, widget, image):
        """Set the up, down, and hover images of an Imagebutton"""
        widget.up_image = image
        widget.down_image = image
        widget.hover_image = image

    def closeInventoryAndToggle(self):
        self.inventory.closeInventory()
        self.hud.toggleInventory()
        self.inventoryShown = False

    def displayInventory(self, callFromHud):
        """Pause the game and enter the inventory screen
           or close the inventory screen and resume the game
           callFromHud should be set to true if you call this
           function from the hud script"""
        if (self.inventoryShown == False):
            self.inventory.showInventory()
            self.inventoryShown = True
            if (callFromHud == False):
                self.hud.toggleInventory()
        else:
            self.inventory.closeInventory()
            self.inventoryShown = False
            if (callFromHud == False):
                self.hud.toggleInventory()

    # all key / mouse event handling routines go here
    def keyPressed(self, evt):
        """When a key is pressed, fife calls this routine."""
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

    def getCoords(self, click):
        """Get the map location x, y cords that have been clicked"""
        coord = self.cameras["main"].toMapCoordinates(click, False)
        coord.z = 0
        location = fife.Location(self.agent_layer)
        location.setMapCoordinates(coord)
        return location

    def mousePressed(self, evt):
        """If a mouse button is pressed down, fife cals this routine
           Currently we assume this is on the map"""
        click = fife.ScreenPoint(evt.getX(), evt.getY())
        if(evt.getButton() == fife.MouseEvent.LEFT):
            self.data.handleMouseClick(self.getCoords(click))
            if (hasattr(self, "context_menu")):
                self.context_menu.vbox.hide()
                delattr(self, "context_menu")
                
        elif(evt.getButton() == fife.MouseEvent.RIGHT):
            # is there an object here?
            i=self.cameras['main'].getMatchingInstances(click, self.agent_layer)
            if(i != ()):
                for obj in i:
                    # check to see if this is an active item
                    if(self.data.objectActive(obj.getId()) != False):            
                        # yes, get the data
                        info = self.data.getItemActions(obj.getId())
                        print info
            if (hasattr(self, "context_menu")):
                self.context_menu.vbox.hide()
                delattr(self, "context_menu")
                data = [["Placeholder", "Placeholder Button", self.placeHolderFunction, click]]
                pos = (evt.getX(), evt.getY())
                self.context_menu = ContextMenu(self.engine, data, pos)

            else:
                data = [["Placeholder", "Placeholder Button", self.placeHolderFunction, click]]
                pos = (evt.getX(), evt.getY())
                self.context_menu = ContextMenu(self.engine, data, pos)

    def placeHolderFunction(self):
        """Just a simple function to make the PC say "Place Holder Function!"
           It's in here because we needed some sort of function to test the context 
           menu with"""
        self.agent_layer.getInstance("PC").say("Place Holder Function!", 1000)
        self.context_menu.vbox.hide()
        delattr(self, "context_menu")

    def mouseMoved(self, evt):
        """Called when the mouse is moved"""
        click = fife.ScreenPoint(evt.getX(), evt.getY())
        i=self.cameras['main'].getMatchingInstances(click, self.agent_layer)
        # no object returns an empty tuple
        if(i != ()):
            for obj in i:
                # check to see if this in our list at all
                if(self.data.objectActive(obj.getId())!=False):
                    # yes, so outline    
                    self.outline_render.addOutlined(obj, 0, 137, 255, 2)
                    # get the text
                    item = self.data.objectActive(obj.getId())
                    if(item != False):
                        self.displayObjectText(obj, item.text)
        else:
            # erase the outline
            self.outline_render.removeAllOutlines()

    def toggle_renderer(self, r_name):
        """Enable or disable the renderer named `r_name`"""
        renderer = self.cameras['main'].getRenderer('GridRenderer')
        renderer.setEnabled(not renderer.isEnabled())

    def quitGame(self):
        """Called when user requests to quit game
           Just calls the ApplicationListener to do the quit"""
        if(self.quitFunction != None):
            self.quitFunction()

    def pump(self):
        """Routine called during each frame. Our main loop is in ./run.py
           We ignore this main loop (but FIFE complains if it is missing)"""
        pass

