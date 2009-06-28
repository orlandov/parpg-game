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


class GameObject (object):
    """A base class that should be inherited by all interactable game objects"""
    def __init__ (self, ID, gfx = {}, coords = (0.0,0.0), mapref = None, 
                  name="Generic object", text="Item description", *args, **kwargs):
        """Set the basic values that are shared by all game objects.
        @type ID: String
        @param ID: Unique object identifier. Must be present.
        @type gfx: Dictionary
        @param gfx: Dictionary with graphics for the different contexts       
        @type coords 2-item tuple
        @param coords: Initial coordinates of the object.
        @type mapref: ???
        @param mapref: Reference to the map where the object is located
        @type name: String
        @param name: The display name of this object (e.g. 'Dirty crate')
        @type text: String
        @param text: A longer description of the item
        """
        self.ID = ID
        self.gfx = gfx
        self.X, self.Y = float(coords[0]), float (coords[1])
        self.mapref = mapref
        self.name = name
        self.text = text
        super(GameObject,self).__init__ (**kwargs)
        
    def trueAtrr (self, attr):
        """Shortcut function to check if the current object has a member named
        is_%attr and if that attribute evaluates to True"""
        return hasattr(self,'is_%s' % attr) and getattr(self, 'is_%s' % attr)

    def _getCoords(self):
        """Get-er property function"""
        return (self.X, self.Y)
    
    def _setCoords (self, coords):
        """Set-er property function"""
        self.X, self.Y = float(coords[0]), float (coords[1])
        
    coords = property (_getCoords, _setCoords, 
        doc = "Property allowing you to get and set the obejct's coordinates via tuples")
    
    def __repr__ (self):
        """A debugging string representation of the object"""
        return "<%s:%s>" % (self.name, self.ID)

class Openable(object):
    def __init__ (self, is_open = True, **kwargs):
        self.is_openable = True
        self.is_open = is_open
        super(Openable,self).__init__ (**kwargs)
    
    def open(self):
        self.is_open = True
    
    def close(self):
        self.is_closed = True
        
class Lockable (Openable):
    def __init__ (self, locked = True, **kwargs):
        self.is_lockable = True
        self.locked = locked
        super(Lockable,self).__init__ (**kwargs)
        
    def unlock (self):
        self.locked = False
        self.close()        
        
    def lock (self):
        self.locked = True
        self.is_open = False
        
class Carryable (object):
    def __init__ (self, **kwargs):
        self.is_carryable = True
        self.in_container = None
        self.weight = 1.0
        super(Carryable,self).__init__ (**kwargs)
    
class Container (object):
    def __init__ (self, **kwargs):
        self.is_container = True
        self.items = []
        super(Container,self).__init__ (**kwargs)
        
    def storeItem (self, item):
        if not item.trueAttr ('carryable'):
            raise ValueError ('% is not carriable!' % item)
        item.in_container = self
        self.items.append (item)
        
    def popItem (self, item, newcontainer):
        if not item in self.items:
            raise ValueError ('I do not contain this item: %s' % item)
        self.items.remove (item)
        newcontainer.putItem (item)
        
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
    def __init__ (self, scripts = {}, **kwargs):
        self.is_scriptable = True
        self.scripts = scripts 
        super(Scriptable,self).__init__ (**kwargs)
        
    def runScript (self, script_name):
        if script_name in self.scripts and self.scrpits[script_name]:
            func, args, kwargs = self.scrpits[script_name]
            func (*args, **kwargs)

class CharStats (object):
    def __init__ (self, **kwargs):
        self.is_charstats = True
        super(CharStats,self).__init__ (**kwargs)
        
class Wearable (object):
    def __init__ (self, **kwargs):
        self.is_wearable = True
        super(Wearable,self).__init__ (**kwargs)
    
class Usable (object):
    def __init__ (self, **kwargs):
        self.is_usable = True
        super(Usable,self).__init__ (**kwargs)
        
class Weapon (object):
    def __init__ (self, **kwargs):
        self.is_weapon = True
        super(Weapon,self).__init__ (**kwargs)
        
class Destructable (object):
    def __init__ (self, **kwargs):
        self.is_destructable = True
        super(Destructable,self).__init__ (**kwargs)
        
class Trappable (object):
    def __init__ (self, **kwargs):
        self.is_trappable = True
        super(Trappable,self).__init__ (**kwargs)
        
if __name__=="__main__":
    """This will be turned into a test suite"""
    
    class Wildcard (GameObject, Lockable, Container, Living, Scriptable, CharStats, Wearable,
                    Usable, Weapon, Destructable, Trappable, Carryable, ):
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
            