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
        self.tele_tiles = []
    
    def getParser(self):
        """Simple one liner to remove XML dependencies in engine.py"""
        return make_parser()
    
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
        elif name == "tele_tile":
            try:
                target = attrs.getValue("target")
                xpos = attrs.getValue("xpos")
                ypos = attrs.getValue("ypos")
                txpos = attrs.getValue("txpos")
                typos = attrs.getValue("typos")
            except(KeyError):
                sys.stderr.write("Error: Data missing in \
                        tele_tile definition\n")
                sys.exit(False)
            self.tele_tiles.append([target, tuple([int(xpos), int(ypos)]), \
                    tuple([int(txpos), int(typos)])])

