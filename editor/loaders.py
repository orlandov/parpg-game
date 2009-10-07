#!python

#   This file is part of PARPG.
#   PARPG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   PARPG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.

import fife

from xmlmap import XMLMapLoader
from serializers import WrongFileType, NameClash
from serializers.xmlobject import XMLObjectLoader

fileExtensions = ('xml',)

class Data(object):
    def __init__(self):
        self.objects = {}

    def createObject(self, layer, object_dict, inst):
        if object_dict.get('id') is not None:
            self.objects[object_dict['id']] = object_dict

data = None
def loadMapFile(path, engine, callback=None):
    global data # ugly hack
    data = Data()
    map_loader = XMLMapLoader(engine, data, callback)
    map = map_loader.loadResource(fife.ResourceLocation(path))
    return map

def loadImportFile(path, engine):
    object_loader = XMLObjectLoader(engine.getImagePool(), engine.getAnimationPool(), engine.getModel(), engine.getVFS())
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
