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
from base import *

"""All actors go here. Concrete classes only."""

__all__ = ["PlayerCharacter", "NonPlayerCharacter",]

TDS = Setting()
_AGENT_STATE_NONE, _AGENT_STATE_IDLE, _AGENT_STATE_RUN, _AGENT_STATE_WANDER, _AGENT_STATE_TALK = xrange(5)

class ActorBehaviour (fife.InstanceActionListener):
    """Fife agent listener
    """
    def __init__(self):
        fife.InstanceActionListener.__init__(self)
    
    def attachToLayer(self, fifeLayer, agentID):
        # init listener
        self.agent = fifeLayer.getInstance(agentID)
        self.agent.addActionListener(self)
        self.state = _AGENT_STATE_NONE
        self.speed = float(TDS.readSetting("PCSpeed"))-1 # TODO: rework/improve
        
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
        
    def onInstanceActionFinished(self, instance, action):
        pass

    
class PCBehaviour (ActorBehaviour):
    def __init__(self, Parent = None, Engine = None):
        super(PCBehaviour, self).__init__()
        
        self.parent = Parent
        self.engine = Engine
        self.idlecounter = 1
        self.speed = float(TDS.readSetting("PCSpeed")) # TODO: rework/improve
        
    def onInstanceActionFinished(self, instance, action):
        """@type instance: ???
           @param instance: ???
           @type action: ???
           @param action: ???
           @return: None"""
        if action.getId() == 'approachDoor':
            # issue map change
            self.parent.engine.changeMap(self.targetMap, self.targetLocation)
        if self.state == _AGENT_STATE_TALK:
            # TODO: do something
            pass
        self.idle()
        if(action.getId() != 'stand'):
            self.idlecounter = 1
        else:
            self.idlecounter += 1
            
    def onNewMap(self, layer):
        """Sets the agent onto the new layer.
        """
        self.agent = layer.getInstance(self.parent.name)
        self.agent.addActionListener(self)
        self.state = _AGENT_STATE_NONE
        self.idlecounter = 1
    
    def idle(self):
        """@return: None"""
        self.state = _AGENT_STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation())

class PlayerCharacter (GameObject, Living, CharStats):
    """
    PC class
    """
    def __init__ (self, ID, agent_layer = None, engine = None, **kwargs):
        super(PlayerCharacter, self).__init__(ID, **kwargs)
        self.is_PC = True
        self.agent_layer = agent_layer
        
        # PC _has_ an inventory, he _is not_ one
        self.inventory = None
        self.engine = engine
        
        self.state = _AGENT_STATE_NONE
        self.behaviour = PCBehaviour(self, engine)
    
    def setup(self):
        """@return: None"""
        self.behaviour.attachToLayer(self.agent_layer, self.ID)

    def start(self):
        """@return: None"""
        self.behaviour.idle()
    
    def run(self, location):
        """@type location: ???
           @param location: ???
           @return: None"""
        self.state = _AGENT_STATE_RUN
        self.behaviour.agent.move('run', location, self.behaviour.speed)

    def approachNPC(self, npcLoc):
        """Approaches an npc and then ???.
           @type npcLoc: fife.Location
           @param npcLoc: the location of the NPC to approach
           @return: None"""
        self.state = _AGENT_STATE_TALK
        self.behaviour.agent.move('run', npcLoc, self.behaviour.speed)

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
        self.state = _AGENT_STATE_RUN
        targetLocation = tuple([int(float(i)) for i in targetLocation])
        doorLocation = tuple([int(float(i)) for i in doorLocation])
        self.targetMap = map
        self.targetLocation = targetLocation
        l = fife.Location(self.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(*doorLocation))
        self.behaviour.agent.move('approachDoor', l, self.behaviour.speed)
        
    def approachBox(self, location):
        """
        Approach a box and then open it
        @type location: list
        @param locatation: list that is converted to a fife.Location
        @return: None
        """
        self.state = _AGENT_STATE_RUN
        boxLocation = tuple([int(float(i)) for i in location])
        l = fife.Location(self.behaviour.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(*boxLocation))
        self.behaviour.agent.move('run', l, self.behaviour.speed)
        self.atBox = True

class NPCBehaviour(ActorBehaviour):
    def __init__(self, Parent = None):
        super(NPCBehaviour, self).__init__()
        
        self.parent = Parent
        self.state = _AGENT_STATE_NONE
        
        # hard code this for now
        self.distRange = (2, 4)
        
    def getTargetLocation(self):
        """@rtype: fife.Location
           @return: NPC's position"""
        x = self.getX()
        y = self.getY()
        if self.state == _AGENT_STATE_WANDER:
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
        if self.state == _AGENT_STATE_WANDER:
            self.targetLoc = self.getTargetLocation()
        self.idle()
        
    
    def idle(self):
        """Controls the NPC when it is idling. Different actions
           based on the NPC's state.
           @return: None"""
        if self.state == _AGENT_STATE_NONE:
            self.state = _AGENT_STATE_IDLE
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _AGENT_STATE_IDLE:
            self.targetLoc = self.getTargetLocation()
            self.state = _AGENT_STATE_WANDER
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _AGENT_STATE_WANDER:
            self.parent.wander(self.targetLoc)
            self.state = _AGENT_STATE_NONE
        elif self.state == _AGENT_STATE_TALK:
            self.agent.act('stand', self.pc.getLocation())

class NonPlayerCharacter(GameObject, Living, Scriptable, CharStats):
    """
    NPC class
    """
    def __init__(self, ID, agent_layer = None, name = 'NPC', \
                 text = 'A nonplayer character', **kwargs):
        # init game object
        super(NonPlayerCharacter, self).__init__(ID, **kwargs)
        self.is_NPC = True
        self.inventory = None
        self.agent_layer = agent_layer
        
        self.behaviour = NPCBehaviour(self)

    def getLocation(self):
        """ Get the NPC's position as a fife.Location object. Basically a
            wrapper.
            @rtype: fife.Location
            @return: the location of the NPC"""
        return self.behaviour.agent.getLocation()
    
    def wander(self, location):
        """Nice slow movement for random walking.
           @type location: fife.Location
           @param location: Where the NPC will walk to.
           @return: None"""
        self.behaviour.agent.move('walk', location, self.behaviour.speed-1)

    def run(self, location):
        """Faster movement than walk.
           @type location: fife.Location
           @param location: Where the NPC will run to."""
        self.behaviour.agent.move('run', location, self.behaviour.speed+1)

    def talk(self):
        """ Makes the NPC ready to talk to the PC
            @return: None"""
        self.state = _AGENT_STATE_TALK
        self.behaviour.idle()
    
    def setup(self):
        """@return: None"""
        self.behaviour.attachToLayer(self.agent_layer, self.ID)

    def start(self):
        """@return: None"""
        self.behaviour.idle()