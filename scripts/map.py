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
from local_loaders.loaders import loadMapFile
from scripts.common.eventlistenerbase import EventListenerBase

from settings import Setting
TDS = Setting()

class Map(fife.MapChangeListener):
    """Map class used to flag changes in the map"""
    def __init__(self, engine, data):
        # init mapchange listener
        fife.MapChangeListener.__init__(self)
        self.map = None
        self.engine = engine
        self.data = data
        
        # init map attributes
        self.cameras = {}
        self.agent_layer = None
        self.model = engine.getModel()
        self.view = engine.getView()
        self.transitions = []
        self.cur_cam2_x = 0
        self.initial_cam2_x = 0
        self.cam2_scrolling_right = True
        self.target_rotation = 0
        self.outline_renderer = None
        
    def reset(self):
        """Reset the data to default settings.
           @return: None"""
        # We have to delete the map in Fife.
        # TODO: We're killing the PC now, but later we will have to save the PC
        if self.map:
            self.model.deleteObjects()
            self.model.deleteMap(self.map)
        self.transitions = []
        self.map = None
        self.agent_layer = None
        # We have to clear the cameras in the view as well, or we can't reuse
        # camera names like 'main'
        self.view.clearCameras()
        self.cameras = {}
        self.cur_cam2_x = 0
        self.initial_cam2_x = 0
        self.cam2_scrolling_right = True
        self.target_rotation = 0
        self.outline_renderer = None
        
    def makeActive(self):
        """Makes this map the active one.
        """
        pass
        
    def load(self, filename):
        """Load a map given the filename.
           @type filename: string
           @param filename: Name of map to load
           @return: None"""
        self.reset()
        self.map = loadMapFile(filename, self.engine, self.data)
         
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
        
        self.outline_render = fife.InstanceRenderer.\
                                        getInstance(self.cameras['main'])
        
        # set the render text
        rend = fife.FloatingTextRenderer.getInstance(self.cameras['main'])
        text = self.engine.getGuiManager().\
                        createFont('fonts/rpgfont.png', 0, \
                                   str(TDS.readSetting("FontGlyphs", \
                                                       strip=False)))
        rend.changeDefaultFont(text)
                
    def addPC(self, agent):
        """Add the player character to the map
           @type agent: Fife.instance of PC
           @return: None"""
        # actually this is real easy, we just have to
        # attach the main camera to the PC, if a camera
        # was already used, we simply recycle it. 
        if self.cameras['main'].getAttached() == None:
            self.cameras['main'].attach(agent)

        
    def toggle_renderer(self, r_name):
        """Enable or disable a renderer.
           @return: None"""
        renderer = self.cameras['main'].getRenderer(str(r_name))
        renderer.setEnabled(not renderer.isEnabled())

