#!python

import pychan
import fife
import pychan.widgets as widgets
from scripts.dialogue import DialogueEngine

class Player(object):
    """
    Mock player object that always has complete quests
    """
    def __init__(self):
        self.current_quests = set()
        self.finished_quests = set()

    def canAcceptQuest(self, quest):
        return     quest not in self.finished_quests \
               and quest not in self.current_quests

    def hasSatisfiedQuest(self, quest):
        return quest in self.current_quests

    def startQuest(self, quest):
        if quest in self.current_quests:
            raise RuntimeError("Already have quest, %s" % quest)
        self.current_quests.add(quest)

    def completeQuest(self, quest):
        self.finished_quests.add(quest)
        self.current_quests.remove(quest)

class DialogueGUI(object):
    def __init__(self, npc):
        callbacks = {
            'say': self.handleSay,
            'responses': self.handleResponses,
            'start_quest': self.startQuest,
            'complete_quest': self.completeQuest,
            'end': self.handleEnd
        }
        pc = Player()
        self.npc = npc
        state = {
            'pc': pc
        }
        self.dialogue_engine = DialogueEngine('dialogue/sample.yaml', callbacks, state)
        self.dialogue_gui = pychan.loadXML("gui/dialogue.xml")

    def startQuest(self, state, quest):
        print "You've picked up the '%s' quest!" % quest,
        state['pc'].startQuest(quest)

    def completeQuest(self, state, quest):
        print "You've finished the '%s' quest" % quest
        state['pc'].completeQuest(quest)

    def initiateDialogue(self):
        stats_label = self.dialogue_gui.findChild(name='stats_label')
        stats_label.text = u'Name: Mockup\nType: Awesome'

        events = {
            'end_button': self.handleEnd
        }
        self.dialogue_gui.mapEvents(events)
        self.dialogue_gui.show()
        responses_list = self.dialogue_gui.findChild(name='choices_list')
        responses = self.dialogue_engine.run()
        self.setResponses(responses)

    def handleSay(self, state, say):
        speech = self.dialogue_gui.findChild(name='speech')
        #speech.text = speech.text + "\n-----\n" + unicode(say)
        speech.text = unicode(say)

    def click_response(self):
        pass

    def handle_entered(self, *args):
        pass
    def handle_exited(self, *args):
        pass
    def handle_clicked(self, *args):
        response = int(args[0].name.replace('response', ''))
        
        if not self.dialogue_engine.reply(response):
            self.handleEnd()

    def handleEnd(self):
        self.dialogue_engine = None
        self.dialogue_gui.hide()
        self.npc.behaviour.state = 1
        self.npc.behaviour.idle()

    def handleResponses(self, *args):
        self.setResponses(args[1])

    def setResponses(self, responses):
        choices_list = self.dialogue_gui.findChild(name='choices_list')
        choices_list.removeAllChildren()
        for i,r in enumerate(responses):
            button = widgets.Label(
                name="response%s"%(i,),
                text=unicode(r[0]),
                hexpand="1",
                min_size=(100,16),
                max_size=(490,48),
                position_technique='center:center'
            )
            button.margins=(5,5)
            button.background_color=fife.Color(0,0,0)
            button.color=fife.Color(0,255,0)
            button.border_size = 0
            button.wrap_text = 1
            button.capture(lambda button=button: self.handle_entered(button), event_name='mouseEntered')
            button.capture(lambda button=button: self.handle_exited(button), event_name='mouseExited')
            button.capture(lambda button=button: self.handle_clicked(button), event_name='mouseClicked')
            choices_list.addChild(button)
            self.dialogue_gui.adaptLayout(True)


