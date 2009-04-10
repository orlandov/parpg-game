#!/usr/bin/env python

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

import sys,cPickle
from xml.sax import make_parser
from xml.sax.handler import ContentHandler 

# code is for building the transition layer for the map
# the world map is built of two layers: one for the world floor, and the other
# for the all the objects (including the player and NPC)
# This program accepts one argument, the original XML map file,
# and outputs another file with 1 or more added layers: the layers holding
# the information for the transition tiles that are rendered over the ground

# this is experimental code for the moment
# awaiting rest of tile graphics for full testing

class XMLTileData:
    def __init__(self,x,y,z,o,i=None):
        self.x=x
        self.y=y
        self.z=z
        self.object=o
        self.ident=i

class XMLLayerData:
    """Class to store one complete layer"""
    def __init__(self,x,y,name):
        self.x_scale=x
        self.y_scale=y
        self.name=name
        self.tiles=[]

class LocalXMLParser(ContentHandler):
    """Class inherits from ContantHandler, and is used to parse the
       local map data"""
    def __init__(self):
        self.search="map"
        self.layers=[]
        self.current_layer=False
        self.final=[]
    
    def startElement(self,name,attrs):
        """Called every time we meet a new element"""
        # we are only looking for the 'layer' elements, the rest we ignore
        if(name=="layer"):
            # grab the data and store that as well
            try:
                x=attrs.getValue('x_scale')
                y=attrs.getValue('y_scale')
                name=attrs.getValue('id')
            except(KeyError):
                sys.stderr.write("Error: Layer information invalid")
                sys.exit(False)
            # start a new layer
            self.layers.append(XMLLayerData(x,y,name))
            self.current_layer = True
        elif name == "i":
            # have a current layer?
            if self.current_layer == False:
                sys.stderr.write("Error: item data outside of layer\n")
                sys.exit(False)
            # ok, it's ok, let's parse and add the data
            try:
                x = attrs.getValue('x')
                y = attrs.getValue('y')
                z = attrs.getValue('z')
                o = attrs.getValue('o')
            except(KeyError):
                sys.stderr.write("Error: Data missing in tile definition\n")
                sys.exit(False)
            try:
                i = attrs.getValue('id')
            except(KeyError):
                i = None
            # convert tile co-ords to integers
            x = float(x)
            y = float(y)
            z = float(z)
            # now we have the tile data, save it for later
            self.layers[-1].tiles.append(XMLTileData(x,y,z,o,i))

    def endElement(self,name):
        if(name=="layer"):
            # end of current layer
            self.current_layer=False

class LocalMap:
    def __init__(self):
        self.layers = []
        self.ttile = []
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def OutputTransLayer(self,l_file):
        if(len(ttiles)==0):
            return True
        try:
            l_file.write('''    <layer x_offset="0.0" pathing="')
                          cell_edges_and_diagonals" y_offset="0.0" 
                          grid_type="square" id="TransitionLayer"
                          x_scale="1" y_scale="1" rotation="0.0">\n''')
            l_file.write('        <instances>"')
            for tile in ttile:
                l_file.write('''            <i x="''')
                l_file.write(str(ttile.x))
            	l_file.write('''"" o="''')
            	l_file.write(i.name)
            	l_file.write('''" y="''')
            	l_file.write(str(ttile.y))
            	l_file.write('''" r="0" z="0.0"></i>\n''')
	    	l_file.write('        </instances>\n    </layer>')
	    	l_file.write('</layer>')
        except(IOError):
            sys.stderr.write("Error: Couldn't write data")
            return False
        return True

    def RenderTransLayer(self,search):
        """Build up the data for a transition layer"""
        size=len(search)
        tiles=[]
        trans=[]
        for t in self.layers[0].tiles:
            if t.object!=None and t.object[:size]==search:
                # found a match, now calculate
                tiles.append([t.x,t.y])
                # touch all of the tiles around this one
                if(self.CheckRange(t.x+1,t.y)==True):
                    tiles.append([t.x+1,t.y])
                if(self.CheckRange(t.x+1,t.y-1)==True):
                    tiles.append([t.x+1,t.y-1])
                if(self.CheckRange(t.x+1,t.y-1)==True):
                    tiles.append([t.x+1,t.y-1])
                if(self.CheckRange(t.x,t.y-1)==True):
                    tiles.append([t.x,t.y-1])
                if(self.CheckRange(t.x,t.y+1)==True):
                    tiles.append([t.x,t.y+1])
                if(self.CheckRange(t.x-1,t.y-1)==True):
                    tiles.append([t.x-1,t.y-1])
                if(self.CheckRange(t.x-1,t.y)==True):
                    tiles.append([t.x-1,t.y])
                if(self.CheckRange(t.x-1,t.y+1)==True):
                    tiles.append([t.x-1,t.y+1])
        # now run down the render tiles

    def LoadFromXML(self,filename):
        """Load a map from the XML file used in Fife
           Returns True if it worked, False otherwise"""
        try:
            map_file=open(filename,'rt')
        except(IOError):
            sys.stderr.write("Error: No map given!\n")
            return(False)
        # now open and read the XML file
        parser=make_parser()
        curHandler=LocalXMLParser()
        parser.setContentHandler(curHandler)
        parser.parse(map_file)
        map_file.close()
        # make a copy of the layer data
        self.layers=curHandler.layers
        return True
    
    def GetSize(self):
        """GetSize stores both the size of the grid"""
        for t in self.layers[0].tiles:
            if t.x > self.max_x:
                self.max_x = t.x
            if t.x < self.min_x:
                self.min_x = t.x
            if t.y > self.max_y:
                self.max_y = t.y
            if t.y < self.min_y:
                self.min_y = t.y
    
    def CheckRange(self,x,y):
        """Grid co-ords in range?"""
        if((x<self.min_x)or(x>self.max_x)or
           (y<self.min_y)or(y>self.may_y)):
           return False
        return True
    
    def PrintDetails(self):
        """Debugging routine to output some details about the map
           Used to check the map loaded ok"""
        # display each layer, then the details
        for l in self.layers:
            print "Layer id:",l.name
        print "Map Dimensions: X=",(self.max_x-self.min_x)+1,
        print " Y=",(self.max_y-self.min_y)+1

if __name__=="__main__":
    # pass a map name as the first argument
    if(len(sys.argv)<2):
        sys.stderr.write("Error: No map given!\n")
        sys.exit(False)
    new_map=LocalMap()
    if(new_map.LoadFromXML(sys.argv[1])==True):
        new_map.GetSize()
        new_map.RenderTransLayer("grass")
        new_map.PrintDetails()

