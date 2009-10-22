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

import logging
import sys
import itertools

class EndException(Exception):
    """EndException is used to bail out from a deeply nested
       runSection/continueWithResponse call stack and end the
       conversation"""
    pass

class ResponseException(Exception):
    """ResponseException is used to bail out from a deeply nested
       runSection/continueWithResponse call stack and allow the user to
       specify a response"""
    pass

class BackException(Exception):
    """BackException is used to bail out from a deeply nested
       runSection/continueWithResponse call stack and rewind the section
       stack"""
    pass

class DialogueEngine(object):
    def __init__(self, obj, callbacks={}, state={}):
        """A very simple dialogue engine for a game.
           d = DialogueEngine(tree, callbacks)
           d = DialogueEngine('screenplay.yaml', callbacks)"""

        if isinstance(obj, dict):
            self.tree = obj
        elif isinstance(obj, str):
            import yaml
            self.tree = yaml.load(file(obj))

        logging.basicConfig(level=logging.INFO)

        self.callbacks = callbacks
        self.state = state

    def run(self):
        """Start running the dialogue engine.
        @returns: list of lists (if requesting a response)
        @returns: None (if at the end of the script)"""
        start_section = self.tree['START']
        self.section_stack = []

        npc_avatar_cb = self.callbacks.get('npc_avatar')
        if npc_avatar_cb:
            npc_avatar_cb(self.state, self.tree['AVATAR'])

        try:
            self.runSection(start_section)
        except EndException:
            # we stopped talking to the NPC
            logging.debug("Reached the end")
            end_cb = self.callbacks.get('end')
            if end_cb:
                end_cb()
            return
        except ResponseException, e:
            return e.args[0]
        except BackException, e:
            self.section_stack.pop(-1)
            try:
                self.runSection(self.section_stack[-1])
                return e
            except ResponseException, e:
                return e.args[0]

    def getSection(self, section_name):
        """Return a section object.
        @type section_name: string
        @param section_name: The section to get
        @return: dict"""
        return self.tree['SECTIONS'][section_name]

    def reply(self, response):
        """After being prompted to provide a response, reply is called to
           submit a response.
           @type choice: int
           @param choice: the index of the response to submit
           @return: list of lists (if requesting a response)
           @return: None (if at the end of the script)"""
        while True:
            try:
                if response is not None:
                    self.continueWithResponse(self.section_stack[-1], \
                                                response)
                else:
                    self.runSection(self.section_stack[-1])
            except ResponseException, e:
                logging.debug("Got response exception %s" % (e.args, ))
                return e.args[0]
            except BackException, e:
                # e.args contains the section to jump back to
                if e.args:
                    stack = self.section_stack[:]
                    stack.reverse()
                    for i,s in enumerate(stack):
                       if s == e.args[0]:
                           # remove the end of the section stack up to desired
                           # section
                           del self.section_stack[-i:]
                           break
                else:
                    self.section_stack.pop(-1)
                response = None
                continue
            except EndException:
                end_cb = self.callbacks.get('end')
                if end_cb:
                    end_cb()
                logging.debug("Reached the end")
                return

    def continueWithResponse(self, section_name, response):
        """Reply to a response in a section and continue executing dialogue
           script
           @type section_name: str
           @param section_name: the section to continue
           @type response: int
           @param response: the index [0,n-1] of the desired response
           @raises: EndException on end of script
           @raises: BackException on "back" reply
           @return: None"""
        state = self.state
        if len(self.section_stack) > 1:
            if self.section_stack[-1] == self.section_stack[-2]:
                self.section_stack.pop(-1)

        for command in itertools.cycle(self.getSection(section_name)):
            if not command.get('responses'):
                continue

            responses = []
            for r in command.get('responses'):
                cond = r[2:]
                if not cond or eval(cond[0], state, {}):
                    responses.append(r)

            section = responses[response][1]
            logging.debug("User chose %s" % (section,))

            if section == "back":
                raise BackException()
            elif section.startswith("back "):
                raise BackException(section[5:])
            elif section == "end":
                raise EndException()

            self.runSection(section)

    def runSection(self, section_name):
        """Run a section
           @type section_name: string
           @param section_name: The section to run
           @return: None
           @raises: EndException on end of script
           @raises: BackException on "back" reply"""

        state = self.state

        self.section_stack.append(section_name)

        if len(self.section_stack) > 1:
            if self.section_stack[-1] == self.section_stack[-2]:
                self.section_stack.pop(-1)

        logging.debug("In runSection %s %s" % (section_name, \
                                               self.section_stack,))
        for command in itertools.cycle(self.getSection(section_name)):
            if command.get("say"):
                if self.callbacks.get('say'):
                    self.callbacks["say"](state, command["say"])

            elif command.get("responses"):
                responses = []
                for response in command.get('responses'):
                    cond = response[2:]
                    if not cond or eval(cond[0], state, {}):
                        responses.append(response)
                if self.callbacks.get("responses"):
                    self.callbacks["responses"](state, responses)

                raise ResponseException(responses)

            elif command.get("start_quest"):
                self.callbacks["start_quest"](state, \
                                              command.get("start_quest"))

            elif command.get("complete_quest"):
                self.callbacks["complete_quest"](state, \
                                                 command.get("complete_quest"))

            elif command.get("meet"):
                self.callbacks["meet"](state, \
                                                 command.get("meet"))

            elif command.get("get_stuff"):
                self.callbacks["get_stuff"](state, \
                                                 command.get("get_stuff"))

            elif command.get("take_stuff"):
                self.callbacks["take_stuff"](state, \
                                                 command.get("take_stuff"))
                
            elif command.get("dialogue"):
                command = command.get("dialogue")
                if command == "end":
                    # indicate we"d like to stop talking
                    raise EndException
                elif command == "back":
                    raise BackException()
                elif command.startswith("back "):
                    raise BackException(command[5:])
                else:
                    raise Exception("Unknown command %s" % (command,))

            else:
                raise Exception("Unknown command %s %s" % (command,))
