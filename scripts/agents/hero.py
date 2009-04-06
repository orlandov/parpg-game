from agent import Agent
from settings import Setting

TDS = Setting()
_STATE_NONE, _STATE_IDLE, _STATE_RUN = xrange(3)

class Hero(Agent):
    """This is the class we use for the PC character"""
    def __init__(self, model, agentName, layer, uniqInMap=True):
        super(Hero, self).__init__(model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.idlecounter = 1
        self.speed=float(TDS.readSetting("PCSpeed"))

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

