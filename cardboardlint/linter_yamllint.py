# -*- coding: utf-8 -*-
# Cardboardlint is a cheap lint solution for pull requests.
# Copyright (C) 2011-2017 The Cardboardlint Development Team
#
# This file is part of Cardboardlint.
#
# Cardboardlint is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Cardboardlint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Linter using yamllint.

This test calls the flake program, see https://yamllint.readthedocs.io/en/latest/
"""
from __future__ import print_function

from cardboardlint.common import Message, run_command, Linter


__all__ = ['linter_yamllint']


DEFAULT_CONFIG = {
    # Filename filter rules
    'filefilter': ['+ *.yml', '+ *.yaml'],
    # Optional path to the config file.
    'config': None
}


def run_yamllint(config, filenames):
    """Linter for checking yamllint results.

    Parameters
    ----------
    config : dict
        Dictionary that contains the configuration for the linter
    filenames : list
        A list of filenames to check

    Returns
    -------
    messages : list
        The list of messages generated by the external linter.

    """
    # get yamllint version
    command = ['yamllint', '--version']
    version_info = run_command(command, verbose=False)[0]
    print('USING              : {0}'.format(version_info))

    def has_failed(returncode, _stdout, _stderr):
        """Determine if yamllint ran correctly."""
        return not 0 <= returncode < 2

    messages = []
    if len(filenames) > 0:
        command = ['yamllint', '-f', 'parsable'] + filenames
        if config['config'] is not None:
            command += ['-c', config['config']]
        output = run_command(command, has_failed=has_failed)[0]
        if len(output) > 0:
            for line in output.splitlines():
                words = line.split(':')
                messages.append(Message(
                    words[0], int(words[1]), int(words[2]), words[3].strip()))
    return messages


# pylint: disable=invalid-name
linter_yamllint = Linter('yamllint', run_yamllint, DEFAULT_CONFIG, language='yaml')
