#!/usr/bin/python

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

"""Containes classes defining the base properties of all interactable in-game 
   objects (such as Carryable, Openable, etc. These are generally independent 
   classes, which can be combined in almost any way and order. 

   Some rules that should be followed when CREATING base property classes:
   
   1. If you want to support some custom initialization arguments, always define 
      them as keyword ones. Only GameObject would use positional arguments.
   2. In __init__() **ALWAYS** call the parent's __init__(**kwargs), preferably 
      *at the end* of your __init__() (makes it easier to follow)
   3. There should always be an is_x class member set to True on __init__ 
      (where X is the name of the class)

   EXAMPLE:

   class Openable(object):
       def __init__ (self, is_open = True, **kwargs):
           self.is_openable = True
           self.is_open = is_open
           super(Openable,self).__init__ (**kwargs)
        

   Some rules are to be followed when USING the base classes to make composed ones:

   1. The first parent should always be the base GameObject class
   2. Base classes other than GameObject can be inherited in any order
   3. The __init__ functoin of the composed class should always invoke the
      parent's __init__() *before* it starts customizing any variables.

   EXAMPLE:

   class TinCan (GameObject, Container, Scriptable, Destructable, Carryable):
       def __init__ (self, *args, **kwargs):
           super(TinCan,self).__init__ (*args, **kwargs)
           self.name = 'Tin Can'"""
import fife
from settings import Setting
from random import randrange

class GameObject (object):
    """A base class to be inherited by all game objects. This must be the
       first class (left to right) inherited by any game object."""
    def __init__ (self, ID, gfx = {}, xpos = 0.0, ypos = 0.0, map_id = None, 
                  blocking=True, name="Generic object", text="Item description",
                  desc="Detailed description", **kwargs):
        """Set the basic values that are shared by all game objects.
           @type ID: String
           @param ID: Unique object identifier. Must be present.
           @type gfx: Dictionary
           @param gfx: Dictionary with graphics for the different contexts       
           @type coords 2-item tuple
           @param coords: Initial coordinates of the object.
           @type map_id: ???
           @param map_id: Identifier of the map where the object is located
           @type blocking: Boolean
           @param blocking: Whether the object blocks character movement
           @type name: String
           @param name: The display name of this object (e.g. 'Dirty crate')
           @type text: String
           @param text: A longer description of the item
           @type desc: String
           @param desc: A long description of the item that is displayed when it is examined
           """
        
        self.ID = ID
        self.gfx = gfx
        self.X = xpos
        self.Y = ypos
        self.map_id = map_id
        self.blocking = True
        self.name = name
        self.text = text
        self.desc = desc
        super(GameObject,self).__init__ (**kwargs)
        
    def trueAttr(self, attr):
        """Shortcut function to check if the current object has a member named
           is_%attr and if that attribute evaluates to True"""
        return hasattr(self,'is_%s' % attr) and getattr(self, 'is_%s' % attr)

    def _getCoords(self):
        """Get-er property function"""
        return (self.X, self.Y)
    
    def _setCoords(self, coords):
        """Set-er property function"""
        self.X, self.Y = float(coords[0]), float (coords[1])
        
    coords = property (_getCoords, _setCoords, 
        doc = "Property allowing you to get and set the obejct's coordinates via tuples")
    
    def __repr__(self):
        """A debugging string representation of the object"""
        return "<%s:%s>" % (self.name, self.ID)

class Openable(object):
    """Adds open() and .close() capabilities to game objects
    The current state is tracked by the .is_open variable"""
    def __init__(self, is_open = True, **kwargs):
        """Init operation for openable objects
        @type is_open: Boolean
        @param is_open: Keyword boolean argument sets the initial state."""
        self.is_openable = True
        self.is_open = is_open
        super(Openable,self).__init__ (**kwargs)
    
    def open(self):
        """Opens the object, and runs an 'onOpen' script, if present"""
        self.is_open = True
        if self.trueAttr ('scriptable'):
            self.runScript('onOpen')
            
    def close(self):
        """Opens the object, and runs an 'onClose' script, if present"""
        self.is_open = False
        if self.trueAttr ('scriptable'):
            self.runScript('onClose')             
        
class Lockable (Openable):
    """Allows objects to be locked"""
    def __init__ (self, locked = True, **kwargs):
        """Init operation for lockable objects
        @type locked: Boolean
        @param locked: Keyword boolen argument to set the initial locked state.
        """
        self.is_lockable = True
        self.locked = locked
        super(Lockable,self).__init__ (**kwargs)
        
    def unlock (self):
        """Handles unlocking functionality"""
        self.locked = False      
        
    def lock (self):
        """Handles  locking functionality"""
        self.close()
        self.locked = True
        
    def open (self, *args, **kwargs):
        """Adds a check to see if the object is unlocked before running the
           .open() function of the parent class"""
        if self.locked:
            raise ValueError ("Open failed: object locked")
        super (Lockable,self).open(*args,**kwargs)
        
class Carryable (object):
    """Allows objects to be stored in containers"""
    def __init__ (self, **kwargs):
        self.is_carryable = True
        self.in_container = None
        self.weight = 1.0
        super(Carryable,self).__init__ (**kwargs)
    
class Container (object):
    """Gives objects the capability to hold other objects"""
    def __init__ (self, **kwargs):
        self.is_container = True
        self.items = []
        super(Container,self).__init__ (**kwargs)
        
    def placeItem (self, item):
        """Adds the provided carriable item to the inventory. 
           Runs an 'onStoreItem' script, if present"""    
        if not item.trueAttr ('carryable'):
            raise ValueError ('% is not carriable!' % item)
        item.in_container = self
        self.items.append (item)
        # Run any scripts associated with storing an item in the container
        if self.trueAttr ('scriptable'):
            self.runScript('onPlaceItem')
        
    def takeItem (self, item):
        """Takes the listed item out of the inventory. 
           Runs an 'ontakeItem' script"""        
        if not item in self.items:
            raise ValueError ('I do not contain this item: %s' % item)
        self.items.remove (item)
        # Run any scripts associated with popping an item out of the container
        if self.trueAttr ('scriptable'):
            self.runScript('ontakeItem')
        
class Inventory (object):
    """Aggregate class for things that have multiple Containers"""
    def __init__ (self, **kwargs):
        self.is_inventory = True
        self.containers = []
        super(Inventory,self).__init__ (**kwargs)
    
class Living (object):
    def __init__ (self, **kwargs):
        self.is_living = True
        super(Living,self).__init__ (**kwargs)
    def die(self):
        self.is_living = False
        
class Scriptable (object):
    """Allows objects to have predefined scripts executed on certain events"""
    def __init__ (self, scripts = {}, **kwargs):
        """Init operation for scriptable objects
           @type scripts: Dictionary
           @param scripts: Dictionary where the event strings are keys. The 
           values are 3-item tuples (function, positional_args, keyword_args)"""
        self.is_scriptable = True
        self.scripts = scripts 
        super(Scriptable,self).__init__ (**kwargs)
        
    def runScript (self, event):
        """Runs the script for the given event"""
        if event in self.scripts and self.scrpits[event]:
            func, args, kwargs = self.scrpits[event]
            func (*args, **kwargs)
            
    def setScript (self, event, func, args = [] , kwargs={}):
        """Sets a script to be executed for the given event."""
        self.scripts[event] = (func, args, kwargs)

class CharStats (object):
    """Provides the object with character statistics"""
    def __init__ (self, **kwargs):
        self.is_charstats = True
        super(CharStats,self).__init__ (**kwargs)
        
class Wearable (object):
    def __init__ (self, **kwargs):
        """Allows the object to be weared somewhere on the body (e.g. pants)"""
        self.is_wearable = True
        super(Wearable,self).__init__ (**kwargs)
    
class Usable (object):
    """Allows the object to be used in some way (e.g. a Zippo lighter 
       to make a fire)"""
    def __init__ (self, **kwargs):
        self.is_usable = True
        super(Usable,self).__init__ (**kwargs)
        
class Weapon (object):
    """Allows the object to be used as a weapon"""
    def __init__ (self, **kwargs):
        self.is_weapon = True
        super(Weapon,self).__init__ (**kwargs)
        
class Destructable (object):
    """Allows the object to be destroyed"""
    def __init__ (self, **kwargs):
        self.is_destructable = True
        super(Destructable,self).__init__ (**kwargs)
        
class Trappable (object):
    """Provides trap slots to the object"""
    def __init__ (self, **kwargs):
        self.is_trappable = True
        super(Trappable,self).__init__ (**kwargs)
        
if __name__=="__main__":
    """This will be turned into a test suite"""
    class Wildcard (GameObject, Lockable, Container, Living, Scriptable, 
                    CharStats, Wearable, Usable, Weapon, Destructable,
                    Trappable, Carryable, ):
        def __init__ (self, ID, *args, **kwargs):
            super(Wildcard,self).__init__ (ID, *args, **kwargs)
            self.name = 'All-purpose carry-all'
            self.text = 'What is this? I dont know'    
    
    test = GameObject (1, {'map':'img/test.png'}, (1,1), None, 'Test object','Description')
    print test
    assert test.X == 1
    assert test.Y == 1
    assert test.coords == (1,1)
    test.coords = (2,2)
    assert test.X == 2.0
    assert test.Y == 2.0
    
    wc = Wildcard (2)
    print wc
    print wc.is_carryable

