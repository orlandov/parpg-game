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
from scripts import world
from base import *

"""All actors go here. Concrete classes only."""

__all__ = ["PlayerCharacter", "NonPlayerCharacter",]

TDS = Setting()
_AGENT_STATE_NONE, _AGENT_STATE_IDLE, _AGENT_STATE_APPROACH, _AGENT_STATE_RUN, _AGENT_STATE_WANDER, _AGENT_STATE_TALK = xrange(6)

class ActorBehaviour (fife.InstanceActionListener):
    """Fife agent listener
    """
    def __init__(self, layer):
        fife.InstanceActionListener.__init__(self)
        self.layer = layer
    
    def attachToLayer(self, agent_ID):
        """ Attaches to a certain layer
            @type agent_ID: String
            @param agent_ID: ID of the layer to attach to.
            @return: None
        """
        self.agent = self.layer.getInstance(agent_ID)
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
    def __init__(self, parent = None, layer = None):
        super(PCBehaviour, self).__init__(layer)
        
        self.parent = parent
        self.idle_counter = 1
        self.speed = float(TDS.readSetting("PCSpeed")) # TODO: rework/improve
        self.nextAction = None
        self.agent = None
        
    def onInstanceActionFinished(self, instance, action):
        """@type instance: ???
           @param instance: ???
           @type action: ???
           @param action: ???
           @return: None"""
        
        # First we reset the next behavior 
        act = self.nextAction
        self.nextAction = None 
        self.idle()
        
        if act:
            act.execute()
            
        if(action.getId() != 'stand'):
            self.idle_counter = 1
        else:
            self.idle_counter += 1
            
    def onNewMap(self, layer):
        """Sets the agent onto the new layer.
        """
        if self.agent is not None:
            self.agent.removeActionListener(self)
            
        self.agent = layer.getInstance(self.parent.ID)
        self.agent.addActionListener(self)
        self.state = _AGENT_STATE_NONE
        self.idle_counter = 1
    
    def idle(self):
        """@return: None"""
        self.state = _AGENT_STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation())

class PlayerCharacter (GameObject, Living, CharStats):
    """
    PC class
    """
    def __init__ (self, ID, agent_layer = None, **kwargs):
        GameObject.__init__( self, ID, **kwargs )
        Living.__init__( self, **kwargs )
        CharStats.__init__( self, **kwargs )

        self.is_PC = True
        
        # PC _has_ an inventory, he _is not_ one
        self.inventory = None
        
        self.state = _AGENT_STATE_NONE
        self.layer_id = agent_layer.getId()
        self.createBehaviour(agent_layer)
    
    def createBehaviour(self, layer):
        """ Creates the behaviour for this actor.
            @return None """
        self.behaviour = PCBehaviour(self, layer)
    
    def setup(self):
        """@return: None"""
        self.behaviour.attachToLayer(self.ID)

    def start(self):
        """@return: None"""
        self.behaviour.idle()
    
    def run(self, location):
        """Makes the PC run to a certain location
           @type location: fife.ScreenPoint
           @param location: Screen position to run to.
           @return: None"""
        self.state = _AGENT_STATE_RUN
        self.behaviour.agent.move('run', location, self.behaviour.speed+1)

    def walk(self, location):
        """Makes the PC walk to a certain location.
           @type location: fife.ScreenPoint
           @param location: Screen position to walk to.
           @return: None"""
        self.state = _AGENT_STATE_RUN
        self.behaviour.agent.move('walk', location, self.behaviour.speed-1)

    def teleport(self, location):
        """Teleports a PC instantly to the given location.
           @type location: fife.Location
           @param location: Target coordinates for PC.
           @return: None"""
        self.state = _AGENT_STATE_IDLE
        self.behaviour.agent.setLocation(location)

    def approach(self, location, action = None):
        """Approaches a location and then perform an action (if set).
           @type loc: fife.Location
           @param loc: the location to approach
           @type action: Action
           @param action: The action to schedule for execution after the approach.
           @return: None"""
        self.state = _AGENT_STATE_APPROACH
        self.behaviour.nextAction = action
        boxLocation = tuple([int(float(i)) for i in location])
        l = fife.Location(self.behaviour.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(*boxLocation))
        self.behaviour.agent.move('run', l, self.behaviour.speed)
        

class NPCBehaviour(ActorBehaviour):
    def __init__(self, Parent = None, Layer = None):
        super(NPCBehaviour, self).__init__(Layer)
        
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
            self.target_loc = self.getTargetLocation()
        self.idle()
        
    
    def idle(self):
        """Controls the NPC when it is idling. Different actions
           based on the NPC's state.
           @return: None"""
        if self.state == _AGENT_STATE_NONE:
            self.state = _AGENT_STATE_IDLE
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _AGENT_STATE_IDLE:
            self.target_loc = self.getTargetLocation()
            self.state = _AGENT_STATE_WANDER
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _AGENT_STATE_WANDER:
            self.parent.wander(self.target_loc)
            self.state = _AGENT_STATE_NONE
        elif self.state == _AGENT_STATE_TALK:
            self.agent.act('stand', self.pc.getLocation())

class NonPlayerCharacter(GameObject, Living, Scriptable, CharStats):
    """
    NPC class
    """
    def __init__(self, ID, agent_layer=None, name='NPC', \
                 text = 'A nonplayer character', **kwargs):
        # init game object
        GameObject.__init__(self, ID, name=name, **kwargs)
        Living.__init__(self, **kwargs)
        Scriptable.__init__(self, **kwargs)
        CharStats.__init__(self, **kwargs)

        self.is_NPC = True
        self.inventory = None
        self.layer_id = agent_layer.getId()
        self.createBehaviour(agent_layer)        
        self.dialogue = kwargs.get('dialogue')

    def createBehaviour(self, layer):
        """ Creates the behaviour for this actor.
            @return None """
        self.behaviour = NPCBehaviour(self, layer)

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

    def talk(self, pc):
        """ Makes the NPC ready to talk to the PC
            @return: None"""
        self.behaviour.state = _AGENT_STATE_TALK
        self.behaviour.pc = pc.behaviour.agent
        self.behaviour.idle()
    
    def setup(self):
        """@return: None"""
        self.behaviour.attachToLayer(self.ID)

    def start(self):
        """@return: None"""
        self.behaviour.idle()
