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
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>

import sys, pygame

# place defines here

TILE_WIDTH  =   72
TILE_HEIGHT =   36

# this is very much a simple routine, but we still have a simple class

class TileImage:
    def __init__(self, picture, name):
        self.image = picture
        self.filename = name

def writeXML(name):
    """Write the XML file as well
       Always the same small file so we do it automatically"""
    # we need to strip off the entire path up to the last
    # TODO: this code will not work on windows
    # strip off the png part and replace with the XML
    filename = name.split('/')[-1]
    x_file = open(name[:-4]+".xml","wt")
    x_file.write('''<?fife type="object"?>\n''')
    x_file.write('''<object id="''')
    x_file.write(filename[:-4])
    x_file.write('''" namespace="PARPG" blocking="1" static="1">\n''')
    x_file.write('''    <image source="''')
    x_file.write(filename)
    x_file.write('''" direction="0" />\n''')
    # the \n\n is ESSENTIAL otherwise the XML parser in FIFE craps out!
    x_file.write('''</object>\n\n''')
    x_file.close

def saveFiles(files):
    """Given a list of TileImages, output them as seperate files
       Returns True if it worked"""
    # files is a list of TileImages
    complete = []
    for i in files:
        try:
            pygame.image.save(i.image, i.filename)
            # output the XML file as well
            writeXML(i.filename)
        except:
            print "Error: Failed to save",filename
            # if we saved some anyway, then tell the user
            if(complete != []):
                print "  Managed to save",
                for name in complete:
                    print name,
                print "\n"
            return False
        complete.append(i.filename)
    # seems like all was ok
    return True
            
def splitImage(image, filename, data):
    """Quite complex this, as there are many differing layouts on the
       hexes that we could be dealing with. We blit from left to right
       data holds the hex position changes in [x,y] format.
       by one and the y value staying the same (on the grid map)"""
    # the starting point for the grab is always the middle of the image
    # + half a tile height
    ypos = (image.get_height() / 2) + (TILE_HEIGHT / 2)
    # you only ever grab half
    width = TILE_WIDTH / 2
    # the height is the rest of the image
    height = image.get_height() - ypos
    # and xpos is logical
    xpos = 0
    tiles = []
    new_surface = pygame.Surface((TILE_WIDTH, height), pygame.SRCALPHA, 32)
    new_surface.blit(image, (0, 0), pygame.Rect(0, 0, width, height))
    tiles.append(new_surface)
    xpos += TILE_WIDTH / 2
    last_x = True
    x_offset = 0
    for t in data:
        if((t[1] != 0)and(last_x=True)):
            # switchback, so this tile must fill the whole width
        if(t[1] == 0):
            last_x = False
            # assume +1 for now
        else:
            last_x = True
            # assume +1 for now
            ypos += TILE_HEIGHT / 2
            xpos += TILE_WIDTH / 2
            height += TILE_HEIGHT / 2

    xpos = 0
    file_counter = 0
    tiles = []
    height = image.get_height()
    while(xpos<image.get_width()):
        # create a new surface the same height as the original but
        # with a width of TILE_WIDTH, and with per-pixel alpha
        new_surface = pygame.Surface((TILE_WIDTH, height), pygame.SRCALPHA, 32)
        # now blit a strip of the image across
        if(xpos == 0):
            new_surface.blit(image, (0, 0),
			     pygame.Rect(0, 0, TILE_WIDTH, height))
            # on the first time around, move ahead by the width of a tile
            xpos += TILE_WIDTH
        else:
            # we need to offset into halfway through the tile on other blits
            new_surface.blit(image, ((TILE_WIDTH/2)-1, 0),
                pygame.Rect(xpos, 0, TILE_WIDTH/2, height))
            xpos += (TILE_WIDTH/2)
        # store the image for later
        tiles.append(TileImage(new_surface,
            filename + chr(ord('a')+file_counter) + ".png"))
        file_counter += 1
    return tiles
            
def convertFiles(filename, txt_data):
    """Take a file, slice into seperate images and then save these new images
       as filename0, filename1 ... filenameN
       Returns True if everything worked
       The second string gives the offsets from left to right. The first tile
       on the LHS MUST be in the centre of the image"""
    # first we need to ensure that the data sent is correct. split it up first
    data=txt_data.split(",")
    if(len(data) < 2):
        print "Error: Invalid tile data layout"
        return False
    # validate each data statement
    ndata = []
    for i in data:
        if(((i[0] != 'x')and(i[0] != 'y'))and(i[1].isdigit()==False)):
            # some issue
            print "Error: Can't decode tile string structure"
            return False
        else:
            # make the data a bit easier to understand
            if(i[0] == 'x'):
                ndata.append(int(i[1]),0)
            else:
                ndata.append(0,int(i[1]))
    # then load the file
    try:
        image = pygame.image.load(filename)
    except(pygame.error):
        print "Error: Couldn't load",filename
        return False        
    # check the length of the data, make sure it's long enough...
    if((TILE_WIDTH / 2) * (len(data) + 1)>image.get_width)):
        print "Error: Target GFX too narrow"
        return False   
    # split into seperate files
    # the [:-4] is used to split off the .png from the filename
    images = splitImage(image, filename[:-4], txt_data)
    # save it and we are done
    if(images == []):
        # something funny happened
        print "Error: Couldn't splice given image file"
        return False
    #return(saveFiles(images))

if __name__=="__main__":
    # check we have some options
    if(len(sys.argv) < 3):
        sys.stderr.write("Error: Not enough data given\n")
        sys.exit(False)
    # ok, so init pygame and do it
    pygame.init()
    sys.exit(convertFiles(sys.argv[1], sys.argv[2]))

