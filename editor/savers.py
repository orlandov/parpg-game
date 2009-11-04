#!python

# This file is part of PARPG.
# PARPG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PARPG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PARPG.  If not, see <http://www.gnu.org/licenses/>.

import fife
import loaders
from serializers import root_subfile

from xml.etree.ElementTree import Element, SubElement, tostring

class Saver(object):
    """Serialize a FIFE map object to an XML file"""

    def __init__(self, filepath, engine):
        self.filepath = filepath
        self.engine = engine
        self.namespace = ''

    def write_map(self, map, import_list):
        """Write the specified map to an XML file"""

        self.map = map
        attrib = {
            'id': map.getId(),
            'format': "1.0"
        }
        self.map_element = Element('map', attrib)
        self.map_element.text = "\n\t"
        self.map_element.tail = "\n"
        # serialize FIFE details
        self.write_imports(import_list)
        self.write_layers()
        self.write_cameras()

        # add newlines to the elements
#        for subElement in self.map_element:
#            subElement.tail = "\n"
        # finally write out the XML file
        file(self.filepath, 'w').write(
            """<?xml version="1.0" encoding="ascii"?>\n%s"""
                % (tostring(self.map_element),))

    def write_imports(self, import_list):
        """Serialize imports"""
        map = self.map
        for import_dir in import_list:
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
        """Returns true, if file is in directories given in import_list"""
        for dir in import_list:
            have = True
            # TODO use os.path.split here
            for test in zip(dir.split(os.path.sep), file.split(os.path.sep)):
                if test[0] != test[1]: have = False
            if have: return True

        return False

    def write_import(self, filename):
        """Write an import filename"""
        import_element = Element('import', { 'file': filename })
        import_element.tail = "\n\t"
        self.map_element.append(import_element)

    def write_import_dir(import_dir):
        """Write an import dir"""
        import_dir_element = Element('import', { 'dir': import_dir })
        import_dir_element.tail = "\n"
        self.map_element.append(import_dir_element)

    def write_layers(self):
        """Write a layer"""
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
            layer_element.text = "\n\t\t"
            layer_element.tail = "\n\n\t"
            self.write_instances(layer_element, layer)

    def write_instances(self, layer_element, layer):
        """Write out the instances in a layer"""
        instances_element = SubElement(layer_element, 'instances')
        instances_element.text = "\n\t\t\t"
        instances_element.tail = "\n\t"
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

            # if the object has an instance id, write out saved attributes
            if inst_id is not None and inst_id in loaders.data.objects:
                skip_keys = ['gfx', 'xpos', 'ypos']
                for key in loaders.data.objects[inst_id]:
                    # set value if we haven't written the key out yet and key
                    # has a value in our attr stash (loaders.data.objects)
                    if key in skip_keys or key in attrib \
                        or key not in loaders.data.objects[inst_id]:
                        continue

                    attrib[key] = str(loaders.data.objects[inst_id][key])

            # the local_loader loader sets object_type as type, we have to
            # correct for that here but really we should fix that there
            if attrib.get('type'):
                attrib['object_type'] = attrib['type']
                del attrib['type']

            inst_element = Element('i', attrib)
            inst_element.tail = "\n\t\t\t"
            instances_element.append(inst_element)

    def write_cameras(self):
        """Write out the cameras specified in a map"""
        cameras = self.engine.getView().getCameras()

        for cam in cameras:
            if cam.getLocationRef().getMap().getId() != self.map.getId(): continue
            cell_dimensions = cam.getCellImageDimensions()

            attrib = {
                'id': cam.getId(),
                'zoom': str(cam.getZoom()),
                'tilt': str(cam.getTilt()),
                'rotation': str(cam.getRotation()),
                'ref_layer_id': cam.getLocation().getLayer().getId(),
                'ref_cell_width': str(cell_dimensions.x),
                'ref_cell_height': str(cell_dimensions.y),
            }

            camera_element = Element('camera', attrib)
            camera_element.tail = "\n"
            self.map_element.append(camera_element)

    def pathing_val_to_str(self, val):
        """Convert a pathing value to a string"""
        if val == fife.CELL_EDGES_AND_DIAGONALS:
            return "cell_edges_and_diagonals"
        if val == fife.FREEFORM:
            return "freeform"
        return "cell_edges_only"

def saveMapFile(path, engine, map, **kwargs):
    """Saves a map"""
    map.setResourceFile(path) #wtf is this
    saver = Saver(path, engine)
    saver.write_map(map, kwargs.get('importList'))
