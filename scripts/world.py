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

TDS = Setting()

# this file should be the meta-file for all FIFE-related code
# engine.py handles is our data model, whilst this is our view
# in order to not replicate data, some of our data model will naturally
# reside on this side of the fence (PC xpos and ypos, for example).
# we should aim to never replicate any data as this leads to maintainance
# issues (and just looks plain bad).
# however, any logic needed to resolve this should sit in engine.py

class MapListener(fife.MapChangeListener):
    """This class listens to changes happening on the map.
       Since in theory we initiate these ourselves, do we need this class?"""
    def __init__(self, map):
        fife.MapChangeListener.__init__(self)

    def onMapChanged(self, map, changedLayers):
        pass

    def onLayerCreate(self, map, layer):
        pass

    def onLayerDelete(self, map, layer):
        pass

class Map:
    def __init__(self, fife_map):
        self.listener = MapListener
        self.map = fife_map

class World(EventListenerBase):
    """World holds the data needed by fife to render the engine
       The engine keeps a copy of this class"""
    def __init__(self, engine):
        super(World, self).__init__(engine, regMouse = True, regKeys = True)
        self.engine = engine
        self.eventmanager = engine.getEventManager()
        self.model = engine.getModel()
        self.view = self.engine.getView()
        self.quitFunction = None
        self.inventoryShown = False
        self.firstInventory = True
        self.data = None
        self.mouseCallback = None

    def reset(self):
        """Rest the map to default settings"""
        self.transitions = []
        self.PC = None
        self.npcs = []
        self.map,self.agent_layer = None,None
        self.cameras = {}
        self.PC = None
        self.npcs = []
        self.cur_cam2_x,self.initial_cam2_x,self.cam2_scrolling_right = 0,0,True
        self.target_rotation = 0

    def load(self, filename):
        """Load a map given the filename
           TODO: a map should only contain static items and floor tiles
           Everything else should be loaded from the engine, because it
           is subject to change"""
        self.reset()
        self.map = loadMapFile(filename, self.engine)
        self.maplistener = MapListener(self.map)

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

    def addPC(self, agent):
        """Add the player character to the map"""
        # actually this is real easy, we just have to
        # attach the main camera to the PC
        self.cameras['main'].attach(agent)
    
    def addObject(self, xpos, ypos, name):
        """Add an object or an NPC to the map
           It makes no difference to fife which is which"""
        obj = self.agent_layer.createInstance(
                self.model.getObject(str(name), "PARPG"),
                fife.ExactModelCoordinate(xpos,ypos,0.0), str(name))
        obj.setRotation(0)
        fife.InstanceVisual.create(obj)

    def displayInventory(self):
        """Pause the game and enter the inventory screen
           or close the inventory screen and resume the game"""
        # show the inventory
        if(self.firstInventory == True):
            self.inventory = inventory.Inventory(self.engine)
            self.firstInventory = False
            self.inventoryShown = True
        # logically firstInventory is false here
        elif(self.inventoryShown == True):
            self.inventory.closeInventory()
            self.inventoryShown = False
        # and here inventoryShown must be false
        else:
            self.inventory.showInventory()
            self.inventoryShown = True

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
                                                  time.strftime('%H:%M:%S'))
            self.engine.getRenderBackend().captureScreen(t)
        if(keyval == key.I):
            # I opens and closes the inventory
            self.displayInventory()

    def getCoords(self, click):
        """Get the map location x, y cords that have been clicked"""
        coord = self.cameras["main"].toMapCoordinates(click, False)
        coord.z = 0
        location = fife.Location(self.agent_layer)
        location.setMapCoordinates(coord)
        return location

    def mousePressed(self, evt):
        """If a mouse button is pressed down, fife cals this routine
           Currently we only check for a left click, and we assume this is on
           the map"""
        click = fife.ScreenPoint(evt.getX(), evt.getY())
        if(evt.getButton() == fife.MouseEvent.LEFT):
            self.data.handleMouseClick(self.getCoords(click))
        elif(evt.getButton() == fife.MouseEvent.RIGHT):
            # there's no need to query fife about what things are where,
            # the engine code should know....
            coords = self.getCoords(click).getLayerCoordinates()
            obj = self.data.getObjectString(coords.x, coords.y)
            if(obj != ""):
                print obj

    def toggle_renderer (self, r_name):
        """Enable or disable the renderer named `r_name`"""
        renderer = self.cameras['main'].getRenderer('GridRenderer')
        renderer.setEnabled(not renderer.isEnabled())

    def displayHelp(self):
        """Displays the pop-up info and help screen"""
        print "Help not yet coded"

    def quitGame(self):
        """Called when user requests to quit game
           Just calls the ApplicationListener to do the quit"""
        if(self.quitFunction != None):
            self.quitFunction()

    def pump(self):
        """Routine called during each frame. Our main loop is in ./run.py
           We ignore this main loop (but FIFE complains if it is missing)"""
        pass

