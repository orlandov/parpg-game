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
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from agents.hero import Hero
from agents.npc import NPC
from objects import GameObject

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

class LocalXMLParser(ContentHandler):
    """Class inherits from ContantHandler, and is used to parse the
       local objects data"""
    def __init__(self):
        self.search = "objects"
        self.pc = None
        self.objects = []
        self.npcs = []
    
    def startElement(self, name, attrs):
        """Called every time we meet a new element in the XML file"""
        # we are only looking for the 'layer' elements, the rest we ignore
        if(name == "PC"):
            # already have a PC?
            if(self.pc != None):
                sys.stderr.write("Error: 2 PC characters defined")
                sys.exit(False)
            # grab the data and store that as well
            try:
                xpos = attrs.getValue("xpos")
                ypos = attrs.getValue("ypos")
            except(KeyError):
                sys.stderr.write("Error: Data missing in PC definition")
                sys.exit(False)
            # store for later
            self.pc=[xpos,ypos]
        elif(name == "NPC"):
            # let's parse and add the data
            try:
                xpos=attrs.getValue("xpos")
                ypos = attrs.getValue("ypos")
                gfx = attrs.getValue("gfx")
                ident = attrs.getValue("id")
                text = attrs.getValue("text")
            except(KeyError):
                sys.stderr.write("Error: Data missing in NPC definition\n")
                sys.exit(False)
            # now we have the data, save it for later
            self.npcs.append([xpos, ypos, gfx, ident, text])
        elif(name == "object"):
            # same old same old
            try:
                xpos = attrs.getValue("xpos")
                ypos = attrs.getValue("ypos")
                gfx = attrs.getValue("gfx")
                ident = attrs.getValue("id")
                text = attrs.getValue("text")
            except(KeyError):
                sys.stderr.write("Error: Data missing in object definition\n")
                sys.exit(False)
            # now we have the data, save it for later
            self.objects.append([xpos, ypos, gfx, ident, text])

class Engine:
    """Engine holds the logic for the game
       Since some data (object position and so forth) is held in the
       fife, and would be pointless to replicate, we hold a instance of
       the fife view here. This also prevents us from just having a
       function heavy controller"""
    def __init__(self, view):
        self.view = view
        self.PC = None
        self.npcs = []
        self.objects = []

    def loadObjects(self, filename):
        """Load objects from the XML file
           Returns True if it worked, False otherwise"""
        try:
            objects_file = open(filename, 'rt')
        except(IOError):
            sys.stderr.write("Error: Can't find objects file\n")
            return False
        # now open and read the XML file
        parser = make_parser()
        cur_handler = LocalXMLParser()
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
        return True

    def addPC(self,pc):
        """Add the PC to the world"""
        self.view.addObject(float(pc[0]), float(pc[1]),"PC")
        self.PC = Hero("PC", self.view.agent_layer)
        # ensure the PC starts on a default action
        self.PC.start()
        self.view.addPC(self.PC.agent)

    def addObjects(self,objects):
        """Add all of the objects we found into the fife map
           and into our class
           An NPC is just an object to FIFE"""
        for i in objects:
            self.view.addObject(float(i[0]), float(i[1]), i[2])
            # now add it as an engine object
            self.objects.append(GameObject(int(float(i[0])),
                                           int(float(i[1])), i[3], i[4]))

    def addNPCs(self,npcs):
        """Add all of the NPCs we found into the fife map
           and into this class"""
        for i in npcs:
            self.view.addObject(float(i[0]), float(i[1]), i[2])
            # now add as engine data
            self.npcs.append(NPC(int(float(i[0])), int(float(i[1])),
                                 i[3], i[4]))

    def getObjectString(self, xpos, ypos):
        """Get the objects description of itself"""
        # cycle through all of the objects; do we have something there?
        for i in self.objects:
            if((xpos == i.xpos)and(ypos == i.ypos)):
                # yes, we have a match, so return the text
                return i.text
        for i in self.npcs:
            if((xpos == i.xpos)and(ypos == i.ypos)):
                # yes, we have a match, so return the text
                return i.text
        # nothing, but return the empty string in case we print it
        return ""

    def loadMap(self,map_file):
        """Load a new map
           TODO: needs some error checking"""
        # first we let FIFE load the rest of the map
        self.view.load(map_file)
        # then we update FIFE with the PC, NPC and object details
        self.loadObjects(map_file[:-4]+"_objects.xml")

    def handleMouseClick(self,position):
        self.PC.run(position)

