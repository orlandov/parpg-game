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

class TeleTile(object):
    """ A simple class to handle tiles that transport the PC. """
    def __init__(self, target, map_tup, targ_tup, layer):
        self.target = target
        self.map_coord = map_tup
        self.targ_coord = targ_tup

    def matchLocation(self, loc):
        """ Checks to see if the map coordinates of the tile is the same
        location as the given location.
        @param loc: a fife.Location object
        @return: True or false, depending on whether or not the tile is a
            match"""
        if self.map_coord[0] == loc.getLayerCoordinates().x and \
                self.map_coord[1] == loc.getLayerCoordinates().y:
            print 'matched'
            return True
        return False
