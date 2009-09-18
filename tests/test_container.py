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
from scripts.objects.base import GameObject, Container, Scriptable, Carryable

class  TestContainer(unittest.TestCase):
    class ScriptableContainer (GameObject, Container, Scriptable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Container.__init__(self, **kwargs)
            Scriptable.__init__(self, **kwargs)

    class NonScriptableContainer (GameObject, Container):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Container.__init__(self, **kwargs)

    class CarryableObject (GameObject, Carryable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Carryable.__init__(self, **kwargs)


    def setUp(self):
        self.ranOnPlaceItem = False
        self.ranOnTakeItem = False
        self.item = self.CarryableObject(6)
        self.item2 = self.CarryableObject(7)

    def tearDown(self):
        self.item = None
        self.item2 = None


    def onPlaceItem(self):
        self.ranOnPlaceItem = True

    def onTakeItem(self):
        self.ranOnTakeItem = True
    

    def testPlaceTake(self):
        """ Test Container mixin Place/Take functions """
        container = self.NonScriptableContainer(5)
        self.assertEqual(container.items,[])
        self.assertEqual(self.item.in_container,None)
        container.placeItem(self.item)
        self.assertEqual(container.items,[self.item])
        self.assertEqual(self.item.in_container, container)
        self.assertRaises(ValueError, container.takeItem, self.item2)
        container.takeItem(self.item)
        self.assertEqual(container.items, [])

    def testScripting(self):
        container = self.ScriptableContainer(5,scripts={'onPlaceItem':(self.onPlaceItem,(),{}),'onTakeItem':(self.onTakeItem,(),{})})
        self.assertFalse(self.ranOnPlaceItem)
        self.assertFalse(self.ranOnTakeItem)
        container.placeItem(self.item)
        self.assertTrue(self.ranOnPlaceItem)
        self.assertFalse(self.ranOnTakeItem)
        self.ranOnPlaceItem = False
        container.takeItem(self.item)
        self.assertFalse(self.ranOnPlaceItem)
        self.assertTrue(self.ranOnTakeItem)

if __name__ == '__main__':
    unittest.main()

