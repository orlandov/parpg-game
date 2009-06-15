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
from agents.hero import Hero
from agents.npc import NPC
from objects import GameObject
from objLoader import LocalXMLParser

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

class MapDoor:
    """A MapDoor is an item that when clicked transports the player to
       another map"""
    def __init__(self, name, new_map, location):
        """@type name: string
           @param name: name of fife object
           @type new_map: string
           @param new_map: name of new map
           @type location: tuple
           @param location: where to put the PC when map is loaded
           @return: None"""
        self.id = name
        self.map = "maps/"+new_map+".xml"
        # location is an (int, int) which stores the intended location 
        # of the PC on the new map
        self.targ_coords = location

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
        # a World object
        self.view = view
        self.PC = None
        self.npcs = []
        self.objects = []
        self.doors = []
        self.PC_targLoc = None

    def reset(self):
        """Clears the data on a map reload so we don't have objects/npcs from
           other maps hanging around.
           @return: None"""
        self.PC = None
        self.npcs = []
        self.objects = []
        self.doors = []

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
        objects_file.close()
        return True

    def addPC(self,pc):
        """Add the PC to the world
           @type pc: list
           @param pc: List of data for PC attributes
           @return: None"""
        if self.PC_targLoc:
            self.view.addObject(float(self.PC_targLoc[0]), \
                    float(self.PC_targLoc[1]), "PC", "PC")
            self.PC_targLoc = None
        else:
            self.view.addObject(float(pc[0]), float(pc[1]),"PC","PC")
        self.PC = Hero("PC", self.view.agent_layer)
        # ensure the PC starts on a default action
        self.PC.start()
        self.view.addPC(self.PC.agent)

    def addObjects(self,objects):
        """Add all of the objects we found into the fife map
           and into our class. An NPC is just an object to FIFE
           @type objects: list
           @param objects: List of objects to add
           @return: None"""
        for i in objects:
            # is it visible?
            if(i[0] == True):
                self.view.addObject(float(i[1]), float(i[2]), i[3], i[4])
            # now add it as an engine object
            self.objects.append(GameObject(i))

    def addNPCs(self,npcs):
        """Add all of the NPCs we found into the fife map to FIFE.
           @type npcs: list
           @param npcs: List of NPC's to add
           @return: None"""
        for i in npcs:
            self.view.addObject(float(i[0]), float(i[1]), i[2], i[3])
            # now add as engine data
            self.npcs.append(NPC(i[4], str(i[3]), self.view.agent_layer))
            self.npcs[-1].start()

    def addDoors(self, doors):
        """Add all the doors to the map as well.
           As an object they will have already been added.
           @type doors: list
           @param doors: List of doors
           @return: None"""
        for i in doors:
            self.doors.append(MapDoor(i[0], i[1], i[2]))

    def objectActive(self, ident):
        """Given the objects ID, pass back the object if it is active,
           False if it doesn't exist or not displayed
           @type ident: string
           @param ident: ID of object
           @rtype: boolean
           @return: Status of result (True/False)"""
        for i in self.objects:
            if((i.display == True)and(i.id == ident)):
                # we found a match
                return i
        # now try NPC's
        for i in self.npcs:
            # all NPC's are deemed active
            if(i.id == ident):
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
        # is it an NPC?
        for i in self.npcs:
            if(obj_id == i.id):
                # keep it simple for now
                actions.append(("Talk",None))
                actions.append(("Attack",None))     
        # is it a door?
        for i in self.doors:
            if(obj_id == i.id):
                # load the new map
                self.PC_targLoc = i.targ_coords
                self.loadMap(str(i.map))
                return None
        # is it in our objects?
        for i in self.objects:
            if(obj_id == i.id):
                actions.append(("Examine",None))
                # is it a container?
                if(i.container == True):
                    actions.append(("Open",None))
                # can you pick it up?
                if(i.carry == True):
                    actions.append(("Pick Up",None))
                #return actions
        #return actions

    def loadMap(self,map_file):
        """Load a new map. TODO: needs some error checking
           @type map_file: string
           @param map_file: Name of map file to load
           @return: None"""
        # first we let FIFE load the rest of the map
        self.view.load(map_file)
        # then we update FIFE with the PC, NPC and object details
        self.reset()
        self.loadObjects(map_file[:-4]+"_objects.xml")

    def handleMouseClick(self,position):
        """Code called when user left clicks the screen.
           @type position: fife.ScreenPoint
           @param position: Screen position of click
           @return: None"""
        self.PC.run(position)

