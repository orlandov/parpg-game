#!python

import xml.etree.ElementTree

class Saver(object):
    def __init__(self, filepath, engine):
        self.filepath = filepath
        self.engine = engine
        self.doc 

    def write_map(self, map, importList):
        id = map.getId()
        format = "42.0"

        

def saveMapFile(path, engine, map, importList=[])
    map.setResourceFile(path) #wtf is this
    saver = Saver(path, engine)
    saver.save(map, importList)
