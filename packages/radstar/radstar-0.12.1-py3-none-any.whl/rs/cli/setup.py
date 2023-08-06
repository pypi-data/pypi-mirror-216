# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import os
import subprocess

from . import cli
from .. import panic, shsplit

# -------------------------------------------------------------------------------------------------------------------- #

RS_RADSTAR_LINKS = ['core', 'jetapp', 'rs', 'scripts', 'templates']

# -------------------------------------------------------------------------------------------------------------------- #

@cli.command()
def setup():
    ''' Configure radstar environment. '''

    # check that we're executing in a radstar environment
    for dir_name in ['/rs', '/rs/env', '/rs/project', '/node_modules']:
        if not os.path.isdir(dir_name):
            panic(f'invalid environment ({dir_name} missing)')

    # create /rs/radstar
    if not os.path.exists('/rs/radstar'):
        os.mkdir('/rs/radstar')
        for x in RS_RADSTAR_LINKS:
            os.symlink(os.path.join(os.getcwd(), x), os.path.join('/rs/radstar', x))

    # create jetapp/node_modules link
    if not os.path.exists('jetapp/node_modules'):
        os.symlink('/node_modules', 'jetapp/node_modules')

    # install jetapp js dependencies
    subprocess.check_call(shsplit('yarn install'), cwd='jetapp')

# -------------------------------------------------------------------------------------------------------------------- #
