#!python

import fife

from xmlmap import XMLMapLoader
from serializers import WrongFileType, NameClash
from serializers.xmlobject import XMLObjectLoader

fileExtensions = ('xml',)

class Data(object):
    def createObject(self, *args):
        print "GOT", args

def loadMapFile(path, engine, callback=None):
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
