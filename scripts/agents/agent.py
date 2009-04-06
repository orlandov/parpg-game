import fife

class Agent(fife.InstanceActionListener):
    """Base class for all NPC's and the main character"""
    def __init__(self, model, agentName, layer, uniqInMap=True):
		fife.InstanceActionListener.__init__(self)
		self.model = model
		self.agentName = agentName
		self.layer = layer
		if uniqInMap:
			self.agent = layer.getInstance(agentName)
			self.agent.addActionListener(self)

    def onInstanceActionFinished(self, instance, action):
        """Called when an action is finished - normally overridden"""
        print "No OnActionFinished defined for Agent"

    def start(self):
        """Called when agent first used - normally overridden"""
        print "No start defined for Agent"
