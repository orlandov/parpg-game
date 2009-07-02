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

from objects import base

class GameState(object):
    """This class holds the current state of the game."""
    def __init__(self):
        """initialize attributes"""
        self.PC = None
        self.objects = {}
        self.currentMap = None
        
    def getObjectsFromMap(self, map_id):
        """Gets all objects that are currently on the given map.
           @type map: String
           @param map: The map name.
           @returns: The list of objects on this map."""
        return [i for i in self.objects.values() if i.map_id == map_id]
    
    def getObjectById(self, id):
        """Gets an object by it's id
           @type id: String
           @param id: The id of the object.
           @returns: The object or None."""
        if id in self.objects:
            return self.objects[id]

