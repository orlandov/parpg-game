#!python

try:
    import yaml
except:
    pass

import logging
import sys
import itertools

class EndException(Exception):
    """EndException is used to bail out from a deeply nested
       run_section/continue_with_response call stack and end the
       conversation"""
    pass

class ResponseException(Exception):
    """ResponseException is used to bail out from a deeply nested
       run_section/continue_with_response call stack and allow the user to
       specify a response"""
    pass

class BackException(Exception):
    """BackException is used to bail out from a deeply nested
       run_section/continue_with_response call stack and rewind the section
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

        try:
            self.run_section(start_section)
        except EndException:
            # we stopped talking to the NPC
            logging.debug("Reached the end")
            end_cb = self.callbacks.get('end')
            if end_cb: end_cb()
            return
        except ResponseException, e:
            return e.args[0]
        except BackException, e:
            self.section_stack.pop(-1)
            try:
                self.run_section(self.section_stack[-1])
                return e
            except ResponseException, e:
                return e.args[0]

    def get_section(self, section_name):
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
                    self.continue_with_response(self.section_stack[-1], response)
                else:
                    self.run_section(self.section_stack[-1])
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
                if end_cb: end_cb()
                logging.debug("Reached the end")
                return

    def continue_with_response(self, section_name, response):
        """Reply to a response in a section and continue executing dialogue script
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

        for command in itertools.cycle(self.get_section(section_name)):
            if not command.get('responses'): continue

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

            self.run_section(section)

    def run_section(self, section_name):
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

        logging.debug("In run_section %s %s" % (section_name, self.section_stack,))
        for command in itertools.cycle(self.get_section(section_name)):
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
                self.callbacks["start_quest"](state, command.get("start_quest"))

            elif command.get("complete_quest"):
                self.callbacks["complete_quest"](state, command.get("complete_quest"))

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
