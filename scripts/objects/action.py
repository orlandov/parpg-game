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
    def __init__(self, engine, targetmapname, targetmapfile , targetpos):
        """Initiates a change of the position of the character
           possibly flagging a new map to be loaded.
           @type engine: Engine reference
           @param engine: A reference to the engine.
           @type targetmapname: String
           @param targetmapname: Target map id 
           @type targetmapfile: String
           @param targetmapfile: Target map filename
           @type targetpos: Tuple
           @param targetpos: (X, Y) coordinates on the target map.
           @return: None"""
        self.engine = engine
        self.targetpos = targetpos
        self.targetmapname = targetmapname
        self.targetmapfile = targetmapfile

    def execute(self):
        """Executes the mapchange."""
        self.engine.changeMap(self.targetmapname, self.targetmapfile, self.targetpos)
       
class OpenBoxAction(Action):
    """Open a box. Needs to be more generic, but will do for now."""
    def __init__(self, engine, boxTitle):
        """@type engine: Engine reference
           @param engine: A reference to the engine.
           @type boxTitle: String
           @param boxTitle: Box title.
           """
        self.engine = engine
        self.boxTitle = boxTitle
    
    def execute(self):
        """Open the box."""
        self.engine.view.hud.createBoxGUI(self.boxTitle)
        
class ExamineBoxAction(Action):
    """Examine a box. Needs to be more generic, but will do for now."""
    def __init__(self, engine, examineName, examineDesc):
        """@type engine: Engine reference
           @param engine: A reference to the engine.
           @type examineName: String
           @param examineName: Name of the object to be examined.
           @type examineName: String
           @param examineName: Description of the object to be examined.
           """
        self.engine = engine
        self.examineName = examineName
        self.examineDesc = examineDesc
        
    def execute(self):
        """Examine the box."""
        self.engine.view.hud.createExamineBox(self.examineName, self.examineDesc)

class TalkAction(Action):
    """An action to represent starting a dialogue"""
    def __init__(self, engine, npc):
        """@type engine: Engine reference
           @param engine: A reference to the engine.
           @type examineName: String
           @param examineName: Name of the object to be examined.
           @type examineName: String
           @param examineName: Description of the object to be examined.
           """
        self.engine = engine
        self.npc = npc
        
    def execute(self):
        """Examine the box."""
        pc = self.engine.gameState.PC
        pc.behaviour.agent.act('stand', self.npc.getLocation())
        self.npc.talk(pc)
        self.engine.view.hud.showDialogue(self.npc)
