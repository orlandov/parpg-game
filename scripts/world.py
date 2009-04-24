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
from scripts.common.eventlistenerbase import EventListenerBase
from loaders import loadMapFile
from agents.hero import Hero
from settings import Setting

TDS = Setting()

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

class World(EventListenerBase):
    """World holds the data needed by fife to render the engine
       Extracting information from the map file, such as is there an object
       here, and so forth are normally done from here, so I propose this
       acts as the map class
       Presumably the story engine will need access to this class"""
    def __init__(self, engine):
        super(World, self).__init__(engine, regMouse=True, regKeys=True)
        self.engine = engine
        self.eventmanager = engine.getEventManager()
        self.model = engine.getModel()
        self.view = self.engine.getView()
        self.filename = ''
        self.instance_to_agent = {}
        self.transitions = []

    def reset(self):
        self.map, self.agentlayer = None, None
        self.cameras = {}
        self.PC = None
        self.cur_cam2_x,self.initial_cam2_x,self.cam2_scrolling_right=0,0,True
        self.target_rotation = 0
        self.instance_to_agent = {}

    def load(self, filename):
        self.filename = filename
        self.reset()
        self.map = loadMapFile(filename, self.engine)
        self.maplistener = MapListener(self.map)

        # there must be a PC object on the objects layer!
        self.agentlayer = self.map.getLayer('ObjectLayer')
        # it's possible there's no transition layer
        size=len('TransitionLayer')
        for layer in self.map.getLayers():
            # could be many layers, but hopefully no more than 3
            if(layer.getId()[:size]=='TransitionLayer'):
                self.transitions.append(self.map.getLayer(layer.getId()))
        self.PC = Hero(self.model,'PC',self.agentlayer)
        self.instance_to_agent[self.PC.agent.getFifeId()] = self.PC
        # ensure the PC starts on a default action
        self.PC.start()

        # init the camera
        for cam in self.view.getCameras():
            self.cameras[cam.getId()] = cam
        self.cameras['main'].attach(self.PC.agent)
        self.view.resetRenderers()
        self.target_rotation = self.cameras['main'].getRotation()
        self.cord_render=self.cameras['main'].getRenderer('CoordinateRenderer')

    def keyPressed(self, evt):
        """When a key is depressed, fife calls this routine."""
        key=evt.getKey()
        keyval = key.getValue()

        if keyval == key.T:
            self.toggle_renderer('GridRenderer')
        if keyval == key.F5:
            # logic would say we use similar code to above and toggle
            # logic here does not work, my friend :-(
            self.cord_render.setEnabled(not self.cord_render.isEnabled())

    def mousePressed(self, evt):
        """If a mouse button is pressed down, fife calss this routine
           Currently we only check for a left click, and we assume this is on
           the map"""
        clickpoint = fife.ScreenPoint(evt.getX(), evt.getY())
        if (evt.getButton()==fife.MouseEvent.LEFT):
            target_mapcoord=self.cameras['main'].toMapCoordinates(clickpoint, False)
            target_mapcoord.z = 0
            l = fife.Location(self.agentlayer)
            l.setMapCoordinates(target_mapcoord)
            self.PC.run(l)
            
    def toggle_renderer (self,r_name):
        """Enable or disable the renderer named `r_name`"""
        renderer = self.cameras['main'].getRenderer('GridRenderer')
        renderer.setEnabled(not renderer.isEnabled())

    def pump(self):
        """Routine called during each frame. Here we need to call the
           story engine code"""
        pass

