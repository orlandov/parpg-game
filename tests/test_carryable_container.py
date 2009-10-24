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
from scripts.objects.composed import CarryableContainer

class  TestCarryableContainer(unittest.TestCase):

    class CarryableObject (GameObject, Carryable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Carryable.__init__(self, **kwargs)


    def setUp(self):
        self.item = self.CarryableObject(9)
        self.item.weight = 9
        self.item2 = self.CarryableObject(10)
        self.item2.weight = 10

    def tearDown(self):
        self.item = None
        self.item2 = None


    def testWeight(self):
        """ Test CarryableContainer weight calculation"""
        container = CarryableContainer(ID=8)
        self.assertEquals(container.weight, 0)
        container.weight = 8
        self.assertEquals(container.weight, 8)
        container.placeItem(self.item)
        self.assertEquals(container.weight, 8+9)
        container.placeItem(self.item2)
        self.assertEquals(container.weight, 8+9+10)
        container.takeItem(self.item)
        self.assertEquals(container.weight, 8+10)

if __name__ == '__main__':
    unittest.main()

