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
import pickle, sys
from agents.hero import Hero
from agents.npc import NPC
from objLoader import LocalXMLParser
from saver import Saver
from gamestate import GameState
from gamedata import *

# design note:
# there is a map file that FIFE reads. We use that file for half the map
# format because the map editor in FIFE uses it, and secondly because it
# save us writing a bunch of new code.
# However, the objects and characters on a map are liable to change
# whilst the game is being run, so when we change the map, we need to
# to grab the objects and npc data EITHER from the engine state, or grab
# from another file if in their initial state
# This other file has the name AAA_objects.xml where AAA.xml is the name
# of the original mapfile.

class Engine:
    """Engine holds the logic for the game.
       Since some data (object position and so forth) is held in the
       fife, and would be pointless to replicate, we hold a instance of
       the fife view here. This also prevents us from just having a
       function heavy controller."""
    
    def __init__(self, view):
        """Initialise the instance.
           @type view: world
           @param view: A world instance
           @return: None"""
        # a World object (the fife stuff, essentially)
        self.view = view
        self.doors = {}
        self.npcs = []
        self.PC = None
        self.mapchange = False
        self.gameState = GameState()

    def reset(self):
        """Clears the data on a map reload so we don't have objects/npcs from
           other maps hanging around.
           @return: None"""
        self.PC = None
        self.npcs = []
        self.doors = {}

    def save(self, path, filename):
        """Writes the saver to a file.
           @type filename: string
           @param filename: the name of the file to write to
           @return: None"""
        self.updateGameState()
        fname = '/'.join([path,filename])
        try:
            f = open(fname, 'w')
        except(IOError):
            sys.stderr.write("Error: Can't find save game: " + fname + "\n")
            return
        pickle.dump(self.gameState, f)
        f.close()

    def load(self, path, filename):
        """Loads a saver from a file.
           @type filename: string
           @param filename: the name of the file to load from
           @return: None"""
        fname = '/'.join([path, filename])
        try:
            f = open(fname, 'r')
        except(IOError):
            sys.stderr.write("Error: Can't find save game file\n")
            return
        self.gameState = pickle.load(f)
        f.close()
        if self.gameState.currentMap:
            self.loadMap(self.gameState.currentMap)
            
    def updateGameState(self):
        """Stores the current pc and npcs positons in the game state."""
        # save the PC position
        self.gameState.PC.posx = self.PC.getX()
        self.gameState.PC.posy = self.PC.getY()
        #save npc positions
        for i in self.npcs:
            if str(i.id) in self.gameState.objects:
                self.gameState.getObjectById(str(i.id)).posx = i.getX()
                self.gameState.getObjectById(str(i.id)).posy = i.getY()

    def loadObjects(self, filename):
        """Load objects from the XML file
           Returns True if it worked, False otherwise.
           @type filename: string
           @param filename: The XML file to read.
           @rtype: boolean
           @return: Status of result (True/False)"""
        try:
            objects_file = open(filename, 'rt')
        except(IOError):
            sys.stderr.write("Error: Can't find objects file\n")
            return False
        # now open and read the XML file
        cur_handler = LocalXMLParser()
        parser = cur_handler.getParser()
        parser.setContentHandler(cur_handler)
        parser.parse(objects_file)
        objects_file.close()
        # must have at least 1 PC
        if(cur_handler.pc == None):
            sys.stderr.write("Error: No PC defined\n")
            sys.exit(False)
        # now add to the map and the engine
        self.addPC(cur_handler.pc)
        self.addNPCs(cur_handler.npcs)
        self.addObjects(cur_handler.objects)
        self.addDoors(cur_handler.doors)
        return True

    def addPC(self,pc):
        """Add the PC to the world
           @type pc: list
           @param pc: List of data for PC attributes
           @return: None"""
        # sync with game data
        if self.gameState.PC:
            # use existing position
            posx = self.gameState.PC.posx
            posy = self.gameState.PC.posy
        else:
            posx = pc[0]
            posy = pc[1]
            # save the new PC to the game data
            self.gameState.PC = HeroData("PC", posx, posy, "PC", self.gameState.currentMap)
        # add to game data    
        self.view.addObject(float(posx), float(posy),"PC","PC")
         # create the PC agent
        self.PC = Hero("PC", self.view.agent_layer, self)
        self.PC.start()
        self.view.addPC(self.PC.agent)

    def addObjects(self,objects):
        """Add all of the objects we found into the fife map
           and into our class. An NPC is just an object to FIFE
           @type objects: list
           @param objects: List of objects to add
           @return: None"""
        for i in objects:
            # already in game data?
            ref = self.gameState.getObjectById(i.id)
            if ref is None:
                # no, add it to the game state
                i.map_id = self.gameState.currentMap
                self.gameState.objects[i.id] = i
            else:
                # yes, use the current game state data
                i.posx = ref.posx
                i.posy = ref.posy
                i.gfx = ref.gfx        
            # is it visible?
            if i.display:
                self.view.addObject(i.posx, i.posy, i.gfx, i.id)

    def addNPCs(self,npcs):
        """Add all of the NPCs we found into the fife map to FIFE.
           @type npcs: list
           @param npcs: List of NPC's to add
           @return: None"""
        for i in npcs:
            # already in the game data?
            ref = self.gameState.getObjectById(i.id) 
            if ref is None:
                # no, add it to the game state
                i.map_id = self.gameState.currentMap
                self.gameState.objects[i.id] = i
            else:
                # yes, use the current game state data
                i.posx = ref.posx
                i.posy = ref.posy
                i.gfx = ref.gfx              
            # add it to the view
            self.view.addObject(i.posx, i.posy, i.gfx, i.id)          
            # create the agent
            self.npcs.append(NPC(i.text, str(i.id), self.view.agent_layer))
            self.npcs[-1].start()

    def addDoors(self, doors):
        """Add all the doors to the map as well.
           As an object they will have already been added.
           @type doors: list
           @param doors: List of doors
           @return: None"""
        for i in doors:
            self.doors[str(i.id)] = MapDoor(i.id, i.destmap, (i.destx, i.desty))

    def objectActive(self, ident):
        """Given the objects ID, pass back the object if it is active,
           False if it doesn't exist or not displayed
           @type ident: string
           @param ident: ID of object
           @rtype: boolean
           @return: Status of result (True/False)"""
        for i in self.gameState.getObjectsFromMap(self.gameState.currentMap):
            if i.display and (i.id == ident):
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
        actions=[]
        # note: ALWAYS check NPC's first!
        for i in self.gameState.getObjectsFromMap(self.gameState.currentMap):
            if(obj_id == i.id):
                if isinstance(i, NpcData):
                    # keep it simple for now, None to be replaced by callbacks
                    actions.append(["Talk", "Talk", self.initTalk, i])
                    actions.append(["Attack", "Attack", self.nullFunc, i]) 
                elif isinstance(i, DoorData):
                    actions.append(["Change Map", "Change Map", \
                            self.PC.approachDoor, [i.posx, i.posy], \
                            self.doors[str(i.id)].map, [i.destx, i.desty]])
                elif isinstance(i, NonLivingObjectData):
                    actions.append(["Examine", "Examine", self.nullFunc, i])
                    # is it a container?
                    if(i.container == True):
                        actions.append(["Open", "Open", self.view.createBoxGUI, i])
                    # can you pick it up?
                    if(i.carryable == True):
                        actions.append(["Pick Up", "Pick Up", self.nullFunc, i])       
        return actions
    
    def nullFunc(self, userdata):
        """Sample callback for the context menus."""
        print userdata
    
    def initTalk(self, npcInfo):
        """ Starts the PC talking to an NPC. """
        # TODO: work more on this when we get NPCData and HeroData straightened
        # out
        for npc in self.gameState.npcs:
            if str(npcInfo.id) == npc.id:
                npc.talk()
                break
        self.PC.approachNPC(npc.getLocation())

    def loadMap(self, map_file):
        """Load a new map. TODO: needs some error checking
           @type map_file: string
           @param map_file: Name of map file to load
           @return: None"""
        # then we let FIFE load the rest of the map
        self.view.load(str(map_file))
        # then we update FIFE with the PC, NPC and object details
        self.reset()
        self.gameState.currentMap = map_file
        self.loadObjects(map_file[:-4] + "_objects.xml")

    def handleMouseClick(self,position):
        """Code called when user left clicks the screen.
           @type position: fife.ScreenPoint
           @param position: Screen position of click
           @return: None"""
        self.PC.run(position)
        
    def changeMap(self, map, targetPosition):
        """Registers for a mapchange on the next pump().
           @type map: ???
           @param map: Name of the target map.
           @type targetPosition: ???
           @param targetPosition: Position of PC on target map.
           @return: None"""
        # save the postions
        self.updateGameState()
        # set the PC position
        self.gameState.PC.posx = targetPosition[0]
        self.gameState.PC.posy = targetPosition[1]
        # set the parameters for the mapchange
        self.targetMap = map
        # issue the mapchange
        self.mapchange = True

    def handleCommands(self):
        if self.mapchange:
            self.loadMap(self.targetMap)
            self.mapchange = False

    def pump(self):
        """Main loop in the engine."""
        self.handleCommands()

