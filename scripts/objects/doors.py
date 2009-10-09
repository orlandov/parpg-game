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

"""Containes classes defining concrete door game objects."""

__all__ = ["ShantyDoor",]

from composed import Door

class ShantyDoor(Door):
    def __init__ (self, ID, name = 'Shanty Door', \
            text = 'A door', gfx = 'shanty-door', target_map_name = 'my-map', \
            target_map = 'map.xml', target_pos = (0.0, 0.0), \
            **kwargs):
        Door.__init__(self, ID = ID, name = name, text = text, gfx = gfx, \
            target_map_name = target_map_name, target_map = target_map, \
            target_pos = target_pos, **kwargs)

