#!/usr/bin/python
import sys, os, unittest

def _jp(path):
    return os.path.sep.join(path.split('/'))

_paths = ('../../engine/swigwrappers/python', '../../engine/extensions')
for p in _paths:
    if p not in sys.path:
        sys.path.append(_jp(p))

from scripts.tests.classTests import WoodenCrateTest

if __name__ == '__main__':
    unittest.main()
