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
        self.local_info = []

    def getParser(self):
        """Simple one liner to remove XML dependencies in engine.py.
           @rtype: parser
           @return: A parser to work with"""
        return make_parser()
    
    def getObjects(self, file_desc):
        """Gets the objects from the file. Populates the dictionary.
           @type file_desc: File
           @param file_desc: an open file from which we read
           @return: None"""
        parser = self.getParser()
        parser.setContentHandler(self)
        parser.parse(file_desc)

    def startElement(self, name, attrs):
        """Called every time we meet a new element in the XML file
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
        """Called when we need to get an actual object. Nasty if statement.
           (Don't see why this should have its own class though...)
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

        all_types = getAllObjects()
        return all_types[obj_type](ID, **info)
