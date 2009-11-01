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

class Action(object):
    """Base Action class, to define the structure"""
    def execute(self):
        """To be overwritten"""
        pass

class ChangeMapAction(Action):
    """A change map scheduled"""
    def __init__(self, engine, target_map_name, target_map_file , target_pos):
        """Initiates a change of the position of the character
           possibly flagging a new map to be loaded.
           @type engine: Engine reference
           @param engine: A reference to the engine.
           @type target_map_name: String
           @param target_map_name: Target map id 
           @type target_map_file: String
           @param target_map_file: Target map filename
           @type target_pos: Tuple
           @param target_pos: (X, Y) coordinates on the target map.
           @return: None"""
        self.engine = engine
        self.target_pos = target_pos
        self.target_map_name = target_map_name
        self.target_map_file = target_map_file

    def execute(self):
        """Executes the map change."""
        self.engine.changeMap(self.target_map_name, self.target_map_file,\
                              self.target_pos)
       
class OpenBoxAction(Action):
    """Open a box. Needs to be more generic, but will do for now."""
    def __init__(self, engine, box_title):
        """@type engine: Engine reference
           @param engine: A reference to the engine.
           @type box_title: String
           @param box_title: Box title.
           """
        self.engine = engine
        self.box_title = box_title
    
    def execute(self):
        """Open the box."""
        self.engine.view.hud.createBoxGUI(self.box_title)
        
class ExamineBoxAction(Action):
    """Examine a box. Needs to be more generic, but will do for now."""
    def __init__(self, engine, examine_name, examine_desc):
        """@type engine: Engine reference
           @param engine: A reference to the engine.
           @type examine_name: String
           @param examine_name: Name of the object to be examined.
           @type examine_name: String
           @param examine_name: Description of the object to be examined.
           """
        self.engine = engine
        self.examine_name = examine_name
        self.examine_desc = examine_desc
        
    def execute(self):
        """Examine the box."""
        self.engine.view.hud.createExamineBox(self.examine_name, \
                                              self.examine_desc)

class TalkAction(Action):
    """An action to represent starting a dialogue"""
    def __init__(self, engine, npc):
        """@type engine: Engine reference
           @param engine: A reference to the engine.
           @type npc: NonPlayerCharacter
           @param npc: NPC to interact with.
           """
        self.engine = engine
        self.npc = npc
        
    def execute(self):
        """Talk with the NPC when we are close enough, otherwise
           we move close.
           @return: None"""
        
        pc = self.engine.game_state.PC
        npc_coordinates = self.npc.getLocation().getLayerCoordinates()
        pc_coordinates = pc.behaviour.agent.getLocation().getLayerCoordinates()
        
        distance_squared = (npc_coordinates.x - pc_coordinates.x) *\
                         (npc_coordinates.x - pc_coordinates.x) +\
                         (npc_coordinates.y - pc_coordinates.y) *\
                         (npc_coordinates.y - pc_coordinates.y)
        
        
        # If we are too far away, we approach the NPC again
        if distance_squared > 2:
            pc.approach([self.npc.getLocation().\
                         getLayerCoordinates().x, \
                         self.npc.getLocation().\
                         getLayerCoordinates().y], \
                        TalkAction(self.engine,\
                                   self.npc))        
        else:
            pc.behaviour.agent.act('stand', self.npc.getLocation())
    
            if self.npc.dialogue is not None:
                self.npc.talk(pc)
                self.engine.view.hud.showDialogue(self.npc)
            else:
                self.npc.behaviour.agent.say("Leave me alone!", 1000)
                
            self.engine.game_state.PC.behaviour.idle()
            self.engine.game_state.PC.nextAction = None 
