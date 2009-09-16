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

import shutil

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class Setting(object):
    def setDefaults(self):
        shutil.copyfile('settings-dist.xml', 'settings.xml')
        self.isSetToDefault = True
        self.changesRequireRestart = True

    def readSetting(self, name, type='int', strip=True, text=False, default=None):
        if not hasattr(self, 'tree'):
            self.tree = ET.parse('settings.xml')
            self.root_element = self.tree.getroot()
        element = self.root_element.find(name)
        if element is not None:
            element_value = element.text
            if element_value is None:
                if type == 'int':
                    return 0
                elif type == 'list':
                    list = []
                    return list
            else:
                if type == 'int':
                    return element_value.strip() if strip else element_value
                elif type == 'list':
                    list = []
                    list_s = []
                    list = str(element_value.strip()).split(";")
                    for item in list:
                        item = item.strip()
                        if text:
                            item = item.replace('\\n', '\n')
                        list_s.append(item)
                    return list_s
                elif type == 'bool':
                    return False if element_value.strip() == 'False' else True
        else:
            print 'Setting,', name, 'does not exist!'

        return default

    def setSetting(self, name, value):
        element = self.root_element.find(name)
        if element is not None:
            if value is not element.text:
                element.text = str(value)
        else:
            print 'Setting,', name, 'does not exist!'

