#/usr/bin/python

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

import fife
import pychan
from pychan.tools import callbackWithArguments as cbwa

class ContainerGUI():
    def __init__(self, engine, title, data):
        """
        A class to create a window showing the contents of a container.
        
        @type engine: fife.Engine
        @param engine: an instance of the fife engine
        @type title: string
        @param title: The title of the window
        @type data: list or string
        @param data: A list of 9 images to use for the slots 1 - 9 OR a string for one image that will be used on all the slots
        @return: None
        """
        pychan.init(engine, debug=True)
        
        self.container_gui = pychan.loadXML("gui/container_base.xml")
        self.container_gui.findChild(name="topWindow").title = title

    
        if type(data) == list:
            self.setContainerImage("Slot1", data[1])
            self.setContainerImage("Slot2", data[2])
            self.setContainerImage("Slot3", data[3])
            self.setContainerImage("Slot4", data[4])
            self.setContainerImage("Slot5", data[5])
            self.setContainerImage("Slot6", data[6])
            self.setContainerImage("Slot7", data[7])
            self.setContainerImage("Slot8", data[8])
            self.setContainerImage("Slot9", data[9])
            print "Setting slots to list: " + data

        else:
            self.setContainerImage("Slot1", data)
            self.setContainerImage("Slot2", data)
            self.setContainerImage("Slot3", data)
            self.setContainerImage("Slot4", data)
            self.setContainerImage("Slot5", data)
            self.setContainerImage("Slot6", data)
            self.setContainerImage("Slot7", data)
            self.setContainerImage("Slot8", data)
            self.setContainerImage("Slot9", data)
            print "Setting slots to string: " + data
            
        container_events = {'takeAllButton':self.nullFunc,
                            'closeButton':self.hideContainer}

        self.container_gui.mapEvents(container_events)

    def nullFunc(self):
        pass

    def setContainerImage(self, widget_name, image):
        """
        Sets the up, down, and hover images of an image button to image

        @type widget_name: string
        @param widget_name: the name of the widget
        @type image: string
        @param image: the path to the image
        @return None
        """
        widget = self.container_gui.findChild(name=widget_name)
        widget.up_image = image
        widget.down_image = image
        widget.hover_image = image
        print 'Set all images on %s using %s' % (widget, image)
        
    def showContainer(self):
        self.container_gui.show()

    def hideContainer(self):
        self.container_gui.hide()
        
