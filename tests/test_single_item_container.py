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
from scripts.objects.base import GameObject, Carryable
from scripts.objects.composed import SingleItemContainer

class  TestSingleItemContainer(unittest.TestCase):

    class CarryableObject (GameObject, Carryable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Carryable.__init__(self, **kwargs)


    def setUp(self):
        self.item = self.CarryableObject(6)
        self.item2 = self.CarryableObject(7)

    def tearDown(self):
        self.item = None
        self.item2 = None


    def testPlaceTake(self):
        """ Test SingleItemContainer Place/Take functions """
        container = SingleItemContainer(ID=5)
        container.placeItem(self.item)
        self.assertRaises(ValueError, container.placeItem, self.item2)
        container.takeItem(self.item)
        self.assertEqual(container.items, [])
        container.placeItem(self.item2)

if __name__ == '__main__':
    unittest.main()

