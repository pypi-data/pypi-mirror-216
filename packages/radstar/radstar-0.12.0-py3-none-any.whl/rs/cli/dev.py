# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import os

from . import cli
from .. import panic

# -------------------------------------------------------------------------------------------------------------------- #

@cli.command()
def dev():
    ''' Setup dev mode. '''

    if not os.path.exists('/rs/project/radstar'):
        panic('/rs/project/radstar missing')

    os.system('sudo rm /rs/radstar')
    os.system('sudo ln -s /rs/project/radstar /rs/radstar')

# -------------------------------------------------------------------------------------------------------------------- #
