#!/usr/bin/env python

# ###################################################
# Copyright (C) 2009 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

import os
import sys

if __name__ == '__main__':
	os.chdir( os.path.split( os.path.realpath( sys.argv[0]) )[0] )
        print os.path.realpath(sys.argv[0])

	os.chdir('../editor')
        print os.getcwd()
	#start editor
	args = [sys.executable, './run.py', ]
        env = os.environ.copy()
        env['PYTHONPATH'] = "../parpg/editor"

        os.execve(args[0], args, env)
        #os.execvp(args[0], args)
