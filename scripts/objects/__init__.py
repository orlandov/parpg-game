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
import containers
import actors
import sys

object_modules = [containers, actors,]

def getAllObjects ():
    """Returns a dictionary with the names of the concrete game object classes
    mapped to the classes themselves"""
    result = {}
    for module in object_modules:
        for class_name in module.__all__:
            result[class_name] = getattr (module,class_name)
            
    return result

def createObject(info, extra = {}):
        """Called when we need to get an actual object. 
           @type info: dict
           @param info: stores information about the object we want to create
           @type extra: dict
           @param extra: stores additionally required attributes, like agent layer, engine etc.
           @return: the object"""
        # First, we try to get the type and ID, which every game_obj needs.
        try:
            obj_type = info.pop('type')
            ID = info.pop('id')
        except KeyError:
            sys.stderr.write("Error: Game object missing type or id.")
            sys.exit(False)
        
        # add the extra info
        for key, val in extra.items():
            info[key] = val

        return getAllObjects()[obj_type](ID, **info)