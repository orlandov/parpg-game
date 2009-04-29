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

import sys,pygame

# place defines here

TILE_WIDTH  =   70

# this is very much a simple routine, but we still have a simple class

class TileImage:
    def __init__(self,picture,name):
        self.image=picture
        self.filename=name

def SaveFiles(files):
    """Given a list of TileImages, output them as seperate files
       Returns True if it worked"""
    # files is a list of TileImages
    complete=[]
    for i in files:
        try:
            pygame.image.save(i.image,i.filename)
        except:
            print "Error: Failed to save",filename
            # if we saved some anyway, then tell the user
            if(complete!=[]):
                print "  Managed to save",
                for name in complete:
                    print name,
                print "\n"
            return False
        complete.append(i.filename)
    # seems like all was ok
    return True
            
def SplitImage(image,filename):
    """Quite complex this, as there are many differing layouts on the
       hexes that we could be dealing with. However, for now we assume
       that we blit from left to right, with the image x position increasing
       by one and the y value staying the same (on the grid map)"""
    xpos=0
    file_counter=0
    tiles=[]
    height=image.get_height()
    while(xpos<image.get_width()):
        # create a new surface the same height as the original but
        # with a width of TILE_WIDTH, and with per-pixel alpha
        new_surface=pygame.Surface((TILE_WIDTH,height),pygame.SRCALPHA,32)
        # now blit a strip of the image across
        if(xpos==0):
            new_surface.blit(image,(0,0),pygame.Rect(0,0,TILE_WIDTH,height))
            # on the first time around, move ahead by the width of a tile
            xpos+=TILE_WIDTH
        else:
            # we need to offset into halfway through the tile on other blits
            new_surface.blit(image,((TILE_WIDTH/2)-1,0),
                pygame.Rect(xpos,0,TILE_WIDTH/2,height))
            xpos+=(TILE_WIDTH/2)
        # store the image for later
        tiles.append(TileImage(new_surface,filename+str(file_counter)+".png"))
        file_counter+=1
    return tiles
            
def ConvertFiles(filename):
    """Take a file, slice into seperate images and then save these new images
       as filename0, filename1 ... filenameN
       Returns True if everything worked"""
    # first off, load the file
    try:
        image=pygame.image.load(filename)
    except(pygame.error):
        print "Error: Couldn't load",filename
        return False
    # split into seperate files
    # the [:-4] is used to split off the .png from the filename
    images=SplitImage(image,filename[:-4])
    # save it and we are done
    if(images==[]):
        # something funny happened
        print "Error: Couldn't splice given image file"
        return False
    return(SaveFiles(images))

if __name__=="__main__":
    # check we have some options
    if(len(sys.argv)<2):
        sys.stderr.write("Error: No image given!\n")
        sys.exit(False)
    # ok, so init pygame and do it
    pygame.init()
    sys.exit(ConvertFiles(sys.argv[1]))

