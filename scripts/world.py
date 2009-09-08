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
        
        # self.data is an engine.Engine object, but is set in run.py
        self.data = None
        self.mouseCallback = None
        self.obj_hash={}

        # self.map is a Map object, set to none here
        self.activeMap = None
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
        """Saves the game state
           @return: None"""
        self.data.save(*args, **kwargs)

    def loadGame(self, *args, **kwargs):
        """Loads the game state
           @return: None"""
        self.data.load(*args, **kwargs)

    def loadMap(self, mapname, filename):
        """Loads a map an stores it under the given name in the maps list.
        """
        map = Map(self.engine, self.data)
        
        """Need to set active map before we load it because the map 
        loader uses call backs that expect to find an active map. 
        This needs to be reworked.
        """
        self.maps[mapname] = map
        self.setActiveMap(mapname)

        map.load(filename)

    
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
            self.hud.quitGame()
        if(keyval == key.T):
            self.activeMap.toggle_renderer('GridRenderer')
        if(keyval == key.F1):
            # display the help screen and pause the game
            self.hud.displayHelp()
        if (keyval == key.D):
            self.hud.showDialogue()
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
            self.hud.toggleInventory()
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
        self.hud.hideContextMenu() # hide the context menu in case it is displayed
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
            self.hud.showContextMenu(data, (scr_point.x, scr_point.y))

    def onWalk(self, click):
        """Callback sample for the context menu."""
        self.hud.hideContainer()
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

    def pump(self):
        """Routine called during each frame. Our main loop is in ./run.py
           We ignore this main loop (but FIFE complains if it is missing)."""
        pass
