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

# sounds.py holds the object code to play sounds and sound effects

class SoundEngine:
    def __init__(self, fife_engine):
        self.engine = fife_engine
        self.sound_engine = self.engine.getSoundManager()
        self.sound_engine.init()
        # set up the sound
        self.music = self.sound_engine.createEmitter()
    
    def playMusic(self, sfile = None):
        if(sfile != None):
            # setup the new sound
            sound = self.engine.getSoundClipPool().addResourceFromFile(sfile)
            self.music.setSoundClip(sound)
            self.music.setLooping(True)
        self.music.play()
    
    def pauseMusic(self):
        """Stop current playback"""
        self.music.stop()

    def setVolume(self, volume):
        pass

