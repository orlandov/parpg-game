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

import yaml

class Quest(object):
    def __init__(self, quest_id, quest_giver_id, quest_name, description,
                 variables):
        """This holds all the quest information"""
        self.quest_id = quest_id
        self.quest_giver_id = quest_giver_id
        self.quest_name = quest_name
        self.description = description
        self.quest_variables = variables

    def setValue(self, variable_name, value):
        """Set the value of a quest variable
           @param variable_name: the name of the variable to set
           @param value: the value you want to assign to the variable
           @return: True on success
           @return: False when it failes"""

        if self.quest_variables.has_key(variable_name):
            self.quest_variables[variable_name]["value"] = value
            return True
        else:
            return False

    def getValue(self, variable_name):
        """Get the value of a quest_variable
           @param variable_name: the name of the variable to set
           @return: the value of the quest_variable"""
        if self.quest_variables.has_key(variable_name):
            return self.quest_variables[variable_name]["value"]
        else:
            return False

    def getGoalValue(self, variable_name):
        """Get the goal value of a quest_variable
           @param variable_name: the name of the variable to set
           @return: the goal value of the quest variable"""
        if self.quest_variables.has_key(variable_name):
            return self.quest_variables[variable_name]["goal_value"]
        else:
            return False

    def increaseValue(self, variable_name, value):
        """Increase a variable by a specified value
           @param variable_name: the name of the variable to set
           @param value: the value you want to increase the variable with
           @return: True on success
           @return: False when it failes"""
        if self.quest_variables.has_key(variable_name):
            self.quest_variables[variable_name]["value"] += value
            return True
        else:
            return False

    def decreaseValue(self, variable_name, value):
        """Decrease a variable by a specified value
           @param variable_name: the name of the variable to set
           @param value: the value you want to decrease the variable with
           @return: True on success
           @return: False when it failes"""
        if self.quest_variables.has_key(variable_name):
            self.quest_variables[variable_name]["value"] -= value
            return True
        else:
            return False

    def isGoalValue(self, variable_name):
        """Check if the variable has reached it's goal value
           @param variable_name: the name of the variable to check
           @return: True when the variable has reached the goal value
           @return: False when it has not reached the goal value"""
        if self.quest_variables.has_key(variable_name):
            return self.quest_variables[variable_name]["value"] == \
                    self.quest_variables[variable_name]["goal_value"]
        else:
            return False

    def isEqualOrBiggerThanGoalValue(self, variable_name):
        """Check if the variable is equil or bigger then it's goal value
           @param variable_name: the name of the variable to set
           @return: True when it has reached or exceeded the goal value
           @return: False when it has not reached or exceeded the goal value
           """
        if variable_name in self.quest_variables:
            return self.quest_variables[variable_name]["value"] >= \
                             self.quest_variables[variable_name]["goal_value"]
        else:
            return False


class QuestEngine(dict):
    def __init__(self):
        """Create a quest engine object"""
        dict.__init__(self)

        self.empty_quest = Quest(None,None,None,None,{})
        self.active_quests = {}
        self.finished_quests = {}

    def __str__(self):
        return self.active_quests.__str__()

    def __getitem__(self, key):
        try:
            return self.active_quests.__getitem__(key)
        except KeyError:
            return self.empty_quest

    def items(self):
        return self.active_quests.items()

    def values(self):
        return self.active_quests.values()

    def keys(self):
        return self.active_quests.keys()

    def addQuest(self, quest):
        """Add a quest to the quest log
           @param quest: the quest file or tree to add to the quest log
           @return: True if succesfully added
           @return: False if failed to add"""

        if isinstance(quest, str):
            #Convert YAML to Quest
            tree = yaml.load(file(quest))

        if isinstance(quest, dict):
            tree = quest

        quest_properties = tree["QUEST_PROPERTIES"]
        variable_defines = tree["DEFINES"]

        self.active_quests[quest_properties["quest_id"]] = \
                              Quest(quest_properties["quest_id"],
                                    quest_properties["quest_giver_id"],
                                    quest_properties["quest_name"],
                                    quest_properties["description"],
                                    variable_defines)
        return True

    def finishQuest(self, quest_id):
        """Move a quest to the finished quests log
           @param quest_id: The id of the quest you want to move
           @return: True on success
           @return: False when it failes
        """
        if self.active_quests.has_key(quest_id):
            #Transfer to finished list
            self.finished_quests[quest_id] = self.active_quests[quest_id]
            del self.active_quests[quest_id]
            return True
        elif self.finished_quests.has_key(quest_id):
            #Temporary fix
            return True

        else:
            return False

    def hasQuest(self, quest_id):
        """Check wether a quest is in the quest log
           @param quest_id: ID of the quest you want to check
           @return: True on when the quest is in the quest log
           @return: False when it's not in the quest log"""
        if quest_id in self.active_quests.keys():
            return True
        else:
            return False

    def hasFinishedQuest(self, quest_id):
        """Check wether a quest is in the finished quests log
           @param quest_id: ID of the quest you want to check
           @return: True on when the quest is in the fisnished quests log
           @return: False when it's not in the finished quests log"""
        if quest_id in self.finished_quests.keys():
            return True
        else:
            return False

    def deleteQuest(self, quest_id):
        """Delete a quest
           @param quest_id: ID of the quest you want to delete
           @return: True on success
           @return: False when it failes"""
        if quest_id in self.active_quests.keys():
            del self.active_quests[quest_id]
            return True
        elif quest_id in self.finished_quests.keys():
            del self.finished_quests[quest_id]
            return True
        return False
