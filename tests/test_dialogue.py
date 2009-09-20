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

import sys
import unittest
from scripts.dialogue import DialogueEngine

class TestDialogue(unittest.TestCase):
    def setUp(self):
        self.tree = {
            'START': 'main',
            'SECTIONS': {
                'main': [
                    { "say": "Greetings stranger" },
                    { "responses": [
                        ["Hi, can you tell me where I am?", "friendly"],
                        ["Watch your words", "aggro"],
                        ["This one toggles", "toggles", "show == True"],
                        ["Always display this one", "display", "True and True"],
                        ["response3", "stop"],
                    ] }
                ],
                'friendly': [
                    { "say": "You sure are lost" },
                    { "responses": [
                        ["Thanks, I know", "thanks"],
                        ["Wait what did you say before?", "back"],
                    ] }
                ],
                'thanks': [
                    { "say": "We haven't seen one of your kind in ages" },
                    { "responses": [
                        ["Blah blah blah", "foo"],
                        ["Say the other thing again", "back"],
                    ] }
                ],
            }
        }
        # record actions in test_vars
        test_vars = { "say": None, "responses": [] }

        def say_cb(state, text):
            state["say"] = text

        self.replies = ["resp1", "back", "stop"]

        def responses_cb(state, responses):
            state['responses'] = responses

        callbacks = {
            "say": say_cb,
            "responses": responses_cb
        }

        self.dialogue = DialogueEngine(self.tree, callbacks, test_vars)

    def assert_say(self, text):
        self.assertEqual(text, self.dialogue.state['say'])

    def assert_responses(self, responses):
        self.assertEqual(responses, self.dialogue.state['responses'])

    def test_simple(self):
        """Test basic dialogue interaction"""
        self.dialogue.state['show'] = False
        self.dialogue.run()

        self.assert_say('Greetings stranger')
        self.assert_responses([
            ["Hi, can you tell me where I am?", "friendly"],
            ["Watch your words", "aggro"],
            ["Always display this one", "display", "True and True"],
            ["response3", "stop"],
        ])
        self.dialogue.reply(0)

        self.assert_say('You sure are lost')
        self.assert_responses([
            ["Thanks, I know", "thanks"],
            ["Wait what did you say before?", "back"]
        ])
        self.dialogue.state['show'] = True
        self.dialogue.reply(1)

        self.assert_say('Greetings stranger')
        self.assert_responses([
            ["Hi, can you tell me where I am?", "friendly"],
            ["Watch your words", "aggro"],
            ["This one toggles", "toggles", "show == True"],
            ["Always display this one", "display", "True and True"],
            ["response3", "stop"],
        ])
        self.dialogue.reply(0)

        self.assert_say('You sure are lost')
        self.dialogue.reply(1)

        self.assert_say('Greetings stranger')
        self.dialogue.reply(0)

        self.assert_say('You sure are lost')
        self.dialogue.reply(0)

        self.assert_say("We haven't seen one of your kind in ages")
        self.dialogue.reply(1)

        self.assert_say('You sure are lost')
        self.dialogue.reply(1)

        self.assert_say('Greetings stranger')

if __name__ == "__main__":
    unittest.main()
