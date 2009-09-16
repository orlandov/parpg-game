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

