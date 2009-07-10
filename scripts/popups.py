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

import textwrap
import fife
import pychan
from scripts import drag_drop_data as data_drag
from scripts.items import item_image_dict
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
        @param data: A list of 9 items to use for the slots 1 - 9 
                     OR
                     one item to be used for all the slots
        @return: None
        """
        self.engine = engine
        pychan.init(self.engine, debug=True)
        
        self.container_gui = pychan.loadXML("gui/container_base.xml")
        self.container_gui.findChild(name="topWindow").title = title
    
        data_drag.dragging = False
        self.original_cursor_id = self.engine.getCursor().getId()


        if type(data) == list:
            self.setContainerImage("Slot1", item_image_dict[data[1]])
            self.setContainerImage("Slot2", item_image_dict[data[2]])
            self.setContainerImage("Slot3", item_image_dict[data[3]])
            self.setContainerImage("Slot4", item_image_dict[data[4]])
            self.setContainerImage("Slot5", item_image_dict[data[5]])
            self.setContainerImage("Slot6", item_image_dict[data[6]])
            self.setContainerImage("Slot7", item_image_dict[data[7]])
            self.setContainerImage("Slot8", item_image_dict[data[8]])
            self.setContainerImage("Slot9", item_image_dict[data[9]])
            
            self.container_gui.findChild(name="Slot1").item = data[1]
            self.container_gui.findChild(name="Slot2").item = data[2]
            self.container_gui.findChild(name="Slot3").item = data[3]
            self.container_gui.findChild(name="Slot4").item = data[4]
            self.container_gui.findChild(name="Slot5").item = data[5]
            self.container_gui.findChild(name="Slot6").item = data[6]
            self.container_gui.findChild(name="Slot7").item = data[7]
            self.container_gui.findChild(name="Slot8").item = data[8]
            self.container_gui.findChild(name="Slot9").item = data[9]

            self.empty_images = {"Slot1":item_image_dict[data[1]],
                                 "Slot2":item_image_dict[data[2]],
                                 "Slot3":item_image_dict[data[3]],
                                 "Slot4":item_image_dict[data[4]],
                                 "Slot5":item_image_dict[data[5]],
                                 "Slot6":item_image_dict[data[6]],
                                 "Slot7":item_image_dict[data[7]],
                                 "Slot8":item_image_dict[data[8]],
                                 "Slot9":item_image_dict[data[9]]}
            
            self.buttons = {}
            for key in self.empty_images:
                self.buttons[key] = "main_inv"

            self.events_to_map = {}
            for button in self.buttons:
                # make every button's callback be self.dragDrop
                self.events_to_map[button] = cbwa(self.dragDrop, button)
                ch = self.container_gui.findChild(name = button)

            self.container_gui.findChild(name="Slot1").item = data[1]
            self.container_gui.findChild(name="Slot2").item = data[2]
            self.container_gui.findChild(name="Slot3").item = data[3]
            self.container_gui.findChild(name="Slot4").item = data[4]
            self.container_gui.findChild(name="Slot5").item = data[5]
            self.container_gui.findChild(name="Slot6").item = data[6]
            self.container_gui.findChild(name="Slot7").item = data[7]
            self.container_gui.findChild(name="Slot8").item = data[8]
            self.container_gui.findChild(name="Slot9").item = data[9]
                
                

        else:
            self.setContainerImage("Slot1", item_image_dict[data])
            self.setContainerImage("Slot2", item_image_dict[data])
            self.setContainerImage("Slot3", item_image_dict[data])
            self.setContainerImage("Slot4", item_image_dict[data])
            self.setContainerImage("Slot5", item_image_dict[data])
            self.setContainerImage("Slot6", item_image_dict[data])
            self.setContainerImage("Slot7", item_image_dict[data])
            self.setContainerImage("Slot8", item_image_dict[data])
            self.setContainerImage("Slot9", item_image_dict[data])

            self.container_gui.findChild(name="Slot1").item = data
            self.container_gui.findChild(name="Slot2").item = data
            self.container_gui.findChild(name="Slot3").item = data
            self.container_gui.findChild(name="Slot4").item = data
            self.container_gui.findChild(name="Slot5").item = data
            self.container_gui.findChild(name="Slot6").item = data
            self.container_gui.findChild(name="Slot7").item = data
            self.container_gui.findChild(name="Slot8").item = data
            self.container_gui.findChild(name="Slot9").item = data

            self.empty_images = {"Slot1":item_image_dict[data],
                                 "Slot2":item_image_dict[data],
                                 "Slot3":item_image_dict[data],
                                 "Slot4":item_image_dict[data],
                                 "Slot5":item_image_dict[data],
                                 "Slot6":item_image_dict[data],
                                 "Slot7":item_image_dict[data],
                                 "Slot8":item_image_dict[data],
                                 "Slot9":item_image_dict[data]}

            self.buttons = {}
            for key in self.empty_images:
                self.buttons[key] = "main_inv"

            self.events_to_map = {}
            for button in self.buttons:
                # make every button's callback be self.dragDrop
                self.events_to_map[button] = cbwa(self.dragDrop, button)
                ch = self.container_gui.findChild(name = button)
                ch.item = data

        self.locations = ["main_inv"]

        self.container_gui.mapEvents(self.events_to_map)   
        self.resetMouseCursor()
            

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
        """
        Show the container
        @return: None
        """
        self.container_gui.show()

    def hideContainer(self):
        """
        Hide the container
        @return: None
        """
        self.container_gui.hide()
        
    def setMouseCursor(self, image, dummy_image, type = "native"): 
        """Set the mouse cursor to an image.
           @type image: string
           @param image: The image you want to set the cursor to
           @type dummy_image: string
           @param dummy_image: ???
           @type type: string
           @param type: ???
           @return: None"""
        cursor = self.engine.getCursor()
        cursor_type = fife.CURSOR_IMAGE
        img_pool = self.engine.getImagePool()
        if(type == "target"):
            target_cursor_id = img_pool.addResourceFromFile(image)  
            dummy_cursor_id = img_pool.addResourceFromFile(dummy_image)
            cursor.set(cursor_type,target_dummy_cursor_id)
            cursor.setDrag(cursor_type,target_cursor_id,-16,-16)
        else:
            cursor_type = fife.CURSOR_IMAGE
            zero_cursor_id = img_pool.addResourceFromFile(image)
            cursor.set(cursor_type,zero_cursor_id)
            cursor.setDrag(cursor_type,zero_cursor_id)
            
    def resetMouseCursor(self):
        """Reset cursor to default image.
           @return: None"""
        c = self.engine.getCursor()
        img_pool = self.engine.getImagePool()
        cursor_type = fife.CURSOR_NATIVE
        # this is the path to the default image
        cursor_id = self.original_cursor_id
        c.setDrag(cursor_type, cursor_id)
        c.set(cursor_type, cursor_id)
        
    def dragDrop(self, obj):
        """Decide whether to drag or drop the image.
           @type obj: string
           @param obj: The name of the object within 
                       the dictionary 'self.buttons'
           @return: None"""
        if(data_drag.dragging == True):
            self.dropObject(obj)
        elif(data_drag.dragging == False):
            self.dragObject(obj)
                
    def dragObject(self, obj):
        """Drag the selected object.
           @type obj: string
           @param obj: The name of the object within
                       the dictionary 'self.buttons'
           @return: None"""
        # get the widget from the container_gui with the name obj
        drag_widget = self.container_gui.findChild(name = obj)
        # get it's type (e.g. main_inv)
        data_drag.dragged_type = self.buttons[obj]
        # get the item that the widget is 'storing'
        data_drag.dragged_item = drag_widget.item
        # get the up and down images of the widget
        up_image = drag_widget._getUpImage()
        down_image = drag_widget._getDownImage()
        # set the mouse cursor to be the widget's image
        self.setMouseCursor(up_image,down_image)
        data_drag.dragged_image = up_image
        data_drag.dragging = True
        # after dragging the 'item', set the widgets' images
        # so that it has it's default 'empty' images
        drag_widget._setUpImage(self.empty_images[obj])
        drag_widget._setDownImage(self.empty_images[obj])
        drag_widget._setHoverImage(self.empty_images[obj])
        
    def dropObject(self, obj):
        """Drops the object being dropped
           @type obj: string
           @param obj: The name of the object within
                       the dictionary 'self.buttons' 
           @return: None"""
        # find the type of the place that the object
        # is being dropped onto
        data_drag.dropped_type  =  self.buttons[obj]
        # if the dragged obj or the place it is being dropped is
        # in the main container_gui, drop the object
        if((data_drag.dragged_type == 'main_inv') or
           (data_drag.dropped_type == 'main_inv')):
            drag_widget = self.container_gui.findChild(name = obj)
            drag_widget._setUpImage(data_drag.dragged_image)
            drag_widget._setHoverImage(data_drag.dragged_image)
            drag_widget._setDownImage(data_drag.dragged_image)
            drag_widget.item = data_drag.dragged_item
            print 'Item: ' + drag_widget.item
            data_drag.dragging = False
            #reset the mouse cursor to the normal cursor
            self.resetMouseCursor()
            # if the object was dropped onto a ready slot, then
            # update the hud
            if (data_drag.dropped_type == 'ready'):
                self.readyCallback()
        
        # if the dragged object's type is the same as the location to
        # to drop it at's, and the dragged object's type is in
        # self.locations, then drop the object
        elif((data_drag.dragged_type == data_drag.dropped_type) and
             (data_drag.dragged_type in self.locations)):
            drag_widget = self.container_gui.findChild(name = obj)
            drag_widget._setUpImage(data_drag.dragged_image)
            drag_widget._setHoverImage(data_drag.dragged_image)
            drag_widget._setDownImage(data_drag.dragged_image)
            drag_widget.item = data_drag.dragged_item
            print 'Item: ' + drag_widget.item
            data_drag.dragging = False
            # reset the mouse cursor
            self.resetMouseCursor()
            # if the object was dropped onto a ready slot, then
            # update the hud
            if(data_drag.dropped_type == 'ready'):
                self.readyCallback()
        # otherwise, we assume that the player is trying to
        # drop an object onto an incompatible slot
        else:
            # reset the mouse cursor
            self.resetMouseCursor()
            data_drag.dragging = False

class ExaminePopup():
    """
    Create a popup for when you click examine on an object
    """
    def __init__(self, engine, object_title, desc):
        """
        Initialize the popup
        
        @type engine: fife.Engine
        @param engine: an instance of the fife engine
        @type object_title: string
        @param object_title: The title for the window, probably should just be the name of the object
        @type desc: string
        @param desc: The description of the object
        @return: None
        """
        self.engine = engine
        pychan.init(self.engine, debug=True)

        self.examineWindow = pychan.widgets.Window(title=unicode(object_title),
                                                   position_technique="center:center",
                                                   min_size=(175,175))
            
        new_desc = textwrap.fill(desc, 34)

        self.scroll = pychan.widgets.ScrollArea(name='scroll', size=(150,150))
        self.description = pychan.widgets.Label(name='descText', text=unicode(new_desc))
        self.scroll.addChild(self.description)
        self.examineWindow.addChild(self.scroll)
        
        self.close_button = pychan.widgets.Button(name='closeButton', text=unicode('Close'))
        self.examineWindow.addChild(self.close_button)

        self.examineWindow.mapEvents({'closeButton':self.examineWindow.hide})

    def closePopUp(self):
        self.examineWindow.hide()
    
    def showPopUp(self):
        self.examineWindow.show()
