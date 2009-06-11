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
from settings import Setting
from random import randint

TDS = Setting()
_STATE_NONE, _STATE_IDLE, _STATE_WANDER = xrange(3)

class NPC(fife.InstanceActionListener):
    """This is the class we use for all NPCs"""
    def __init__(self, text, agent_name, layer):
        """Init function.
           @param text: a string of text that will be output to screen when
               character is right clicked
           @param id: the 'id' of the NPC in the map_object.xml file
           @param layer: a fife.Instance object, (engine.view.agent_layer)"""
        fife.InstanceActionListener.__init__(self)
        self.text = text
        self.id = agent_name
        # a fife.Instance
        self.agent = layer.getInstance(agent_name)
        self.agent.addActionListener(self)
        self.state = _STATE_NONE
        self.speed = float(TDS.readSetting("PCSpeed"))-1
        self.target_loc = self.getTargetLocation() 
        self.text = text

    def getX(self):
        """@return: the x coordinate of the NPC's location as an int"""
        return self.agent.getLocation().getLayerCoordinates().x

    def getY(self):
        """@return: the y coordinate of the NPC's location as an int"""
        return self.agent.getLocation().getLayerCoordinates().y

    def getTargetLocation(self):
        """@return: a fife.Location object based off of the NPC's
           position and current state"""
        x = self.getX()
        y = self.getY()
        if self.state == _STATE_WANDER:
            """ Random Walk """
            rl = randint(-1, 1)
            ud = randint(-1, 1)
            x += rl
            y += ud
        l = fife.Location(self.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(*tuple([x, y])))
        return l

    def onInstanceActionFinished(self, instance, action):
        """What the NPC does when it has finished an action.
           Called somewhere else (TODO: where?)"""
        if self.state == _STATE_WANDER:
            self.target_loc = self.getTargetLocation()
        self.idle()

    def start(self):
        self.idle()

    def idle(self):
        """Controls the NPC when it is idling. Different actions
           based on the NPC's state"""
        if self.state == _STATE_NONE:
            self.state = _STATE_IDLE
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _STATE_IDLE:
            self.target_loc = self.getTargetLocation()
            self.state = _STATE_WANDER
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _STATE_WANDER:
            self.wander(self.target_loc)

    def wander(self, location):
        """Nice slow movement for random walking.
           @param location: a fife.Location object, where the NPC
           will walk to"""
        self.agent.move('walk', location, self.speed-1)

    def run(self, location):
        """Faster movement than walk.
           @param location: a fife.Location object, where the NPC will run to"""
        self.agent.move('run', location, self.speed+1)

