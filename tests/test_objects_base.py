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
from scripts.objects.base import *

class TestObjectsBase(unittest.TestCase):

    def testWildcard(self):
        class Wildcard (GameObject, Lockable, Container, Living, Scriptable,
                        CharStats, Wearable, Usable, Weapon, Destructable,
                        Trappable, Carryable, ):
            def __init__ (self, ID, *args, **kwargs):
                self.name = 'All-purpose carry-all'
                self.text = 'What is this? I dont know'
                GameObject.  __init__( self, ID, **kwargs )
                Lockable.    __init__( self, **kwargs )
                Container.   __init__( self, **kwargs )
                Living.      __init__( self, **kwargs )
                Scriptable.  __init__( self, **kwargs )
                CharStats.   __init__( self, **kwargs )
                Wearable.    __init__( self, **kwargs )
                Usable.      __init__( self, **kwargs )
                Weapon.      __init__( self, **kwargs )
                Destructable.__init__( self, **kwargs )
                Trappable.   __init__( self, **kwargs )
                Carryable.   __init__( self, **kwargs )
        wc = Wildcard (2)

        # TODO: need to fill the rest of these tests out

        attrs = dict(
            is_openable = True,
            is_open = True,
            is_lockable = True,
            locked = True,
            is_carryable = True,
            weight = 1.0,
            is_container = True,
            items = [],
            is_living = True,
            is_scriptable = True
        )

        for attr in attrs:
            self.assertEqual(getattr(wc, attr), attrs[attr])
