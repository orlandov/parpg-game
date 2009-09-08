#!/usr/bin/python
import sys, os, unittest

def _jp(path):
    return os.path.sep.join(path.split('/'))

_paths = ('../../engine/swigwrappers/python', '../../engine/extensions','tests')
test_suite = unittest.TestSuite()

for p in _paths:
    if p not in sys.path:
        sys.path.append(_jp(p))

for p in os.listdir("tests") :
    if p[-3:] == ".py" :
        test_suite.addTest(unittest.TestLoader().loadTestsFromName(p[:-3]))

unittest.TextTestRunner(verbosity=2).run(test_suite)