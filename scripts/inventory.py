#!/usr/bin/python

import sys,os

import fife
import fifelog
import pychan
from pychan.tools import callbackWithArguments as cbwa

class Inventory():
    """Main inventory class"""
    def __init__(self, engine):
        pychan.init(engine, debug = True)
        self.engine = engine
        self.dragging = False
        self.dragged_image = None
        self.dragged_type = None
        self.dragged_item = None
        self.dropped_type = None
        self.original_cursor_id = self.engine.getCursor().getId()

        self.inventory = pychan.loadXML("gui/inventory.xml")
        self.events_to_map = {}

        # the images that should be used for the buttons when they are "empty"
        self.empty_images = {'A1':'gui/inv_images/inv_backpack.png',
                             'A2':'gui/inv_images/inv_backpack.png',
                             'A3':'gui/inv_images/inv_backpack.png',
                             'A4':'gui/inv_images/inv_backpack.png',
                             'A5':'gui/inv_images/inv_backpack.png',
                             'B1':'gui/inv_images/inv_backpack.png',
                             'B2':'gui/inv_images/inv_backpack.png',
                             'B3':'gui/inv_images/inv_backpack.png',
                             'B4':'gui/inv_images/inv_backpack.png',
                             'B5':'gui/inv_images/inv_backpack.png',
                             'C1':'gui/inv_images/inv_backpack.png',
                             'C2':'gui/inv_images/inv_backpack.png',
                             'C3':'gui/inv_images/inv_backpack.png',
                             'C4':'gui/inv_images/inv_backpack.png',
                             'C5':'gui/inv_images/inv_backpack.png',
                             'D1':'gui/inv_images/inv_backpack.png',
                             'D2':'gui/inv_images/inv_backpack.png',
                             'D3':'gui/inv_images/inv_backpack.png',
                             'D4':'gui/inv_images/inv_backpack.png',
                             'D5':'gui/inv_images/inv_backpack.png',
                             'Head':'gui/inv_images/inv_head.png',
                             'LeftHeld':'gui/inv_images/inv_litem.png',
                             'RightHeld':'gui/inv_images/inv_ritem.png',
                             'LeftHand':'gui/inv_images/inv_lhand.png',
                             'RightHand':'gui/inv_images/inv_rhand.png',
                             'Body':'gui/inv_images/inv_torso.png',
                             'Belt':'gui/inv_images/inv_belt.png',
                             'Ready1':'gui/inv_images/inv_belt_pouches.png',
                             'Ready2':'gui/inv_images/inv_belt_pouches.png',
                             'Ready3':'gui/inv_images/inv_belt_pouches.png',
                             'Ready4':'gui/inv_images/inv_belt_pouches.png',
                             'LeftFoot':'gui/inv_images/inv_lfoot.png',
                             'RightFoot':'gui/inv_images/inv_rfoot.png'}

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
        self.locations = ['ready', 'head', 'foot', 'hand',
                          'belt', 'held', 'body']
        for button in self.buttons:
            # make every button's callback be self.dragDrop
            self.events_to_map[button] = cbwa(self.dragDrop, button)
            ch = self.inventory.findChild(name = button)
            # make every slot's item be empty
            ch.item = ""

        self.inventory.mapEvents(self.events_to_map)   
        self.resetMouseCursor()
        self.inventory.show()

    def closeInventory(self):
        """Close the inventory"""
        self.inventory.hide()

    def showInventory(self):
        """Show the inventory"""
        self.inventory.show()

    def setMouseCursor(self, image, dummy_image, type = "native"): 
        """Set the mouse cursor to an image"""
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
        """Reset cursor to default image"""
        c = self.engine.getCursor()
        img_pool = self.engine.getImagePool()
        cursor_type = fife.CURSOR_NATIVE
        # this is the path to the default image
        cursor_id = self.original_cursor_id
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
        drag_widget = self.inventory.findChild(name = obj)
        self.dragged_type = self.buttons[obj]
        self.dragged_item = drag_widget.item
        up_image = drag_widget._getUpImage()
        down_image = drag_widget._getDownImage()
        self.setMouseCursor(up_image,down_image)
        self.dragged_image = up_image
        self.dragging = True

        drag_widget._setUpImage(self.empty_images[obj])
        drag_widget._setDownImage(self.empty_images[obj])
        drag_widget._setHoverImage(self.empty_images[obj])
        
    def dropObject(self, obj):
        """Drops the object being dropped"""
        self.dropped_type  =  self.buttons[obj]
        if((self.dragged_type == 'main_inv') or
           (self.dropped_type == 'main_inv')):
            drag_widget = self.inventory.findChild(name = obj)
            drag_widget._setUpImage(self.dragged_image)
            drag_widget._setHoverImage(self.dragged_image)
            drag_widget._setDownImage(self.dragged_image)
            drag_widget.item = self.dragged_item
            self.dragging = False
            self.resetMouseCursor()
        elif((self.dragged_type == self.dropped_type) and
             (self.dragged_type in self.locations)):
            drag_widget = self.inventory.findChild(name = obj)
            drag_widget._setUpImage(self.dragged_image)
            drag_widget._setHoverImage(self.dragged_image)
            drag_widget._setDownImage(self.dragged_image)
            drag_widget.item = self.dragged_item
            self.dragging = False
            self.resetMouseCursor()
        else:
            self.resetMouseCursor()
            self.dragging = False
