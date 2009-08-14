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

from PyQt4 import QtCore, QtGui

class SyntaxHighlighter(QtGui.QSyntaxHighlighter):
    """
    A class to highlight the syntax keywords
    """

    def highlightBlock(self, text):
        """
        Highlight the syntax in the text of self.widget
        @type text: QtCore.QString
        @param text: the text to highlight syntax in
        @return: None
        """
        cmdFormat = QtGui.QTextCharFormat()
        cmdFormat.setFontWeight(QtGui.QFont.Bold)
        cmdFormat.setForeground(QtGui.QColor("blue"))
        
        quoteFormat = QtGui.QTextCharFormat()
        quoteFormat.setForeground(QtGui.QColor("green"))

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtGui.QColor("red"))

        multiLineCommentFormat = QtGui.QTextCharFormat()
        multiLineCommentFormat.setForeground(QtGui.QColor("magenta"))
            
        cmds = ["npc", "NPC", "pc", "PC", "section", "SECTION", "SCRIPTNAME",
                "scriptname", "endsection", "ENDSECTION", "callsection", 
                "CALLSECTION", "option", "OPTION", "endoption", "ENDOPTION", 
                "playsound", "PLAYSOUND", "say", "SAY", "attack", "ATTACK", 
                "return", "RETURN","IF", "if", "ELIF", "elif", "ELSE", "else",
                "#", "/\*", "\""]

        for cmd in cmds:
            # if its a quote
            if (cmd == "\""):
                startExp = QtCore.QRegExp(cmd)
                startIndex = text.indexOf(startExp)
                if (self.format(startIndex) == singleLineCommentFormat or
                    self.format(startIndex) == multiLineCommentFormat):
                    return
                else:
                    endIndex = text.indexOf(startExp, startIndex+1)
                    quoteLength = endIndex - startIndex + 1
                    self.setFormat(startIndex, quoteLength, quoteFormat)
                
            # if its a singeline comment
            elif (cmd == "#"):
                startExp = QtCore.QRegExp(cmd)
                startIndex = text.indexOf(startExp)
                self.setFormat(startIndex, text.length(), singleLineCommentFormat)                

            # if its a multiline comment
            elif (cmd == "/\*"):
                startExp = QtCore.QRegExp(cmd)
                endExp = QtCore.QRegExp("\*/")
                self.setCurrentBlockState(0)
                
                startIndex = 0
                if (self.previousBlockState() != 1):
                    startIndex = text.indexOf(startExp)

                while (startIndex >= 0):
                    endIndex = text.indexOf(endExp, startIndex)
                    if (endIndex == -1):
                        self.setCurrentBlockState(1)
                        commentLength = text.length() - startIndex
                    else:
                        commentLength = endIndex - startIndex + endExp.matchedLength()

                    self.setFormat(startIndex, commentLength, multiLineCommentFormat)
                    startIndex = text.indexOf(startExp, startIndex + commentLength)

            # otherwise its just a command
            else:       
                expression = QtCore.QRegExp(cmd)
                index = int(text.indexOf(expression))
                while (index >= 0):
                    length = int(expression.matchedLength())
                    self.setFormat(index, length, cmdFormat)
                    index = text.indexOf(expression, index + length)
