# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from scripts.objects.base import GameObject

class GameObjectTest(unittest.TestCase):
    def setUp(self):
        self.game_object=GameObject (1, {'map':'img/test.png'},
                           1, 1, None, True, 'Test object', 'Description')
    

    def tearDown(self):
        self.game_object = None

    def testCoords(self):
        self.assertEqual(self.game_object.coords, (1, 1))
        self.assertEqual(self.game_object.X, 1)
        self.assertEqual(self.game_object.Y, 1)
        self.game_object.coords = (2,2)
        self.assertEqual(self.game_object.X, 2.0)
        self.assertEqual(self.game_object.Y, 2.0)

    def testTrueAttr(self):
        self.game_object.is_test=True
        self.game_object.is_test2=False
        self.assertEqual(self.game_object.trueAttr('test'),True)
        self.assertEqual(self.game_object.trueAttr('test2'),False)
        self.assertEqual(self.game_object.trueAttr('test3'),False)

    def testRepr(self):
        self.assertEqual(repr(self.game_object), "<Test object:1>")


if __name__ == '__main__':
    unittest.main()

