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
from scripts.objects.base import Lockable, GameObject


class  TestLockable(unittest.TestCase):

    class LockableObject (GameObject, Lockable):
        def __init__ (self, ID, **kwargs):
            GameObject.__init__(self, ID, **kwargs)
            Lockable.__init__(self, **kwargs)

    def testConstructor(self):
        """ Test Lockable mixin constructor """
        lockable = self.LockableObject(4)
        self.assertEqual(lockable.locked,False)
        self.assertEqual(lockable.is_open,True)
        lockable = self.LockableObject(4,locked=False,is_open=False)
        self.assertEqual(lockable.locked, False)
        self.assertEqual(lockable.is_open, False)
        lockable = self.LockableObject(4,locked=True)
        self.assertEqual(lockable.locked, True)
        self.assertEqual(lockable.is_open, False)

    def testLockUnlock(self):
        """ Test Lockable mixin locking and unlocking """
        lockable = self.LockableObject(4)
        lockable.open()
        self.assertEqual(lockable.is_open, True)
        lockable.lock()
        self.assertEqual(lockable.locked, True)
        self.assertEqual(lockable.is_open,False)
        self.assertRaises(ValueError, lockable.open)
        lockable.unlock()
        self.assertEqual(lockable.locked, False)
        self.assertEqual(lockable.is_open,False)    

if __name__ == '__main__':
    unittest.main()

