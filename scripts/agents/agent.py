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

import fife

class Agent(fife.InstanceActionListener):
    """Base class for all NPC's and the main character"""
    # self.model,'PC',self.agent_layer
    def __init__(self,agentName,layer):
        # add this class for callbacks from fife itself
        fife.InstanceActionListener.__init__(self)
        self.agentName=agentName
        self.agent=layer.getInstance(agentName)
        self.agent.addActionListener(self)

    def onInstanceActionFinished(self, instance, action):
        """Called when an action is finished - normally overridden"""
        raise CodeError("No OnActionFinished defined for Agent")

    def start(self):
        """Called when agent first used - normally overridden"""
        raise CodeError("No start defined for Agent")

