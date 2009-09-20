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

from scripts import dialogue
import yaml
import sys

"""
A very simple demonstration of the dialogue engine in effect. It mocks up a
simple user object and allows the dialogue engine to interact with it via
callbacks we provide.
"""

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

def main():

    # set up some closures
    def say_cb(state, text):
        print "NPC says:", text

    def get_reply(responses):
        for i, response in enumerate(responses):
            print "%d. %s" % (i, response)
        print "\nChoose a response: ",
        val = int(sys.stdin.readline().strip())
        print "you picked %s" % (val,)
        return val

    def start_quest(state, quest):
        print "You've picked up the '%s' quest!" % quest,
        state['pc'].startQuest(quest)

    def complete_quest(state, quest):
        print "You've finished the '%s' quest" % quest
        state['pc'].completeQuest(quest)

    callbacks = {
        "say": say_cb,
        "start_quest": start_quest,
        "complete_quest": complete_quest
    }

    pc = Player()

    state = {
        'quests': {},
        'pc': pc
    }

    dialog = dialogue.DialogueEngine('dialogue/sample.yaml', callbacks, state)
    responses = dialog.run()
    while responses:
        choice = get_reply(responses)
        responses = dialog.reply(choice)

if __name__ == "__main__":
    main()
