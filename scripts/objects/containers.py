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

"""Containes classes defining concrete container game objects like crates,
barrels, chests, etc."""

__all__ = ["WoodenCrate",]

import composed

class WoodenCrate (composed.ImmovableContainer):
    def __init__ (self, ID, name = 'Wooden Crate', \
            text = 'A battered crate', gfx = {'map': 'crate'}, **kwargs):
        super(WoodenCrate,self).__init__ (ID, name = name, gfx = gfx, \
                text = text, **kwargs)
