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

import fife, pychan

class ContextMenu(object):
    def __init__(self, engine, menu_items, pos):
        """@type engine: ???
           @param engine: ??? 
           @type menu_items: list
           @param menu_items: A list of items containing the name and 
                              text for the menu item and callback
                              i.e. [["menu", "Some text",  Callback]
           @type pos: ???
           @param pos: Screen position to use 
           @return: None"""

        self.vbox = pychan.widgets.VBox(position=pos)
        events_to_map = {}
        for item in menu_items:
            p = pychan.widgets.Button(name=item[0], text=unicode(item[1]))
            self.vbox.addChild(p)
            events_to_map [item[0]] = self.action_decorator(*item[2:])
        self.vbox.mapEvents(events_to_map)
        self.show()
    
    def show(self):
        """Shows the context menu"""
        self.vbox.show()
    def hide(self):
        """Hides the context menu"""
        self.vbox.hide()
        
    def action_decorator (self,func, *args, **kwargs):
        """This function is supposed to add some generic that should be
        executed before and/or after an action is fired through the
        context menu.
        
        @type func: Any callable
        @param func: The original action function
        @param args: Unpacked list of positional arguments
        @param kwargs: Unpacked list of keyword arguments
        @return: A wrapped version of func
        """
        
        def decorated_func ():
            """ This is the actual wrapped version of func, that is returned.
            It takes no external arguments, so it can safely be passed around
            as a callback."""
            # some stuff that we do before the actual action is executed
            self.hide()
            # run the action function, and record the return value
            ret_val = func (*args,**kwargs)
            # we can eventually add some post-action code here, if needed (e.g. logging)
            pass        
            # return the value, as if the original function was called
            return ret_val
        return decorated_func
        
