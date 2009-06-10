import fife
import pychan

class ContextMenu():
    """
    Arguments:
        menu_items : A list of items containing the name and 
                     text for the menu item and callback
                     i.e. [["menuitem1", "Menu Item 1",  menuCallback1],
                           ["menuitem2", "Menu Item 2", menuCallback2]]
    """
    def __init__(self, engine, menu_items, pos):
        pychan.init(engine, debug = True)
        
        self.vbox = pychan.widgets.VBox(position=pos)
        events_to_map = {}
        
        for item in menu_items:
            p = pychan.widgets.Button(name=item[0], text=unicode(item[1]))
            self.vbox.addChild(p)
            events_to_map[item[0]] = item[2]
            
        self.vbox.mapEvents(events_to_map)
        self.vbox.show()
            
