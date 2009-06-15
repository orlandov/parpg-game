#!/usr/bin/python

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# a simple class to hold the information about objects (not NPC's, but
# can be interacted with)

class GameObject:
    """Class to handle GameObjects"""
    def __init__(self, data):
        """Init is a little complicated becuase we have 2 types of
           constructors in one function
           display -> true, we display on screen
           xpos, ypos -> position in map
           gfx -> img data (the FIFE reference)
           text -> descriptive text
           owner -> what it is contained in
           contain -> True / False is it a container
           carry -> True / False it can be carried
           @type data: list
           @param data: List of data for the object
           @return: None"""
        if(data[0] == True):
            self.display = True
            self.xpos = int(float(data[1]))
            self.ypos = int(float(data[2]))
            self.gfx = data[3]
            self.id = data[4]
            self.text = data[5]
            self.container = data[6]
            self.carry = data[7]
            self.owner = None
        else:
            self.display = False
            self.xpos = None
            self.ypos = None
            self.gfx = data[1]
            self.id = data[2]
            self.text = data[3]
            self.owner = data[4]
            self.container = data[5]
            self.carry = data[6]
        # convert the data
        if(self.container == u'1'):
            self.container = True
        else:
            self.container = False
        if(self.carry == u'1'):
            self.carry = True
        else:
            self.carry= False

