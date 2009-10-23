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
        self.my_cam_id = None
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
        if self.map:
            self.model.deleteObjects()
            self.model.deleteMap(self.map)
        self.transitions = []
        self.map = None
        self.agent_layer = None        
        # We have to clear the cameras in the view as well, or we can't reuse
        # camera names like 'main'
        #self.view.clearCameras()
        self.initial_cam2_x = 0
        self.cam2_scrolling_right = True
        #self.cameras = {}
        self.cur_cam2_x = 0
        self.target_rotation = 0
        self.outline_renderer = None
        
    def makeActive(self):
        """Makes this map the active one.
        """
        self.cameras[self.my_cam_id].setEnabled(True)

        
    def load(self, filename):
        """Load a map given the filename.
           @type filename: String
           @param filename: Name of map to load
           @return: None"""
        self.reset()
        self.map = loadMapFile(filename, self.engine, self.data)
        self.agent_layer = self.map.getLayer('ObjectLayer')

        # if this is not the very first map load in the game carry over the PC instance
        if self.data.target_position:
            x = float(self.data.target_position[0])
            y = float(self.data.target_position[1])
            z = 0
            pc_obj = self.model.getObject("player", "PARPG")
            inst = self.agent_layer.createInstance(pc_obj,\
                                            fife.ExactModelCoordinate(x,y,z),\
                                            "PC")
            inst.setRotation(self.data.game_state.PC.behaviour.agent.getRotation())
            fife.InstanceVisual.create(inst)

        # it's possible there's no transition layer
        size = len('TransitionLayer')
        for layer in self.map.getLayers():
            # could be many layers, but hopefully no more than 3
            if(layer.getId()[:size] == 'TransitionLayer'):
                self.transitions.append(self.map.getLayer(layer.getId()))

        """ Initialize the camera.
        Note that if we have more than one camera in a map file
        we will have to rework how self.my_cam_id works. To make sure
        the proper camera is set as the 'main' camera."""
        for cam in self.view.getCameras():
            self.my_cam_id = cam.getId()
            self.cameras[self.my_cam_id] = cam
        self.view.resetRenderers()
        self.target_rotation = self.cameras[self.my_cam_id].getRotation()

        self.outline_render = fife.InstanceRenderer.\
                                        getInstance(self.cameras[self.my_cam_id])

        # set the render text
        rend = fife.FloatingTextRenderer.getInstance(self.cameras[self.my_cam_id])
        text = self.engine.getGuiManager().\
                        createFont('fonts/rpgfont.png', 0, \
                                   str(TDS.readSetting("FontGlyphs", \
                                                       strip=False)))
        rend.changeDefaultFont(text)

        # Make World aware that this is now the active map.
        self.data.view.active_map = self
                
    def addPC(self):
        """Add the player character to the map
           @return: None"""

        # Update gamestate.PC
        self.data.game_state.PC.behaviour.onNewMap(self.agent_layer)

        # actually this is real easy, we just have to
        # attach the main camera to the PC, if a camera
        # was already used, we simply recycle it. 
        if self.cameras[self.my_cam_id].getAttached() == None:
            self.cameras[self.my_cam_id].attach(self.data.game_state.PC.behaviour.agent)

        
    def toggle_renderer(self, r_name):
        """Enable or disable a renderer.
           @return: None"""
        renderer = self.cameras[self.my_cam_id].getRenderer(str(r_name))
        renderer.setEnabled(not renderer.isEnabled())

