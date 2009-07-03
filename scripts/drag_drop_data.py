#/usr/bin/python

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

class DragAndDropData():
    """
    This contains the data that tells the GUI whether something is being dragged, dropped etc.
    It is in one place to allow communication between multiple windows
    """
    def __init___(self):
        """
        @return: None
        """
        self.dragging = False
        self.dragged_image = None
        self.dragged_type = None
        self.dragged_item = None
        self.dropped_type = None
