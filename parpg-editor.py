#!/usr/bin/python

#   This file is part of PARPG.
#   PARPG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   PARPG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

"""This program is a hack to be able to hook into the FIFE map editor load and
save functionality. It runs the FIFE editor such that our custom loaders and savers are
used instead of the stock FIFE ones. Ideally the FIFE editor could be extended
to support custom loaders and savers in a way that's not trying to trick the
process into running our code. :)"""
if __name__ == '__main__':
	os.chdir( os.path.split( os.path.realpath( sys.argv[0]) )[0] )

	os.chdir('../editor')
	args = [sys.executable, './run.py', '../parpg/maps/map.xml']
        env = os.environ.copy()
        env['PYTHONPATH'] = "../parpg/editor:../parpg/local_loaders"

        os.execve(args[0], args, env)
