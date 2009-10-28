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
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.

from scripts import dialogue
from scripts import quest_engine
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
        self.inventory = set(['beer'])
        self.peopleIknow = set()

    def meet(self,npc):
        if npc in self.peopleIknow:
            raise RuntimeError("I already know %s" % npc)
        self.peopleIknow.add(npc)

    def met(self,npc):
        return npc in self.peopleIknow


class Beer(object):
    quality = 3


class Box(object):
    """
    Mock box object than can be opened or closed
    This would normally be a container
    """
    def __init__(self):
        self.state = 'closed'

    def isOpen(self):
        if self.state == 'open':
            return self.state
        else:
            return False

    def isClosed(self):
        if self.state == 'closed':
             return self.state
        else:
             return False

    def open(self):
        self.state = 'open'
        return self.state

    def close(self):
        self.state = 'closed'
        return self.state


def main(dialogue_file):

    # set up some closures
    def say_cb(state, text):
        print "NPC says:", text

    def get_reply(responses):
        for i, response in enumerate(responses):
            print "%d. %s" % (i, response)

        while True:
            try:
                print "\nChoose a response: ",
                val = int(sys.stdin.readline().strip())
            except ValueError:
                print "That's not a valid value, amigo"
                continue
            break

        print "you picked %s" % (val,)
        return val

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

    callbacks = {
        "say": say_cb,
        "start_quest": start_quest,
        "complete_quest": complete_quest,
        "delete_quest": delete_quest,
        "increase_value": increase_value,
        "decrease_value": decrease_value,
        "set_value": set_value,
        "meet": meet,
        "get_stuff" : get_stuff,
        "take_stuff" : take_stuff
    }

    pc = Player()
    box = Box()
    quest = quest_engine.QuestEngine()
    beer = Beer()

    state = {
        'quest': quest,
        'pc': pc,
        'box': box,
        'beer': beer
    }

    dialog = dialogue.DialogueEngine(dialogue_file, callbacks, state)
    responses = dialog.run()
    while responses:
        choice = get_reply(responses)
        responses = dialog.reply(choice)

if __name__ == "__main__":
    print "1 - Dialogue sample\n2 - Quest Sample"
    choice = input("> ")
    if choice == 1:
        dialogue_file = 'dialogue/drunkard.yaml'
    elif choice == 2:
        dialogue_file = 'dialogue/quest_sample.yaml'
    if len(sys.argv) > 1:
        dialogue_file = sys.argv[1]

    main(dialogue_file)
