#!/usr/bin/python

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

import sys, os, shutil, re

from scripts.common import utils
# add paths to the swig extensions
utils.addPaths ('../../engine/swigwrappers/python', '../../engine/extensions')

if not os.path.exists('settings.xml'):
    shutil.copyfile('settings-dist.xml', 'settings.xml')

import fife_compat, fife, fifelog
import pychan
from scripts import world
from scripts import engine
from scripts.engine import Engine
from scripts.common import eventlistenerbase
from basicapplication import ApplicationBase
from settings import Setting

TDS = Setting()

"""This folder holds the main meta-data for PARPG. This file should be
   minimal, since folding code into the controller with MVC is usually bad
   All game and logic and data is held held and referenced in /scripts/engine.py
   All fife stuff goes in /scripts/world.py"""

class ApplicationListener(eventlistenerbase.EventListenerBase):
    def __init__(self, engine, world, model):
        """Initialise the instance.
           @type engine: ???
           @param engine: ???
           @type world: ???
           @param world: ???
           @type model: engine.Engine
           @param model: an instance of PARPG's engine"""
        super(ApplicationListener, self).__init__(engine,
                                                  regKeys=True,regCmd=True,
                                                  regMouse=False, 
                                                  regConsole=True,
                                                  regWidget=True)
        self.engine = engine
        self.world = world
        self.model = model
        engine.getEventManager().setNonConsumableKeys([fife.Key.ESCAPE,])
        self.quit = False
        self.aboutWindow = None

    def quitGame(self):
        """Forces a quit game on next cycle.
           @return: None"""
        self.quit = True

    def onConsoleCommand(self, command):
        """
        Called on every console comand
        @type command: string
        @param command: the command to run
        @return: result
        """
        result = None

        if (command.lower() in ('quit', 'exit')):
            self.quitGame()

        load_regex = re.compile('^load')
        l_matches = load_regex.match(command.lower())
        if (l_matches != None):
            end_load = l_matches.end()
            try:
                l_args = command.lower()[end_load+1:].strip()
                l_path, l_filename = l_args.split(' ')
                self.model.load(l_path, l_filename)
                result = "Loaded file: " + l_path + l_filename

            except Exception, l_error:
                self.engine.getGuiManager().getConsole().println('Error: ' + str(l_error))

        save_regex = re.compile('^save')
        s_matches = save_regex.match(command.lower())
        if (s_matches != None):
            end_save = s_matches.end()
            try:
                s_args = command.lower()[end_save+1:].strip()
                s_path, s_filename = s_args.split(' ')
                self.model.save(s_path, s_filename)
                result = "Saved to file: " + s_path + s_filename

            except Exception, s_error:
                self.engine.getGuiManager().getConsole().println('Error: ' + str(s_error))
                   
        else:
            try:
                result = str(eval(command))
            except Exception, e:
                result = str(e)

        if not result:
            result = 'no result'
        
        return result

    def onCommand(self, command):
        """Enables the game to be closed via the 'X' button on the window frame
           @type command: fife.Command
           @param command: The command to read.
           @return: None"""
        if(command.getCommandType() == fife.CMD_QUIT_GAME):
            self.quit = True
            command.consume()

class PARPG(ApplicationBase):
    """Main Application class
       We use an MVC data model.
       self.world is our view,self.engine is our model
       This file is the minimal controller"""
    def __init__(self):
        """Initialise the instance.
           @return: None"""
        super(PARPG,self).__init__()
        self.world = world.World(self.engine)
        self.model = engine.Engine(self.world)
        self.world.data = self.model
        self.listener = ApplicationListener(self.engine,self.world,self.model)
        self.world.quitFunction = self.listener.quitGame
        self.model.loadMap("main_map", str(TDS.readSetting("MapFile")))   
        pychan.init(self.engine, debug = True)

    def loadSettings(self):
        """Load the settings from a python file and load them into the engine.
           Called in the ApplicationBase constructor.
           @return: None"""
        import settings
        self.settings = settings
        eSet=self.engine.getSettings()
        eSet.setDefaultFontGlyphs(str(TDS.readSetting("FontGlyphs",
                                                      strip=False)))
        eSet.setDefaultFontPath(str(TDS.readSetting("Font")))
        eSet.setBitsPerPixel(int(TDS.readSetting("BitsPerPixel")))
        eSet.setInitialVolume(float(TDS.readSetting("InitialVolume")))
        eSet.setSDLRemoveFakeAlpha(int(TDS.readSetting("SDLRemoveFakeAlpha")))
        eSet.setScreenWidth(int(TDS.readSetting("ScreenWidth")))
        eSet.setScreenHeight(int(TDS.readSetting("ScreenHeight")))
        eSet.setRenderBackend(str(TDS.readSetting("RenderBackend")))
        eSet.setFullScreen(int(TDS.readSetting("FullScreen")))
        try:
            eSet.setWindowTitle(str(TDS.readSetting("WindowTitle")))
            eSet.setWindowIcon(str(TDS.readSetting("WindowIcon")))
        except:
            pass            
        try:
            eSet.setImageChunkingSize(int(TDS.readSetting("ImageChunkSize")))
        except:
            pass

    def initLogging(self):
        """Initialize the LogManager.
           @return: None"""
        LogModules = TDS.readSetting("LogModules",type='list')
        self.log = fifelog.LogManager(self.engine,
                                      int(TDS.readSetting("LogToPrompt")),
                                      int(TDS.readSetting("LogToFile")))
        if(LogModules):
            self.log.setVisibleModules(*LogModules)

    def createListener(self):
        """@return: None"""
        # already created in constructor
        # but if we don't put one here, Fife gets all fussy :-)
        pass

    def _pump(self):
        """Main game loop.
           There are in fact 2 main loops, this one and the one in World.
           @return: None"""
        if self.listener.quit:
            self.breakRequested = True
        else:
            self.model.pump()
            self.world.pump()

def main():
    """Application code starts from here"""
    app = PARPG()
    app.run()

if __name__ == '__main__':
    main()

