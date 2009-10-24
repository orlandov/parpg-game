#!/usr/bin/python

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

import unittest
from scripts.inventory import Inventory
from scripts.objects.base import GameObject, Carryable

class  TestInventory(unittest.TestCase):
    class CarryableObject (GameObject, Carryable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Carryable.__init__(self, **kwargs)

    def setUp(self):
        self.item = self.CarryableObject(12)
        self.item.weight = 12
        self.item2 = self.CarryableObject(13)
        self.item2.weight = 13
        self.inventory = Inventory(ID=11)

    def testPlaceTakeMove(self):
        """Test Inventory Place/Take/Move functions"""
        self.assertTrue(self.inventory.isSlotEmpty("backpack"))
        self.inventory.placeItem(self.item)
        self.assertTrue(self.item in self.inventory.getItemsInSlot("backpack"))
        self.assertEqual(self.inventory.weight, 12)
        self.assertEqual(self.inventory.count(), 1)
        self.assertFalse(self.inventory.isSlotEmpty("backpack"))

        self.inventory.moveItemToSlot(self.item, "groin")
        self.assertFalse(self.item in self.inventory.getItemsInSlot("backpack"))
        self.assertTrue(self.item in self.inventory.getItemsInSlot("groin"))
        self.assertEqual(self.inventory.count(), 1)
        
        self.assertRaises(ValueError, self.inventory.moveItemToSlot, self.item2, "somewhere")
        
        self.inventory.moveItemToSlot(self.item2, "chest")
        self.assertEqual(self.inventory.count(),2)
        self.assertEqual(self.inventory.weight, 12+13)
        self.assertTrue(self.item2 in self.inventory.getItemsInSlot("chest"))

        self.inventory.takeItem(self.item)
        self.assertEqual(self.inventory.count(),1)
        self.assertEqual(self.inventory.weight, 13)

    def testReplace(self):
        """Test Inventory items replace each other in single-item slots"""
        self.inventory.placeItem(self.item)
        self.inventory.moveItemToSlot(self.item,"neck")
        self.assertFalse(self.inventory.isSlotEmpty("neck"))
        self.assertTrue(self.item in self.inventory.getItemsInSlot("neck"))

        self.inventory.moveItemToSlot(self.item2, "neck")
        self.assertFalse(self.inventory.isSlotEmpty("neck"))
        self.assertTrue(self.item2 in self.inventory.getItemsInSlot("neck"))
        self.assertFalse(self.item in self.inventory.getItemsInSlot("neck"))
        
if __name__ == '__main__':
    unittest.main()

