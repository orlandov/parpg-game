import unittest
from scripts.console import Console

class test_console(unittest.TestCase):
    def setUp(self):
        self.con=Console(None)
        self.invalString="Invalid command, enter help for more information"
        pass
    
    def tearDown(self):
        pass 

    def testConsoleCommandHelp(self):
        """ Test the help console command """
        
        self.assertNotEqual(self.con.handleHelp("help"),self.invalString)
        self.assertNotEqual(self.con.handleConsoleCommand("help"),
                            self.invalString)

    def testConsoleCommandPython(self):
        """ Test the python console command """ 
        self.assertEqual(self.con.handlePython("python 1+1"),"2")
        self.assertEqual(self.con.handleConsoleCommand("python 1+1"),"2")
       
    def testInvalid(self):
        """Test an invalid console command """

        self.assertEqual(self.con.handleConsoleCommand("invalid"),
                         self.invalString)

