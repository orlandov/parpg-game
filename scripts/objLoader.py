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

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import sys
from gamedata import *

class LocalXMLParser(ContentHandler):
    """Class inherits from ContantHandler, and is used to parse the
       local objects data"""
    def __init__(self):
        """Initialise the instance.
           @return: None"""
        self.search = "objects"
        self.pc = None
        self.objects = []
        self.npcs = []
        self.doors = []
    
    def getParser(self):
        """Simple one liner to remove XML dependencies in engine.py.
           @rtype: parser
           @return: A parser to work with"""
        return make_parser()
    
    def getObject(self, attrs):
        """Grab the object details from the XML data.
           @type attrs: ???
           @param attrs: XML attributes
           @return: None"""
        try:
            display = attrs.getValue("display")
            xpos, ypos = 0, 0
            owner = None
            if(display == "True"):
                xpos = attrs.getValue("xpos")
                ypos = attrs.getValue("ypos")
            else:
                owner = attrs.getValue("owner")
            gfx = attrs.getValue("gfx")
            ident = attrs.getValue("id")
            text = attrs.getValue("text")
            contain = attrs.getValue("contain")
            carry = attrs.getValue("carry")
        except(KeyError):
            sys.stderr.write("Error: Data missing in object definition\n")
            sys.exit(False)
        # now we have the data, save it for later
        self.objects.append(NonLivingObjectData(str(ident), float(xpos),
                            float(ypos), str(text), None, str(gfx),
                            str(display) == "True", str(owner),
                            str(contain) == "1", str(carry) == "1"))

    def getDoor(self, attrs):
        """Grab the door data.
           @type attrs: ???
           @param attrs: XML attributes
           @return: None"""
        try:
            display = attrs.getValue("display")
            xpos, ypos, xdest, ydest = 0, 0, 0, 0
            owner = None
            if(display == "True"):
                xpos = attrs.getValue("xpos")
                ypos = attrs.getValue("ypos")
            else:
                owner = attrs.getValue("owner")
            xdest = attrs.getValue("txpos")
            ydest = attrs.getValue("typos")
            gfx = attrs.getValue("gfx")
            ident = attrs.getValue("id")
            text = attrs.getValue("text")
            map = attrs.getValue("map")
        except(KeyError):
            sys.stderr.write("Error: Data missing in door definition\n")
            sys.exit(False)
        # now we have the data, save it for later
        door = DoorData(ident, xpos, ypos, text, None, gfx, display == "True",
                        owner, xdest, ydest, map)
        self.objects.append(door)
        self.doors.append(door)

    def startElement(self, name, attrs):
        """Called every time we meet a new element in the XML file
           @type name: string
           @param name: XML element?
           @type attrs: ???
           @param attrs: XML attributes
           @return: None"""
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
            self.npcs.append(NpcData(ident, xpos, ypos, text, None, gfx, True))
        elif(name == "object"):
            # same old same old
            self.getObject(attrs)
        elif(name == "door"):
            # firstly, add the object
            self.getDoor(attrs)

