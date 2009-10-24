# This file is part of PARPG.
# 
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

from scripts.objects.base import GameObject, Container, Carryable
from scripts.objects.composed import CarryableContainer, SingleItemContainer as Slot
import copy

class Inventory(CarryableContainer):
    """The class to represent inventory 'model': allow operations with
    inventory contents, perform weight/bulk calculations, etc"""
    def __init__(self, ID, **kwargs):
        """Initialise instance"""
        CarryableContainer.__init__(self, ID=ID, **kwargs)
        self.items = {"head": Slot(ID), "neck": Slot(ID), "shoulders": Slot(ID),
                      "chest": Slot(ID), "abdomen": Slot(ID), "left_arm": Slot(ID),
                      "right_arm": Slot(ID),"groin": Slot(ID), "hips": Slot(ID),
                      "left_leg": Slot(ID), "right_leg": Slot(ID),
                      "backpack": CarryableContainer(ID)}
        for key,item in self.items.iteritems():
            item.name = key
        self.item_lookup = {}

    def placeItem(self,item):
        self.items["backpack"].placeItem(item)
        self.item_lookup[item.ID] = "backpack"
        
    def takeItem(self,item):
        if not item.ID in self.item_lookup:
            raise ValueError ('I do not contain this item: %s' % item)
        self.items[self.item_lookup[item.ID]].takeItem(item)
        self.item_lookup[item.ID] = None

    def getWeight(self):
        """Total weight of all items in container + container's own weight"""
        return sum((item.weight for item in self.items.values()), self.own_weight)

    def setWeightDummy(self, weight):
        pass

    weight = property(getWeight, setWeightDummy, "Total weight of container")


    def count(self):
        return sum(item.count() for item in self.items.values())
    
    def takeOff(self, item):
        return self.moveItemToSlot(item, "backpack")

    def moveItemToSlot(self,item,slot):
        if not slot in self.items:
            raise(ValueError,"%s: No such slot" % slot)

        if item.ID in self.item_lookup:
            self.items[self.item_lookup[item.ID]].takeItem(item)
        try:
            self.items[slot].placeItem(item)
        except ValueError:
            self.takeOff(self.items[slot].items[0])
            self.items[slot].placeItem(item)
        self.item_lookup[item.ID] = slot
     
    def getItemsInSlot(self, slot):
        if not slot in self.items:
            raise(ValueError,"%s: No such slot" % slot)
        return copy.copy(self.items[slot].items)

    def isSlotEmpty(self, slot):
        if not slot in self.items:
            raise(ValueError,"%s: No such slot" % slot)
        return self.items[slot].count() == 0

    def __repr__(self):
        return "[%s:%s "%(self.name, self.ID)+reduce((lambda a,b: str(a) +', '+str(b)), self.items.values())+" ]"
