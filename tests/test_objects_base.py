#!python

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
