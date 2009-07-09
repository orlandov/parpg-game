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

class ObjectXMLParser(ContentHandler):
    """ObjectXMLParser call constructors to make GameObjects using information
       provided in _objects.xml files."""
    def __init__(self):
        """Initializes the ObjectXMLParser."""
        # local_info is a list of dictionaries. When startElement is called 
        # (through code in the scripts.Engine), this list is populated.
        self.local_info = []
        # parser is created when getObjects is called.
        self.parser = None
    
    def getObjects(self, file_desc):
        """Reads the object data into dictionaries out of which
        the game objects can be constructed.
           @type file_desc: File
           @param file_desc: an open file from which we read
           @return: None"""
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(file_desc)
        self.agent_layer = None

    def startElement(self, name, attrs):
        """Called every time we meet a new element in the XML file. This
           function is specified in ContentHandler, and is called by the parser.
           @type name: string
           @param name: XML element?
           @type attrs: ???
           @param attrs: XML attributes
           @return: None"""
        # For now, only looking for game_obj things
        if str(name) == "object":
            obj_info = {}
            # we need to convert all the unicode strings to ascii strings
            for key, val in attrs.items():
                obj_info[str(key)] = str(val)
            self.local_info.append(obj_info)
