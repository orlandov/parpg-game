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
from scripts.objects.actors import NonPlayerCharacter

class MockLayer(object):
    """Mock Layer Object"""
    def getId(self):
        return 1

class TestNonPlayerCharacter(unittest.TestCase):
    def setUp(self):
        self.npc=NonPlayerCharacter(1, MockLayer(), 'Ronnie Dobbs')
    
    def tearDown(self):
        self.npc = None

    def testTrueAttr(self):
        """Test NPC trueAttr functionality"""
        self.assertEqual(self.npc.trueAttr('living'), True)
        self.assertEqual(self.npc.trueAttr('charstats'), True)

    def testRepr(self):
        """Test NPC textual representation"""
        self.assertEqual(repr(self.npc), "<Ronnie Dobbs:1>")

    def testName(self):
        """Test NPC name"""
        self.assertEqual(self.npc.name, "Ronnie Dobbs")

if __name__ == '__main__':
    unittest.main()

