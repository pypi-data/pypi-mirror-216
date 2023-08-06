# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import os

from . import cli
from .. import panic
from .setup import RS_RADSTAR_LINKS

# -------------------------------------------------------------------------------------------------------------------- #

@cli.command()
def dev():
    ''' Setup dev mode. '''

    if not os.path.exists('/rs/project/radstar'):
        panic('/rs/project/radstar missing')

    if os.path.islink('/rs/radstar'):
        os.unlink('/rs/radstar')

    elif os.path.isdir('/rs/radstar'):
        for x in RS_RADSTAR_LINKS:
            x = os.path.join('/rs/radstar', x)
            if not os.path.islink(x):
                panic(f'expected symlink at {x}')
            os.unlink(x)
        os.rmdir('/rs/radstar')

    os.symlink('/rs/project/radstar', '/rs/radstar')

# -------------------------------------------------------------------------------------------------------------------- #
