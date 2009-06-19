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

from agents.npc import NPC

class SavedData(object):
    """ SavedData holds data that can be passed to Engine in the addPC, addNPCs,
        etc. functions."""

    def __init__(self, PC, npcs, objects, doors):
        """ Creates a new SavedData object.
            @type PC: list
            @param PC: a list of the x y coordinates of the PC
            @type npcs: dict
            @param npcs: {npc identifier : npc list info as LocalXMLParser}
            @type objects: dict
            @param objects: {object id : object list info as LocalXMLParser}
            @type doors: dict
            @param doors: {door id : door list info as LocalXMLParser}
            @return: None"""
        # PC = [xposition, yposition]
        self.PC = PC
        # one NPC = [xpos, ypos, gfx, ident, text]
        self.npcs = npcs
        # one object (if visible) = [True, xpos, ypos, gfx, ident, text,
        #   contain, carry]
        # one object (if not visible) = [False, gfx, ident, text, owner,
        #   contain, carry]
        self.objects = objects
        # one door = [id, target map, (xpos, ypos)]
        self.doors = doors

    def getNPC(self, ident):
        """ Attempts to find a specific npc in the npc dictionary
            @type ident: string
            @param ident: the identifier of the npc we're looking for
            @return: the list of npc information if found, False otherwise"""
        return self.npcs.get(ident, False)

    def getPC(self):
        """ There's only one PC. Return it and throw an exception if it doesn't
            exist.
            @rtype: Hero
            @return: an instance of the Hero class"""
        if self.PC:
            return self.PC
        sys.stderr.write("Error: No PC defined.\n")
        sys.exit(False)
  
    def getList(self, target):
        """ Turn the a storage dict into a list readable by Engine.addX
            @type target: string
            @param target: can be "npcs", "objects", "doors"
            @return: a list of readable information"""
        if target == "npcs":
            return self.npcs.values()
        elif target == "objects":
            return self.objects.values()
        elif target == "doors":
            return self.doors.values()
        else:
            #TODO raise appropriate exception
            print "not acceptable target"

class Saver(object):
    """ Saver holds data that will be used for saving and loading maps and
        objects throughout the game. World has a copy of this class."""

    def __init__(self):
        """ Constructor for the saver.
            @return: None"""
        # { map_id - string : SavedData }
        self.maps = {}
        # cur_map is a string of the current filename
        self.curMap = None

    def addData(self, pc, npcs, objects, doors):
        """ Adds a new maps worth of data to the maps object.
            @type pc: list
            @param pc: a list of the x y coordinates of the PC
            @type npcs: list
            @param npcs: a list of various npc information as from .xml files
            @type objects: list
            @param objects: a list of various object info as from .xml files
            @type doors: list
            @param doors: a list of various door info as from .xml files
            @return: None"""
        if self.curMap != None:
            npcDict = {}
            for npc in npcs:
                npcDict[npc[3]] = npc
            objDict = {}
            for obj in objects:
                if obj[0]:
                    objDict[obj[4]] = obj
                else:
                    objDict[obj[2]] = obj
            doorDict = {}
            for door in doors:
                doorDict[door[0]] = door
            self.maps[self.curMap] = SavedData(pc, npcDict, objDict, doorDict)

    def setCurMap(self, map_name):
        """ Sets the name of the current map. The name is maps/x.xml.
            @type map_name: string
            @param map_name: The name of the map the PC is on
            @return: None"""
        self.curMap = map_name

    def getData(self, map_name):
        """ Checks to see if the saver has a requested map and returns it.
            Returns false if the map doesn't exist in the saver.
            @type map_name: string
            @param map_name: the name of the map to check for
            @return: the engine object or False"""
        if self.maps.has_key(map_name):
            return self.maps[map_name]
        return False
   
    def updatePC(self, PC):
        """ Updates the PC's information. We care about:
                - the PC's position
            TODO: care about other things! (hp, etc)
            @type PC: Hero
            @param PC: the PC
            @return: None"""
        pcInfo = self.maps[self.curMap].getPC()
        pcInfo[0] = PC.getX()
        pcInfo[1] = PC.getY()

    def updateNPCs(self, npcList):
        """ Updates all NPCs who have changed since the map was loaded.
            Right now, we care about:
                - the NPC position
            @type npcList: list
            @param npcList: list of members of NPC class
            @return: None"""
        for npc in npcList:
            npcInfo = self.maps[self.curMap].getNPC(npc.id)
            if npcInfo:
                npcInfo[0] = npc.getX()
                npcInfo[1] = npc.getY()
