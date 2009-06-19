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
from random import randrange

TDS = Setting()
_STATE_NONE, _STATE_IDLE, _STATE_WANDER, _STATE_TALK = xrange(4)

class NPC(fife.InstanceActionListener):
    """This is the class we use for all NPCs"""
    def __init__(self, text, agent_name, layer):
        """Init function.
           @type text: string
           @param text: The text to draw when character is right clicked.
           @type agent_name: string
           @param agent_name: the ID of the NPC
           @type layer: ???
           @param layer: ???
           @return: None"""
        fife.InstanceActionListener.__init__(self)
        self.text = text
        self.id = agent_name
        # a fife.Instance
        self.agent = layer.getInstance(agent_name)
        self.agent.addActionListener(self)
        self.state = _STATE_NONE
        self.speed = float(TDS.readSetting("PCSpeed"))-1
        # hard code this for now
        self.distRange = (2, 4)
        self.targetLoc = self.getTargetLocation() 
        self.text = text
        # good to have the pc in case we ever need to follow it
        self.pc = layer.getInstance('PC')

    def getX(self):
        """Get the NPC's x position on the map.
           @rtype: integer"
           @return: the x coordinate of the NPC's location"""
        return self.agent.getLocation().getLayerCoordinates().x

    def getY(self):
        """Get the NPC's y position on the map.
           @rtype: integer
           @return: the y coordinate of the NPC's location"""
        return self.agent.getLocation().getLayerCoordinates().y

    def getLocation(self):
        """ Get the NPC's position as a fife.Location object. Basically a
            wrapper.
            @rtype: fife.Location
            @return: the location of the NPC"""
        return self.agent.getLocation()

    def getTargetLocation(self):
        """@rtype: fife.Location
           @return: NPC's position"""
        x = self.getX()
        y = self.getY()
        if self.state == _STATE_WANDER:
            """ Random Target Location """
            l = [0, 0]
            for i in range(len(l)):
                sign = randrange(0, 2)
                dist = randrange(self.distRange[0], self.distRange[1])
                if sign == 0:
                    dist *= -1
                l[i] = dist
            x += l[0]
            y += l[1]
            # Random walk is
            # rl = randint(-1, 1);ud = randint(-1, 1);x += rl;y += ud
        l = fife.Location(self.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(*tuple([x, y])))
        return l

    def onInstanceActionFinished(self, instance, action):
        """What the NPC does when it has finished an action.
           Called by the engine and required for InstanceActionListeners.
           @type instance: fife.Instance
           @param instance: self.agent (the NPC listener is listening for this
            instance)
           @type action: ???
           @param action: ???
           @return: None"""
        if self.state == _STATE_WANDER:
            self.targetLoc = self.getTargetLocation()
        self.idle()

    def start(self):
        """@return: None"""
        self.idle()

    def idle(self):
        """Controls the NPC when it is idling. Different actions
           based on the NPC's state.
           @return: None"""
        if self.state == _STATE_NONE:
            self.state = _STATE_IDLE
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _STATE_IDLE:
            self.targetLoc = self.getTargetLocation()
            self.state = _STATE_WANDER
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _STATE_WANDER:
            self.wander(self.targetLoc)
            self.state = _STATE_NONE
        elif self.state == _STATE_TALK:
            self.agent.act('stand', self.pc.getLocation())

    def wander(self, location):
        """Nice slow movement for random walking.
           @type location: fife.Location
           @param location: Where the NPC will walk to.
           @return: None"""
        self.agent.move('walk', location, self.speed-1)

    def run(self, location):
        """Faster movement than walk.
           @type location: fife.Location
           @param location: Where the NPC will run to."""
        self.agent.move('run', location, self.speed+1)

    def talk(self):
        """ Makes the NPC ready to talk to the PC
            @return: None"""
        self.state = _STATE_TALK
        self.idle()
