# coding: utf-8

import fife, sys
import pychan
from pychan import widgets
from filebrowser import FileBrowser

def u2s(string):
	return string.encode(sys.getfilesystemencoding())

class PARPGFileBrowser(FileBrowser):
	"""
	A sub-class of filebrowser.FileBrowser
	"""
	def __init__(self, engine, fileSelected, savefile=False, selectdir=False, extensions=('xml',), guixmlpath="gui/filebrowser.xml"):
		FileBrowser.__init__(self, engine, fileSelected, False, False, extensions, guixmlpath)

	def _selectFile(self):
		self._widget.hide()
		selection = self._widget.collectData('fileList')
		if self.savefile:
			data = self._widget.collectData('saveField')

			try:
				data_split = data.split('.')[1]
			except:
				self._warningMessage()
				return
			
		if self.savefile:
			if (data_split == 'dat'):
				self.fileSelected(self.path, u2s(self._widget.collectData('saveField')))
				return
			else:
				self._warningMessage()
				return
		else:
			if selection >= 0 and selection < len(self.file_list):
				self.fileSelected(self.path, u2s(self.file_list[selection]))
				return
			
			elif self.selectdir:
				self.fileSelected(self.path)
				return

			else:
				print 'FileBrowser: error, no selection.'
