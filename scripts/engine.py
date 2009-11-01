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

# there should be NO references to FIFE here!
import pickle
import sys
from gamestate import GameState
from objects import *
from objects.action import *


class Engine:
    """Engine holds the logic for the game.
       Since some data (object position and so forth) is held in the
       fife, and would be pointless to replicate, we hold a instance of
       the fife view here. This also prevents us from just having a
       function heavy controller."""
    
    def __init__(self, view):
        """Initialize the instance.
           @type view: world
           @param view: A world instance
           @return: None"""
        # a World object (the fife stuff, essentially)
        self.view = view
        self.map_change = False
        self.load_saver = False
        self.savegame = None
        self.game_state = GameState()
        self.pc_run = 1
        self.target_position = None
        self.target_map_name = None
        self.target_map_file = None

    def save(self, path, filename):
        """Writes the saver to a file.
           @type filename: string
           @param filename: the name of the file to write to
           @return: None"""
        fname = '/'.join([path, filename])
        try:
            f = open(fname, 'wb')
        except(IOError):
            sys.stderr.write("Error: Can't find save game: " + fname + "\n")
            return
        
        # save the PC coordinates before we destroy the behaviour
        coords = self.game_state.PC.behaviour.agent.getLocation().\
                    getMapCoordinates()
        self.game_state.saved_pc_coordinates = (coords.x, coords.y)
        
        # can't pickle SwigPyObjects
        behaviours = {}
        behaviour_player = self.game_state.PC.behaviour
        self.game_state.PC.behaviour = None
        
        # Backup the behaviours 
        for map_id in self.game_state.objects:
            behaviours[map_id] = {}
            for (object_id, npc) in self.game_state.objects[map_id].items():
                if npc.trueAttr("NPC"):
                    behaviours[map_id][object_id] = npc.behaviour
                    npc.behaviour = None
        
        # Pickle it 
        pickle.dump(self.game_state, f)
        f.close()
        
        # Restore behaviours
        for map_id in behaviours:
            for (object_id, behaviour) in behaviours[map_id].items():
                self.game_state.objects[map_id][object_id].behaviour = \
                    behaviours[map_id][object_id]
                
        self.game_state.PC.behaviour = behaviour_player

    def load(self, path, filename):
        """Loads a saver from a file.
           @type filename: string
           @param filename: the name of the file (including path) to load from
           @return: None"""
            
        fname = '/'.join([path, filename])

        try:
            f = open(fname, 'rb')
        except(IOError):
            sys.stderr.write("Error: Can't find save game file\n")
            return
        
        #Remove all currently loaded maps so we can start fresh
        self.view.deleteMaps();
        
        self.game_state = pickle.load(f)
        f.close()
        
        # Recreate all the behaviours. These can't be saved because FIFE
        # objects cannot be pickled
        for map_id in self.game_state.objects:
            for (object_id, npc) in self.game_state.objects[map_id].items():
                if npc.trueAttr("NPC"):
                    npc.createBehaviour(self.view.active_map.agent_layer)

        # Fix the player behaviour
        self.game_state.PC.createBehaviour(self.view.active_map.agent_layer)
        
        #In most maps we'll create the PC Instance internally. In these
        #cases we need a target position
        self.target_position = self.game_state.saved_pc_coordinates
        
        #Load the current map
        if self.game_state.current_map_file:
            self.loadMap(self.game_state.current_map_name, \
                         self.game_state.current_map_file) 
            
    def createObject (self, layer, attributes, instance):
        """Create an object and add it to the current map.
           @type layer: fife.Layer
           @param layer: FIFE layer object exists in
           @type attributes: Dictionary
           @param attributes: Dictionary of all object attributes
           @type instance: fife.Instance
           @param instance: FIFE instance corresponding to the object
           @return: None
        """
        # create the extra data
        extra = {}
        extra['agent_layer'] = layer
        extra['engine'] = self
        
        obj = createObject(attributes, extra)
        
        if obj.trueAttr("PC"):
            self.addPC(layer, obj, instance)
        else:
            self.addObject(layer, obj, instance)

        

    def addPC(self, layer, pc, instance):
        """Add the PC to the map
           @type layer: fife.Layer
           @param layer: FIFE layer object exists in
           @type pc: PlayerCharacter
           @param pc: PlayerCharacter object
           @type instance: fife.Instance
           @param instance: FIFE instance of PC
           @return: None
        """
        # For now we copy the PC, in the future we will need to copy
        # PC specifics between the different PC's
        self.game_state.PC = pc
        self.game_state.PC.setup()

    def addObject(self, layer, obj, instance):
        """Adds an object to the map.
           @type layer: fife.Layer
           @param layer: FIFE layer object exists in
           @type obj: GameObject
           @param obj: corresponding object class
           @type instance: fife.Instance
           @param instance: FIFE instance of object
           @return: None
        """

        ref = self.game_state.getObjectById(obj.ID, \
                                            self.game_state.current_map_name) 
        if ref is None:
            # no, add it to the game state
            self.game_state.objects[self.game_state.current_map_name][obj.ID] \
                                                                          = obj
        else:
            # yes, use the current game state data
            obj.X = ref.X
            obj.Y = ref.Y
            obj.gfx = ref.gfx  
             
        if obj.trueAttr("NPC"):
            # create the agent
            obj.setup()
            
            # create the PC agent
            obj.start()

    def objectActive(self, ident):
        """Given the objects ID, pass back the object if it is active,
           False if it doesn't exist or not displayed
           @type ident: string
           @param ident: ID of object
           @rtype: boolean
           @return: Status of result (True/False)"""
        for i in \
           self.game_state.getObjectsFromMap(self.game_state.current_map_name):
            if (i.ID == ident):
                # we found a match
                return i
        # no match
        return False

    def getItemActions(self, obj_id):
        """Given the objects ID, return the text strings and callbacks.
           @type obj_id: string
           @param obj_id: ID of object
           @rtype: list
           @return: List of text and callbacks"""
        actions = []
        # note: ALWAYS check NPC's first!
        obj = self.game_state.getObjectById(obj_id, \
                                            self.game_state.current_map_name)
        
        if obj is not None:
            if obj.trueAttr("NPC"):
                # keep it simple for now, None to be replaced by callbacks
                actions.append(["Talk", "Talk", self.initTalk, obj])
                actions.append(["Attack", "Attack", self.nullFunc, obj])
            else:
                actions.append(["Examine", "Examine", \
                                self.game_state.PC.approach, [obj.X, obj.Y], \
                                ExamineBoxAction(self, obj.name, obj.text)])
                # is it a Door?
                if obj.trueAttr("door"):
                    actions.append(["Change Map", "Change Map", \
                       self.game_state.PC.approach, [obj.X, obj.Y], \
                            ChangeMapAction(self, obj.target_map_name, \
                                obj.target_map, obj.target_pos)])
                # is it a container?
                if obj.trueAttr("container"):
                    actions.append(["Open", "Open", 
                                    self.game_state.PC.approach, \
                                    [obj.X, obj.Y], \
                                    OpenBoxAction(self, "Box")])
                # can you pick it up?
                if obj.trueAttr("carryable"):
                    actions.append(["Pick Up", "Pick Up", self.nullFunc, obj])

        return actions
    
    def nullFunc(self, userdata):
        """Sample callback for the context menus."""
        print userdata
    
    def initTalk(self, npcInfo):
        """ Starts the PC talking to an NPC. """
        # TODO: work more on this when we get NPCData and HeroData straightened
        # out
        npc = self.game_state.getObjectById(npcInfo.ID, \
                                            self.game_state.current_map_name)
        self.game_state.PC.approach([npc.getLocation().\
                                     getLayerCoordinates().x, \
                                     npc.getLocation().\
                                     getLayerCoordinates().y], \
                                    TalkAction(self, npc))

    def loadMap(self, map_name, map_file):
        """Load a new map.
           @type map_name: string
           @param map_name: Name of the map to load
           @type map_file: string
           @param map_file: Filename of map file to load
           @return: None"""
        self.game_state.current_map_file = map_file
        self.game_state.current_map_name = map_name
        self.view.loadMap(map_name, str(map_file))

        # create the PC agent
        self.view.active_map.addPC()
        self.game_state.PC.start()

    def handleMouseClick(self, position):
        """Code called when user left clicks the screen.
           @type position: fife.ScreenPoint
           @param position: Screen position of click
           @return: None"""
        if(self.pc_run == 1):
            self.game_state.PC.run(position)
        else:
            self.game_state.PC.walk(position)

    def changeMap(self, map_name, map_file, target_position):
        """Registers for a map change on the next pump().
           @type name_name: String
           @param map_name: Id of the map to teleport to
           @type map_file: String
           @param map_file: Filename of the map to teleport to
           @type target_position: Tuple
           @param target_position: Position of PC on target map.
           @return None"""
        # set the parameters for the map change if moving to a new map
        if map_name != self.game_state.current_map_name:
            self.target_map_name = map_name
            self.target_map_file = map_file
            self.target_position = target_position
            # issue the map change
            self.map_change = True
        else:
            #set the player position on the current map
            self.view.teleport(target_position)

    def handleCommands(self):
        if self.map_change:
            self.loadMap(self.target_map_name, self.target_map_file)
            self.view.teleport(self.target_position)
            self.map_change = False
        
        if self.load_saver:
            self.load(self.savegame)
            self.load_saver = False

    def pump(self):
        """Main loop in the engine."""
        self.handleCommands()
