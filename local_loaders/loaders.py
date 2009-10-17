#!/usr/bin/python

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Most of this code was copied from the FIFE file loaders.py
# It is part of the local code base now so we customize what happens as 
# we read map files
import fife

from xmlmap import XMLMapLoader
from serializers import WrongFileType, NameClash

from serializers.xmlobject import XMLObjectLoader

fileExtensions = ('xml',)

def loadMapFile(path, engine, data, callback=None):
    """     load map file and get (an optional) callback if major stuff 
            is done:
    - map creation
    - parsed impor0ts
    - parsed layers 
    - parsed cameras
    the callback will send both a string and a float (which shows
    the overall process), callback(string, float)
    
    Inputs:
        path = filename for map
        engine = FIFE engine
        data = Engine object for PARPG data
        
    @return    map    : map object
    """
    map_loader = XMLMapLoader(engine, data, callback)
    map = map_loader.loadResource(fife.ResourceLocation(path))
    print "--- Loading map took: ", map_loader.time_to_load, " seconds."
    return map

def loadImportFile(path, engine):
    object_loader = XMLObjectLoader(engine.getImagePool(), \
                                    engine.getAnimationPool(), \
                                    engine.getModel(), engine.getVFS())
    res = None
    try:
        res = object_loader.loadResource(fife.ResourceLocation(path))
        print 'imported object file ' + path
    except WrongFileType:
        pass
#        print 'ignored non-object file ' + path
    except NameClash:
        pass
#        print 'ignored already loaded file ' + path
    return res
