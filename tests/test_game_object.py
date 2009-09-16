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

import unittest
from scripts.objects.base import GameObject

class TestGameObject(unittest.TestCase):
    def setUp(self):
        self.game_object=GameObject (1, {'map':'img/test.png'},
                           1, 1, None, True, 'Test object', 'Description')
    

    def tearDown(self):
        self.game_object = None

    def testCoords(self):
        """ Test GameObject coordinates manipulation"""

        self.assertEqual(self.game_object.coords, (1, 1))
        self.assertEqual(self.game_object.X, 1)
        self.assertEqual(self.game_object.Y, 1)
        self.game_object.coords = (2,2)
        self.assertEqual(self.game_object.X, 2.0)
        self.assertEqual(self.game_object.Y, 2.0)

    def testTrueAttr(self):
        """ Test GameObject trueAttr functionality"""
        
        self.game_object.is_test=True
        self.game_object.is_test2=False
        self.assertEqual(self.game_object.trueAttr('test'),True)
        self.assertEqual(self.game_object.trueAttr('test2'),False)
        self.assertEqual(self.game_object.trueAttr('test3'),False)

    def testRepr(self):
        """ Test GameObject textual representation"""

        self.assertEqual(repr(self.game_object), "<Test object:1>")


if __name__ == '__main__':
    unittest.main()

