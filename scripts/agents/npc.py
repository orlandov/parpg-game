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

from agent import Agent
from settings import Setting

TDS = Setting()
_STATE_NONE, _STATE_IDLE, _STATE_RUN = xrange(3)

class NPC(Agent):
    """This is the class we use for all NPCs"""
    def __init__(self, model, agentName, layer, uniqInMap=True):
        super(NPC, self).__init__(model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.idlecounter = 1
        #self.speed=float(TDS.readSetting("PCSpeed"))

    def onInstanceActionFinished(self, instance, action):
        self.idle()
        if action.getId() != 'stand':
            self.idlecounter = 1
        else:
            self.idlecounter += 1

    def start(self):
        self.idle()

    def idle(self):
        self.state = _STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation())

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('run',location,self.speed)

