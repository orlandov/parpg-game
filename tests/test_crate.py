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
from scripts.objects.containers import WoodenCrate

class TestWoodenCrate(unittest.TestCase):
    def setUp(self):
        self.crate = WoodenCrate(ID='crate01')
        self.crate2 = WoodenCrate(ID='crate02', locked=False)

    def testCreation(self):
        """ Test the WoodenCrate creation"""
        self.assertEqual(self.crate.ID, 'crate01')
        self.assertEqual(self.crate.name, 'Wooden Crate')
        self.assertEqual(self.crate.text, 'A battered crate')
        self.assertEqual(self.crate.gfx, 'crate')
        self.assertEqual(self.crate.coords, (0.0, 0.0))
        self.assertEqual(self.crate.map_id, None)
        self.assertEqual(self.crate.blocking, True)
        self.assertEqual(self.crate.is_open, True)
        self.assertEqual(self.crate.locked, True)
        self.assertEqual(self.crate.scripts, {})

        self.assertEqual(self.crate2.ID, 'crate02')
        self.assertEqual(self.crate2.locked, False)

    # can't test containing functionality...there are no containable objects

    def testLockable(self):
        """ Test the WoodenCrate lockability"""
        self.crate2.lock()
        self.assertEqual(self.crate2.locked, True)
        self.crate2.unlock()
        self.assertEqual(self.crate2.locked, False)
