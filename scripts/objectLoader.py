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
from objects import getAllObjects
from objects.containers import *
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
        # an agent layer, which is set to something in getObjects and is set
        # to None at the end of getObjects to ensure that it is always current.
        self.agent_layer = None
    
    def getObjects(self, file_desc, a_layer):
        """Gets the objects from the file. Populates local_info. This function
           is how the scripts.Engine object interacts with the objectLoader.
           So, this function takes the current agent_layer from the engine and
           sets self.agent_layer so that it can be used in startElement.
           @type file_desc: File
           @param file_desc: an open file from which we read
           @return: None"""
        parser = make_parser()
        parser.setContentHandler(self)
        self.agent_layer = a_layer
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
        if name == "game_obj":
            obj_info = dict(attrs.items())
            # we need to convert all the unicode strings to ascii strings
            for key, val in attrs.items():
                obj_info.pop(key)
                obj_info[str(key)] = str(val)
            self.local_info.append(self.createObject(obj_info))
 
    def createObject(self, info):
        """Called when we need to get an actual object. 
           @type info: dict
           @param info: stores information about the object we want to create
           @return: the object"""
        # First, we try to get the type and ID, which every game_obj needs.
        try:
            obj_type = info.pop('type')
            ID = info.pop('ID')
        except KeyError:
            sys.stderr.write("Error: Game object missing type or id.")
            sys.exit(False)
        
        # add the agent_layer to the object dictionary in case it is needed by
        # the object we are constructing. If it is not needed, it will be 
        # ignored
        info['agent_layer'] = str(self.agent_layer)

        all_types = getAllObjects()
        return all_types[obj_type](ID, **info)
