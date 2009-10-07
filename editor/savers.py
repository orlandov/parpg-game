#!python

from xml.etree.ElementTree import Element, SubElement, tostring
from serializers import root_subfile

class Saver(object):
    def __init__(self, filepath, engine):
        self.filepath = filepath
        self.engine = engine

    def write_map(self, map, import_list):
        self.map_element = Element('map')
        self.map = map

        id = map.getId()
        format = "42.0"

        self.write_imports(import_list)
        print tostring(self.map_element)

    def write_imports(self, import_list):
        map = self.map
        for import_dir in import_list:
            print "GRF", map.getResourceFile()
            self.write_importdir(
                root_subfile(map.getResourceFile(), import_dir))

        imports = []
        for layer in map.getLayers():
            for instance in layer.getInstances():
                file = instance.getObject().getResourceFile()
                if (file in imports): break
                if self.have_superdir(file, import_list): break
                imports.append(file)
                self.write_import(
                    root_subfile(map.getResourceFile(), file))

    def have_superdir(self, file, import_list):
        '''returns true, if file is in directories given in import_list'''
        for dir in import_list:
            have = True
            for test in zip(dir.split(os.path.sep), file.split(os.path.sep)):
                if test[0] != test[1]: have = False
            if have: return True

        return False

    def write_import(self, file):
        import_element = SubElement(self.map_element, 'import')
        import_element.attrib['file'] = file

    def write_import_dir(import_dir):
        import_element = SubElement(self.map_element, 'import')
        import_element.attrib['dir'] = import_dir

def saveMapFile(path, engine, map, **kwargs):
    map.setResourceFile(path) #wtf is this
    saver = Saver(path, engine)
    saver.write_map(map, kwargs.get('importList'))
