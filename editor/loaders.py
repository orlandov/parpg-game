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
    """     load map file and get (an optional) callback if major stuff is done:
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
    data = Data()
    map_loader = XMLMapLoader(engine, data, callback)
    map = map_loader.loadResource(fife.ResourceLocation(path))
    print "--- Loading map took: ", map_loader.time_to_load, " seconds."
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
