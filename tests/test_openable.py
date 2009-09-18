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
from scripts.objects.base import Scriptable, Openable, GameObject


class TestOpenable(unittest.TestCase):

    class OpenableScriptable (GameObject, Openable, Scriptable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Openable.__init__(self, **kwargs)
            Scriptable.__init__(self, **kwargs)

    class OpenableNonScriptable (GameObject, Openable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Openable.__init__(self, **kwargs)
    
    def onOpen(self):
        self.ran_on_open=True
        
    def onClose(self):
        self.ran_on_close=True

    def setUp(self):   
        self.ran_on_open=False
        self.ran_on_close=False
    
    def testOpenClose(self):
        """ Test Openable mixin open-close functionality"""

        self.openable = self.OpenableNonScriptable(3)
        self.assertEqual(self.openable.is_open,True)

        self.openable.close()
        self.assertEqual(self.openable.is_open,False)
        
        # Duplicate close() should not lead to any ill effects
        self.openable.close()
        self.assertEqual(self.openable.is_open,False)

        self.openable.open()
        self.assertEqual(self.openable.is_open,True)

        # Duplicate open() should not lead to any ill effects
        self.openable.open()
        self.assertEqual(self.openable.is_open,True)

    def testScripting(self):
        """ Test Openable mixin with scripting"""

        self.openable = self.OpenableScriptable(3, scripts={'onOpen':(self.onOpen,(),{}),'onClose':(self.onClose,(),{})})
        self.assertEqual(self.ran_on_close,False)
        self.assertEqual(self.ran_on_open,False)
        self.assertEqual(self.openable.is_open,True)
        self.openable.close()
        self.assertEqual(self.ran_on_close,True)
        self.assertEqual(self.ran_on_open,False)
        self.assertEqual(self.openable.is_open,False)
        self.ran_on_close=False
        self.openable.open()
        self.assertEqual(self.ran_on_close,False)
        self.assertEqual(self.ran_on_open,True)
        self.assertEqual(self.openable.is_open,True)

    def testInitiallyClosed(self):
        """ Test Openable mixin instantiation in closed state"""
        
        self.openable = self.OpenableNonScriptable(3, is_open=False)
        self.assertEqual(self.openable.is_open,False)
        self.openable.open()
        self.assertEqual(self.openable.is_open,True)

if __name__ == '__main__':
    unittest.main()

