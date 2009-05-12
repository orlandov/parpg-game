#!/usr/bin/python

import sys, os


# Add fife modules to the path and import them
def _jp(path):
    return os.path.sep.join(path.split('/'))

_paths = ('../../../engine/swigwrappers/python', '../../../engine/extensions')
for p in _paths:
    if p not in sys.path:
        sys.path.append(_jp(p))

import fife
import fifelog
import pychan
from pychan.tools import callbackWithArguments as cbwa

#Main inventory class
class Inventory():

    def __init__(self, engine):
        pychan.init(engine,debug=True)

        self.engine = engine
    
        self.dragging = False
        self.dragged_image = None
        self.dragged_type = None
        self.dragged_item = None
        self.dropped_type = None
        
    
        self.inventory = pychan.loadXML("gui/inventory.xml")
    
        events_to_map = {'close_button':self.inventory.hide,
                         'reset_button':self.resetImages}

        self.empty_images = {}


        # every button on the inventory and its category
        self.buttons = {'A1':'main_inv', 'A2':'main_inv', 'A3':'main_inv',
                        'A4':'main_inv', 'A5':'main_inv', 'B1':'main_inv',
                        'B2':'main_inv', 'B3':'main_inv', 'B4':'main_inv',
                        'B5':'main_inv', 'C1':'main_inv', 'C2':'main_inv',
                        'C3':'main_inv', 'C4':'main_inv', 'C5':'main_inv',
                        'D1':'main_inv', 'D2':'main_inv', 'D3':'main_inv',
                        'D4':'main_inv', 'D5':'main_inv',
                        'LeftFoot':'foot', 'RightFoot':'foot',
                        'LeftHand':'hand', 'RightHand':'hand',
                        'Head':'head', 'Ready1':'ready', 
                        'Ready2':'ready', 'Ready3':'ready', 
                        'Ready4':'ready', 'Belt':'belt', 'LeftHeld':'held',
                        'RightHeld':'held', 'Body':'body'}
        
        # all possible categories
        self.locations = ['ready', 'head', 'foot', 'hand', 'belt', 'held', 'body']
        
        for button in self.buttons:
            # make every button's callback be self.dragDrop
            events_to_map[button] = cbwa(self.dragDrop, button)
            ch = self.inventory.findChild(name=button)
            
            #make every slot's item be empty
            ch.item = ""
            self.empty_images[button] = ch._getUpImage()


        self.inventory.mapEvents(events_to_map)   
        self.resetMouseCursor()
        self.inventory.show()

    def closeInventory(self):
        self.inventory.hide()

    def showInventory(self):
        self.inventory.show()

    # resets all images in the program to the way they were when the program
    # was first launched (will be taken out on release)
    def resetImages(self):
        for image in self.empty_images:
            child = self.inventory.findChild(name=image)
            original_image = self.empty_images[image]
            
            child._setUpImage(original_image)
            child._setDownImage(original_image)
            child._setHoverImage(original_image)


    # set the mouse cursor to an image
    def setMouseCursor(self, image, dummy_image, type="native"): 
            
        cursor = self.engine.getCursor()
        cursor_type = fife.CURSOR_IMAGE
        img_pool = self.engine.getImagePool()
        
        if(type == "target"):
            target_cursor_id = img_pool.addResourceFromFile(image)  
            dummy_cursor_id = img_pool.addResourceFromFile(dummy_image)
            cursor.set(cursor_type, target_dummy_cursor_id)
            cursor.setDrag(cursor_type, target_cursor_id, -16, -16)
            
        else:
            cursor_type = fife.CURSOR_IMAGE
            zero_cursor_id = img_pool.addResourceFromFile(image)
            cursor.set(cursor_type, zero_cursor_id)
            cursor.setDrag(cursor_type, zero_cursor_id)
            
    # reset mouse cursor to default image ("gui/inv_images/cursor.png")
    def resetMouseCursor(self):
        c = self.engine.getCursor()
        
        img_pool = self.engine.getImagePool()
        
        cursor_type = fife.CURSOR_IMAGE
        cursor_id = img_pool.addResourceFromFile("gui/inv_images/cursor.png")
        c.setDrag(cursor_type, cursor_id)
        c.set(cursor_type, cursor_id)
        
    # decide whether to drag or drop the image
    def dragDrop(self, obj):
        if(self.dragging == True):
            self.dropObject(obj)
            
        elif(self.dragging == False):
            self.dragObject(obj)
                
    # drag the selected object
    def dragObject(self, obj):
    
        drag_widget = self.inventory.findChild(name=obj)
        
        self.dragged_type = self.buttons[obj]
        self.dragged_item = drag_widget.item
        
        up_image = drag_widget._getUpImage()
        down_image = drag_widget._getDownImage()
        self.setMouseCursor(up_image, down_image)
        self.dragged_image = up_image
        self.dragging = True
        
    #drop the object being currently dragged
    def dropObject(self, obj):
        self.dropped_type = self.buttons[obj]
        
        if((self.dragged_type == 'main_inv') or
           (self.dropped_type == 'main_inv')):
            drag_widget = self.inventory.findChild(name=obj)
            drag_widget._setUpImage(self.dragged_image)
            drag_widget._setHoverImage(self.dragged_image)
            drag_widget._setDownImage(self.dragged_image)
            drag_widget.item = self.dragged_item
            self.dragging = False
            self.resetMouseCursor()
            
        
        elif((self.dragged_type == self.dropped_type) and
             (self.dragged_type in self.locations)):
            drag_widget = self.inventory.findChild(name=obj)
            drag_widget._setUpImage(self.dragged_image)
            drag_widget._setHoverImage(self.dragged_image)
            drag_widget._setDownImage(self.dragged_image)
            drag_widget.item = self.dragged_item
            self.dragging = False
            self.resetMouseCursor()
    

        else:
            self.resetMouseCursor()
            self.dragging = False
