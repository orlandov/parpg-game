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

import time
import fife
import pychan
from sounds import SoundEngine
from datetime import date
from scripts.common.eventlistenerbase import EventListenerBase
from local_loaders.loaders import loadMapFile
from sounds import SoundEngine
from settings import Setting
from scripts import hud
from scripts.popups import *
from pychan.tools import callbackWithArguments as cbwa
from map import Map

TDS = Setting()

# this file should be the meta-file for all FIFE-related code
# engine.py handles is our data model, whilst this is our view
# in order to not replicate data, some of our data model will naturally
# reside on this side of the fence (PC xpos and ypos, for example).
# we should aim to never replicate any data as this leads to maintenance
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
        super(World, self).__init__(engine, reg_mouse=True, reg_keys=True)
        # self.engine is a fife.Engine object, not an Engine object
        self.engine = engine
        self.event_manager = engine.getEventManager()
        self.quitFunction = None
        
        # self.data is an engine.Engine object, but is set in run.py
        self.data = None
        self.mouseCallback = None

        # self.map is a Map object, set to none here
        self.active_map = None
        self.maps = {}

        # setup the inventory model
        # make slot 'A1' and 'A3' container daggers
        inv_model = {'A1':'dagger01', 'A3':'dagger01'}

        hud_callbacks = {
            'saveGame': self.saveGame,
            'loadGame': self.loadGame,
            'quitGame': self.quitGame,
        }
        self.hud = hud.Hud(self.engine, TDS, inv_model, hud_callbacks)
        self.action_number = 1

        # init the sound
        self.sounds = SoundEngine(engine)
        
        # don't force restart if skipping to new section
        if (TDS.readSetting("PlaySounds") == "1"):
            if(self.sounds.music_init == False):
                self.sounds.playMusic("/music/preciouswasteland.ogg")
                
    def quitGame(self):
        """Quits the game
        @return: None"""
        self.quitFunction()

    def saveGame(self, *args, **kwargs):
        """Saves the game state, delegates call to engine.Engine
           @return: None"""
        self.data.save(*args, **kwargs)

    def loadGame(self, *args, **kwargs):
        """Loads the game state, delegates call to engine.Engine
           @return: None"""
        self.data.load(*args, **kwargs)
        
    def loadMap(self, map_name, filename):
        """Loads a map and stores it under the given name in the maps list.
           @type map_name: text
           @param map_name: The name of the map to load 
           @type filename: text
           @param filename: File which contains the map to be loaded
           @return: None
        """
        if not map_name in self.maps:
            """Need to set active map before we load it because the map 
            loader uses call backs that expect to find an active map. 
            This needs to be reworked.
            """
            map = Map(self.engine, self.data)
            self.maps[map_name] = map        
            self.setActiveMap(map_name)
            map.load(filename)
    
    def setActiveMap(self, map_name):
        """Sets the active map that is to be rendered.
           @type map_name: text
           @param map_name: The name of the map to load 
           @return: None
        """
        self.active_map = self.maps[map_name]
        self.active_map.makeActive()

    def displayObjectText(self, obj, text):
        """Display on screen the text of the object over the object.
           @type obj: fife.instance
           @param obj: object to draw over
           @type text: text
           @param text: text to display over object
           @return: None"""
        obj.say(str(text), 1000)

    def keyPressed(self, evt):
        """Whenever a key is pressed, fife calls this routine.
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        key = evt.getKey()
        key_val = key.getValue()

        if(key_val == key.Q):
            # we need to quit the game
            self.hud.quitGame()
        if(key_val == key.T):
            self.active_map.toggle_renderer('GridRenderer')
        if(key_val == key.F1):
            # display the help screen and pause the game
            self.hud.displayHelp()
        if(key_val == key.F5):
            # logic would say we use similar code to above and toggle
            # logic here does not work, my friend :-(
            self.cord_render.setEnabled(not self.cord_render.isEnabled())
        if(key_val == key.F7):
            # F7 saves a screenshot to fife/clients/parpg/screenshots
            t = "screenshots/screen-%s-%s.png" % \
                    (date.today().strftime('%Y-%m-%d'),\
                    time.strftime('%H-%M-%S'))
            print "PARPG: Saved:",t
            self.engine.getRenderBackend().captureScreen(t)
        if(key_val == key.F10):
            # F10 shows/hides the console
            self.engine.getGuiManager().getConsole().toggleShowHide()
        if(key_val == key.I):
            # I opens and closes the inventory
            self.hud.toggleInventory()
        if(key_val == key.A):
            # A adds a test action to the action box
            # The test actions will follow this format: Action 1,
            # Action 2, etc.
            self.hud.addAction("Action " + str(self.action_number))
            self.action_number += 1
        if(key_val == key.ESCAPE):
            # Escape brings up the main menu
            self.hud.displayMenu()
            # Hide the quit menu 
            self.hud.quit_window.hide()
        if(key_val == key.M):
            self.sounds.toggleMusic()

    def mouseReleased(self, evt):
        """If a mouse button is released, fife calls this routine.
           We want to wait until the button is released, because otherwise
           pychan captures the release if a menu is opened.
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        self.hud.hideContextMenu()
        scr_point = fife.ScreenPoint(evt.getX(), evt.getY())
        if(evt.getButton() == fife.MouseEvent.LEFT):
            self.data.handleMouseClick(self.getCoords(scr_point))      
        elif(evt.getButton() == fife.MouseEvent.RIGHT):
            # is there an object here?
            instances = self.active_map.cameras['main'].\
                            getMatchingInstances(scr_point, \
                                                 self.active_map.agent_layer)
            info = None
            for inst in instances:
                # check to see if this is an active item
                if(self.data.objectActive(inst.getId())):            
                    # yes, get the data
                    info = self.data.getItemActions(inst.getId())
                    break
                
            # take the menu items returned by the engine or show a
            # default menu if no items    
            data = info or \
                [["Walk", "Walk here", self.onWalk, self.getCoords(scr_point)]]
            # show the menu
            self.hud.showContextMenu(data, (scr_point.x, scr_point.y))

    def onWalk(self, click):
        """Callback sample for the context menu."""
        self.hud.hideContainer()
        self.data.game_state.PC.run(click)

    def teleport(self, position):
        """Called when a door is used that moves a player to a new
           location on the same map. the setting of position may want
           to be created as its own method down the road.
           @type position: String Tuple
           @param position: X,Y coordinates passed from engine.changeMap
           @return: fife.Location
        """
        coord = fife.DoublePoint3D(float(position[0]), float(position[1]), 0)
        location = fife.Location(self.active_map.agent_layer)
        location.setMapCoordinates(coord)
        self.data.game_state.PC.teleport(location)

    def mouseMoved(self, evt):
        """Called when the mouse is moved
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        click = fife.ScreenPoint(evt.getX(), evt.getY())
        i=self.active_map.cameras['main'].getMatchingInstances(click, \
                                                self.active_map.agent_layer)
        # no object returns an empty tuple
        if(i != ()):
            front_y = 0
            front_obj = None

            for obj in i:
                # check to see if this in our list at all
                if(self.data.objectActive(obj.getId())):
                    # check if the object is on the foreground 
                    obj_map_coords = \
                                      obj.getLocation().getMapCoordinates()
                    obj_screen_coords = self.active_map.cameras["main"]\
                                    .toScreenCoordinates(obj_map_coords)
                    
                    if obj_screen_coords.y > front_y:
                        #Object on the foreground
                        front_y = obj_screen_coords.y
                        front_obj = obj

            if front_obj:                    
                self.active_map.outline_render.removeAllOutlines() 
                self.active_map.outline_render.addOutlined(front_obj, 0, \
                                                               137, 255, 2)
                # get the text
                item = self.data.objectActive(front_obj.getId())
                if(item is not None):
                    self.displayObjectText(front_obj, item.name)
        else:
            # erase the outline
            self.active_map.outline_render.removeAllOutlines()

    def getCoords(self, click):
        """Get the map location x, y coordinates from the screen coordinates
           @type click: fife.ScreenPoint
           @param click: Screen coordinates
           @rtype: fife.Location
           @return: The map coordinates"""
        coord = self.active_map.cameras["main"].toMapCoordinates(click, False)
        coord.z = 0
        location = fife.Location(self.active_map.agent_layer)
        location.setMapCoordinates(coord)
        return location

    def pump(self):
        """Routine called during each frame. Our main loop is in ./run.py
           We ignore this main loop (but FIFE complains if it is missing)."""
        pass
