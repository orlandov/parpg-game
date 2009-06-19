#!/usr/bin/python

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import fife
from settings import Setting

TDS = Setting()
_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_TALK = xrange(4)

class Hero(fife.InstanceActionListener):
    def __init__(self, agentName, layer, engine):
        """This is the class we use for the PC character.
           @type agentName: string
           @param agentName: name of the agent
           @type layer: string
           @param layer: Layer to place agent on.
           @type engine: scripts.engine.Engine
           @param engine: Reference to the engine that owns this PC.
           @return: None"""
        # add this class for callbacks from fife itself
        fife.InstanceActionListener.__init__(self)
        self.agentName = agentName
        self.agent = layer.getInstance(agentName)
        self.agent.addActionListener(self)
        self.state = _STATE_NONE
        self.idlecounter = 1
        self.speed = float(TDS.readSetting("PCSpeed"))
        self.engine = engine
        
    def onNewMap(self, layer):
        """Sets the agent onto the new layer.
        """
        self.agent = layer.getInstance(self.agentName)
        self.agent.addActionListener(self)
        self.state = _STATE_NONE
        self.idlecounter = 1

    def getX(self):
        """ Get the Hero's position on the map.
            @rtype: integer
            @return: the x coordinate of the NPC's location"""
        return self.agent.getLocation().getLayerCoordinates().x

    def getY(self):
        """ Get the Hero's position on the map.
            @rtype: integer
            @return: the y coordinate of the NPC's location"""
        return self.agent.getLocation().getLayerCoordinates().y

    def onInstanceActionFinished(self, instance, action):
        """@type instance: ???
           @param instance: ???
           @type action: ???
           @param action: ???
           @return: None"""
        if action.getId() == 'approachDoor':
            # issue map change
            self.engine.changeMap(self.targetMap, self.targetLocation)
        if self.state == _STATE_TALK:
            # TODO: do something
            pass
        self.idle()
        if(action.getId() != 'stand'):
            self.idlecounter = 1
        else:
            self.idlecounter += 1

    def start(self):
        """@return: None"""
        self.idle()

    def idle(self):
        """@return: None"""
        self.state = _STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation())

    def run(self, location):
        """@type location: ???
           @param location: ???
           @return: None"""
        self.state = _STATE_RUN
        self.agent.move('run', location, self.speed)

    def approachNPC(self, npcLoc):
        """Approaches an npc and then ???.
           @type npcLoc: fife.Location
           @param npcLoc: the location of the NPC to approach
           @return: None"""
        self.state = _STATE_TALK
        self.agent.move('run', npcLoc, self.speed)

    def approachDoor(self, doorLocation, map, targetLocation):
        """Approach a door and then teleport to the new map.
           @type doorLocation: list
           @param doorLocation: list that is converted to a fife.Location
            that tells the PC where the door is
           @type map: ???
           @param map: ???
           @type targetLocation: list
           @param targetLocation: list that is converted to a tuple
            that tels the PC where it should appear on the target map
           @return: None"""
        # The casting here is HORRIBLE, but I think it is preferable to having
        # doors behave differently than other objects, hence the change.
        self.state = _STATE_RUN
        targetLocation = tuple([int(float(i)) for i in targetLocation])
        doorLocation = tuple([int(float(i)) for i in doorLocation])
        self.targetMap = map
        self.targetLocation = targetLocation
        l = fife.Location(self.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(*doorLocation))
        self.agent.move('approachDoor', l, self.speed)
