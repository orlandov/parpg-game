#!python

import fife
from serializers import root_subfile

from xml.etree.ElementTree import Element, SubElement, tostring

class Saver(object):
    def __init__(self, filepath, engine):
        self.filepath = filepath
        self.engine = engine
        self.namespace = ''

    def write_map(self, map, import_list):
        print "import list", import_list
        self.map = map

        attrib = {
            'id': map.getId(),
            'format': "1.0"
        }
        self.map_element = Element('map', attrib)

        self.write_imports(import_list)
        self.write_layers()
        self.write_cameras()

        print file('../parpg/maps/map_new.xml', 'w').write(
            """<?xml version="1.0" encoding="ascii"?>"""+
            tostring(self.map_element) + "\n")

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
                if (file in imports): continue
                if self.have_superdir(file, import_list): continue
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
        self.map_element.append(Element('import', { 'file': file }))

    def write_import_dir(import_dir):
        self.map_element.append(Element('import', { 'dir': dir }))

    def write_layers(self):
        for layer in self.map.getLayers():
            cellgrid = layer.getCellGrid()
            attrib = {
                'id': layer.getId(),
                'grid_type': cellgrid.getType(),
                'x_scale': str(cellgrid.getXScale()),
                'y_scale': str(cellgrid.getYScale()),
                'rotation': str(cellgrid.getRotation()),
                'x_offset': str(cellgrid.getXShift()),
                'y_offset': str(cellgrid.getYShift()),
                'pathing': self.pathing_val_to_str(layer.getPathingStrategy()),
                'transparency': str(layer.getLayerTransparency()),
            }
            layer_element = SubElement(self.map_element, 'layer', attrib)
            self.write_instances(layer_element, layer)

    def write_instances(self, layer_element, layer):
        instances_element = SubElement(layer_element, 'instances')
        for inst in layer.getInstances():
            position = inst.getLocationRef().getExactLayerCoordinates()
            attrib = {
                'o': inst.getObject().getId(),
                'x': str(position.x),
                'y': str(position.y),
                'z': str(position.z),
                'r': str(inst.getRotation()),
            }
            namespace = inst.getObject().getNamespace()
            if namespace != self.namespace:
                attrib['ns'] = inst.getObject().getNamespace()
                self.namespace = namespace
            inst_id = inst.getId()
            if inst_id:
                attrib['id'] = inst_id

            instances_element.append(Element('i', attrib))

    def write_cameras(self):
        cameras = self.engine.getView().getCameras()

        for cam in cameras:
            if cam.getLocationRef().getMap().getId() != self.map.getId(): continue
            cell_dimensions = cam.getCellImageDimensions()
            viewport = cam.getViewPort()

            attrib = {
                'id': cam.getId(),
                'zoom': str(cam.getZoom()),
                'tilt': str(cam.getTilt()),
                'rotation': str(cam.getRotation()),
                'ref_layer_id': cam.getLocation().getLayer().getId(),
                'ref_cell_width': str(cell_dimensions.x),
                'ref_cell_height': str(cell_dimensions.y),
            }

            if viewport != self.engine.getRenderBackend().getArea():
                attrib['viewport'] = '%d,%d,%d,%d' % (viewport.x, viewport.y, viewport.w, viewport.h)
            self.map_element.append(Element('camera', attrib))


    def pathing_val_to_str(self, val):
        if val == fife.CELL_EDGES_AND_DIAGONALS:
            return "cell_edges_and_diagonals"
        if val == fife.FREEFORM:
            return "freeform"
        return "cell_edges_only"

def saveMapFile(path, engine, map, **kwargs):
    map.setResourceFile(path) #wtf is this
    saver = Saver(path, engine)
    saver.write_map(map, kwargs.get('importList'))
