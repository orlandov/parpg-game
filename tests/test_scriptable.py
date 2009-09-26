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
from scripts.objects.base import GameObject, Scriptable

class  TestScriptable(unittest.TestCase):
    def setUp(self):
        self.script_ran1=False
        self.script_ran2=False

    def tearDown(self):
        self.scriptable = None

    def script1(self,param1,param2):
        self.script_ran1=True
        self.assertEqual(param1, 'param1')
        self.assertEqual(param2, 'param2')

    def script2(self,param3,param4):
        self.script_ran2=True
        self.assertEqual(param3, 'param3')
        self.assertEqual(param4, 'param4')

    def testScripting(self):
        """Test Scriptable mixin scripting abilities"""
        scriptable = Scriptable()
        scriptable.runScript('script1')
        self.assertFalse(self.script_ran1)
        self.assertFalse(self.script_ran2)
        scriptable = Scriptable({'script1':(self.script1,('param1',),{'param2':'param2'})})
        scriptable.runScript('script1')
        self.assertTrue(self.script_ran1)
        self.assertFalse(self.script_ran2)
        self.script_ran1=False
        scriptable.setScript('script2', self.script2, ('param3',), {'param4':'param4'})
        scriptable.runScript('script2')
        self.assertTrue(self.script_ran2)
        self.assertFalse(self.script_ran1)

if __name__ == '__main__':
    unittest.main()

