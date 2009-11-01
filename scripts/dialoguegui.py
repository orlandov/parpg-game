#!python

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

import pychan
import fife
import pychan.widgets as widgets
from scripts.dialogue import DialogueEngine

class DialogueGUI(object):
    def __init__(self, npc, quest_engine, pc):
        self.pc = pc

        # define dialogue engine callbacks
        def start_quest(state, quest):
            print "You've picked up the '%s' quest!" % quest
            state['quest'].addQuest(quest)

        def complete_quest(state, quest_id):
            print "You've finished the quest %s" % quest_id
            state['quest'].finishQuest(quest_id)

        def delete_quest(state, quest_id):
            print "You've deleted quest %s" % quest_id
            state['quest'].deleteQuest(quest_id)

        def increase_value(state, quest_id, variable, value):
            print "Increased %s by %i"%(variable,value)
            state['quest'][quest_id].increaseValue(variable,value)

        def decrease_value(state, quest_id, variable, value):
            print "Decreased %s by %i"%(variable,value)
            state['quest'][quest_id].decreaseValue(variable,value)

        def set_value(state,quest_id, variable, value):
            print "Set %s to %i"%(variable,value)
            state['quest'][quest_id].setValue(variable,value)

        def meet(state, npc):
            print "You've met %s!" % npc
            state['pc'].meet(npc)

        def get_stuff(state, thing):
            if thing not in state['pc'].inventory:
                state['pc'].inventory.add(thing)
                print "You've now have the %s" % thing

        def take_stuff(state,thing):
            if thing in state['pc'].inventory:
                state['pc'].inventory.remove(thing)
                print "You no longer have the %s" % thing

        dialogue_callbacks = {
            "complete_quest": complete_quest,
            "decrease_value": decrease_value,
            "delete_quest": delete_quest,
            'end': self.handleEnd,
            "get_stuff" : get_stuff,
            "increase_value": increase_value,
            "meet": meet,
            'npc_avatar': self.handleAvatarImage,
            'responses': self.handleResponses,
            'say': self.handleSay,
            "set_value": set_value,
            "start_quest": start_quest,
            "take_stuff" : take_stuff
        }

        self.npc = npc
        state = {
            'pc': self.pc,
            'quest': quest_engine
        }
        self.dialogue_engine = DialogueEngine(npc.dialogue,
                                              dialogue_callbacks, state)
        self.dialogue_gui = pychan.loadXML("gui/dialogue.xml")

    def initiateDialogue(self):
        """Callback for starting a quest"""
        stats_label = self.dialogue_gui.findChild(name='stats_label')
        stats_label.text = u'Name: Ronwell\nA grizzled villager'

        events = {
            'end_button': self.handleEnd
        }
        self.dialogue_gui.mapEvents(events)
        self.dialogue_gui.show()
        responses_list = self.dialogue_gui.findChild(name='choices_list')
        responses = self.dialogue_engine.run()
        self.setResponses(responses)

    def handleSay(self, state, say):
        """Callback for NPC speech"""
        speech = self.dialogue_gui.findChild(name='speech')
        # to append text to npc speech box, uncomment the following line
        #speech.text = speech.text + "\n-----\n" + unicode(say)
        speech.text = unicode(say)

    def handleEntered(self, *args):
        """Callback for when user hovers over response label"""
        pass

    def handleExited(self, *args):
        """Callback for when user hovers out of response label"""
        pass

    def handleClicked(self, *args):
        """Handle a response being clicked"""
        response = int(args[0].name.replace('response', ''))
        if not self.dialogue_engine.reply(response):
            self.handleEnd()

    def handleEnd(self):
        """Handle the end of the conversation being reached. Either from the
           GUI or from within the conversation itself."""
        self.dialogue_engine = None
        self.dialogue_gui.hide()
        self.npc.behaviour.state = 1
        self.npc.behaviour.idle()

    def handleAvatarImage(self, state, image):
        """Callback to handle when the dialogue engine wants to set the NPC image
           @type image: str
           @param image: filename of avatar image"""
        avatar_image = self.dialogue_gui.findChild(name='npc_avatar')
        avatar_image.image = image

    def handleResponses(self, *args):
        """Callback to handle when the dialogue engine wants to display a new
           list of options"""
        self.setResponses(args[1])

    def setResponses(self, responses):
        """Creates the list of clickable response labels and sets their
           respective on-click callbacks
           @type responses: [ [ "response text", section, condition ], ...]
           @param responses: the list of response objects from the dialogue
                             engine"""
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
            button.margins = (5,5)
            button.background_color = fife.Color(0,0,0)
            button.color = fife.Color(0,255,0)
            button.border_size = 0
            button.wrap_text = 1
            button.capture(lambda button=button: self.handleEntered(button), \
                           event_name='mouseEntered')
            button.capture(lambda button=button: self.handleExited(button), \
                           event_name='mouseExited')
            button.capture(lambda button=button: self.handleClicked(button), \
                           event_name='mouseClicked')
            choices_list.addChild(button)
            self.dialogue_gui.adaptLayout(True)


