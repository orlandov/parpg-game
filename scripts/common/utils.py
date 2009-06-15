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

# Miscellaneous game functions

import os, sys

# TODO: Having a file like this just looks cheap and 'hackish'. Fix if possible

def addPaths (*paths):
    """Adds a list of paths to sys.path. Paths are expected to use forward
       slashes, for example '../../engine/extensions'. Slashes are converted
       to the OS-specific equivalent.
       @type *paths: ???
       @param *paths: Paths to files?
       @return: None"""
    for p in paths:
        if not p in sys.path:
            sys.path.append(os.path.sep.join(p.split('/')))

