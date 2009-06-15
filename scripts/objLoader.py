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

class LocalXMLParser(ContentHandler):
    """Class inherits from ContantHandler, and is used to parse the
       local objects data"""
    def __init__(self):
        self.search = "objects"
        self.pc = None
        self.objects = []
        self.npcs = []
        self.doors = []
        self.visuals = []
        # create unique names for all of the visuals
        self.visual_count = 0
    
    def getParser(self):
        """Simple one liner to remove XML dependencies in engine.py"""
        return make_parser()
    
    def getObject(self, attrs):
        """Grab the object details from the XML"""
        try:
            display = attrs.getValue("display")
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
        if(display == "True"):
            self.objects.append([True, xpos, ypos, gfx, ident,
                                 text, contain, carry])
        else:
            self.objects.append([False, gfx, ident, text,
                                 owner, contain, carry])

    def getDoor(self, attrs):
        """Grab door data"""
        try:
            display = attrs.getValue("display")
            if(display == "True"):
                xpos = attrs.getValue("xpos")
                ypos = attrs.getValue("ypos")
            else:
                owner = attrs.getValue("owner")
            gfx = attrs.getValue("gfx")
            ident = attrs.getValue("id")
            text = attrs.getValue("text")
        except(KeyError):
            sys.stderr.write("Error: Data missing in door definition\n")
            sys.exit(False)
        # now we have the data, save it for later
        if(display == "True"):
            self.objects.append([True, xpos, ypos, gfx, ident,
                                 text, "0", "0"])
        else:
            self.objects.append([False, gfx, ident, text,
                                 owner, "0", "0"])

    def getVisual(self, attrs):
        """Visual elements are there just for the eye candy"""
        try:
            xpos = attrs.getValue("xpos")
            ypos = attrs.getValue("ypos")
            gfx = attrs.getValue("gfx")
        except(KeyError):
            sys.stderr.write("Error: Data missing in visual definition\n")
            sys.exit(False)
        name = "visual-"+str(self.visual_count)
        self.visual_count += 1
        self.visuals.append([xpos,ypos,gfx,name])
  
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
            self.getObject(attrs)
        elif(name == "visual"):
            self.getVisual(attrs)
        elif(name == "door"):
            # firstly, add the object
            self.getDoor(attrs)
            # then save the other data
            try:
                new_map = attrs.getValue("map")
                txpos = attrs.getValue("txpos")
                typos = attrs.getValue("typos")
            except(KeyError):
                sys.stderr.write("Error: Door has no map or no target!\n")
                sys.exit(False)
            # format is [id,map_name,target coords on new map]
            self.doors.append([self.objects[-1][4],new_map, \
                    tuple([txpos, typos])])
