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

"""
This program is a hack. To be able to hook into the FIFE map editor load and
save functionality we have to change the import path. It runs the FIFE
editor such that our custom loaders and savers are used instead of the stock
FIFE ones. Ideally the FIFE editor could be extended to support custom loaders
and savers so we don't have to resort to tricking the editor. :)
"""

if __name__ == '__main__':
    # Either FIFE or the editor do not like being passed an absolute
    # path. Maybe a bug? We have to force paths relative to the parpg
    # directory. This also assumes that the parpg directory is at the same
    # level as the FIFE editor. :P
    parpg_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    parpg_dir = parpg_path.split('/')[-1]

    args = [sys.executable, './run.py']

    if len(sys.argv) > 1:
        map_path = sys.argv[1]

        args.append(os.path.join('..', parpg_dir, map_path))
        print args

    fife_editor_path = os.path.join(parpg_path, '..', 'editor')
    os.chdir(fife_editor_path)
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([
        os.path.join('..', parpg_path, 'editor'),
        os.path.join('..', parpg_path, 'local_loaders')
    ])

    os.execve(args[0], args, env)
