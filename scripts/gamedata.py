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

class BaseObjectData(object):
    """Basis for game object data.
    """
    def __init__(self, ident, posx, posy, text, cmap, gfx=None, display=True):
        """Set the basic values that are shared by all game objects.
        @type ident: String
        @param ident: Unique identifier for this object.
        @type posx: Integer
        @param posx: Position X
        @type posy: Integer
        @param posy: Position Y
        @type text: String
        @param text: The caption of this object
        @type cmap: String
        @param cmap: Map where this object is currently located
        @type display: Bool
        @param display: Display this object?
        @type gfx: String
        @param gfx: ???
        @returns: None"""
        self.id = ident
        self.posx = posx
        self.posy = posy
        self.display = display
        self.text = text
        self.map = cmap
        self.gfx = gfx
    
    def __cmp__(self, other):
        """Compares this instance to another.
        @type other: BaseObjectData
        @param other: The other object to compare
        @returns: True if the ids are equal, false otherwise."""
        return self.id == other.id
    
class DoorData(BaseObjectData):
    """Represents a door.
    """
    def __init__(self, ident, posx, posy, text, cmap, gfx, display,
                 owner, destx, desty, destmap):
        """Set initial values
        @type ident: String
        @param ident: Unique identifier for this object.
        @type posx: Integer
        @param posx: Position X
        @type posy: Integer
        @param posy: Position Y
        @type text: String
        @param text: The caption of this object
        @type cmap: String
        @param cmap: Map where this NPC is currently located
        @type display: Bool
        @param display: Display this object?
        @type gfx: String
        @param gfx: ???
        @type owner: ???
        @param owner: The owner of this object
        @type destx: Integer
        @param destx: Target X
        @type desty: Integer
        @param desty: Target Y
        @type destmap: String
        @param destmap: Target map
        @returns: None"""
        super(DoorData, self).__init__(ident, posx, posy, text,
                                       cmap, gfx, display)
        self.destx = destx
        self.desty = desty
        self.owner = owner
        self.destmap = destmap

class NpcData(BaseObjectData):
    """Non Player Character
    """
    def __init__(self, ident, posx, posy, text, cmap, gfx=None, display=True):
        """Set initial NPC values.
        @type ident: String
        @param ident: Unique identifier for this object.
        @type posx: Integer
        @param posx: Position X
        @type posy: Integer
        @param posy: Position Y
        @type text: String
        @param text: The caption of this object
        @type cmap: String
        @param cmap: Map where this NPC is currently located
        @type display: Bool
        @param display: Display this object?
        @type gfx: String
        @param gfx: ???
        @returns: None"""
        super(NpcData, self).__init__(ident, posx, posy, text,
                                      cmap, gfx, display)

class HeroData(NpcData):
    """Hero character, for now equal to a NPC"""
    def __init__(self, ident, posx, posy, text, cmap, gfx=None, display=True):
        """Set initial NPC values.
        @type ident: String
        @param ident: Unique identifier for this object.
        @type posx: Integer
        @param posx: Position X
        @type posy: Integer
        @param posy: Position Y
        @type text: String
        @param text: The caption of this object
        @type cmap: String
        @param cmap: Map where this NPC is currently located
        @type display: Bool
        @param display: Display this object?
        @type gfx: String
        @param gfx: ???
        @returns: None"""
        super(HeroData, self).__init__(ident, posx, posy, text,
                                       cmap, gfx, display)

class NonLivingObjectData(BaseObjectData):
    def __init__(self, ident, posx, posy, text, cmap, gfx=None, display=True, 
                 owner=None, container=False, carryable=False):
        """Set initial object values.
        @type ident: String
        @param ident: Unique identifier for this object.
        @type posx: Integer
        @param posx: Position X
        @type posy: Integer
        @param posy: Position Y
        @type text: String
        @param text: The caption of this object
        @type cmap: String
        @param cmap: Map where this NPC is currently located
        @type owner: ???
        @param owner: The owner of this object
        @type container: Bool
        @param container: Can this a container?
        @type carryable: Bool
        @param carryable: Can this object be carried?
        @type display: Bool
        @param display: Display this object?
        @type gfx: String
        @param gfx: ???
        @returns: None"""
        super(NonLivingObjectData, self).__init__(ident, posx, posy, text, 
                                                  cmap, gfx, display)
        self.container = container
        self.carryable = carryable
        self.owner = owner

class MapDoor:
    """A MapDoor is an item that when clicked transports the player to
       another map"""
    def __init__(self, name, new_map, location):
        """@type name: string
           @param name: name of fife object
           @type new_map: string
           @param new_map: name of new map
           @type location: tuple
           @param location: where to put the PC when map is loaded
           @return: None"""
        self.id = name
        self.map = new_map
        # location is an (int, int) which stores the intended location 
        # of the PC on the new map
        self.targ_coords = location

