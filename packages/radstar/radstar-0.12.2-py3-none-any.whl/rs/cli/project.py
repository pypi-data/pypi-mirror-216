# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from itertools import chain
import os
import shutil

import click
import jinja2
import yaml

from . import cli
from .. import init_radstar, list_apps

# -------------------------------------------------------------------------------------------------------------------- #

@cli.group('project')
def project_cli():
    ''' Project management. '''

# -------------------------------------------------------------------------------------------------------------------- #

@project_cli.command()
@click.argument('image_prefix', nargs=1, required=False)
def configure(image_prefix=None):
    ''' (Re)configure project. '''

    with open('/rs/project/project.yml') as f:
        project_data = yaml.safe_load(f)

    init_radstar(no_init=True)

    # apt packages
    project_data['apt_pkgs'] = chain_attrs('apt.packages')
    project_data['apt_build_pkgs'] = chain_attrs('apt.build_packages')
    project_data['apt_dev_pkgs'] = chain_attrs('apt.dev_packages')

    # apt repos
    project_data['apt_repos'] = chain_attrs('apt.repos')
    project_data['apt_build_repos'] = chain_attrs('apt.build_repos')
    project_data['apt_dev_repos'] = chain_attrs('apt.dev_repos')

    # docker
    for x in ['build', 'build_setup', 'dev_setup', 'setup']:
        project_data[f'docker_{x}'] = '\n'.join(cmds for app in list_apps() if (cmds := app.get_attr(f'docker.{x}')))

    copy_with_templates('templates/root', '/rs/project', project_data)
    copy_with_templates('templates/devcontainer', '/rs/project/.devcontainer', project_data)
    copy_with_templates('templates/vscode', '/rs/project/.vscode', project_data)

# -------------------------------------------------------------------------------------------------------------------- #

def copy_with_templates(src: str, dst: str, project_data: dict):

    for src_root, dirs, files in os.walk(src):

        dst_root = os.path.join(dst, src_root[len(src)+1:])
        if not os.path.isdir(dst_root):
            os.mkdir(dst_root)

        for x in dirs:
            if x[0] == '.':
                continue
            x = os.path.join(dst_root, x)

            if not os.path.isdir(x):
                os.mkdir(x)

        for x in files:
            if x[0] == '.':
                continue

            src_file = os.path.join(src_root, x)
            if x.startswith('dot-'):
                x = x.replace('dot-', '.', 1)
            dst_file = os.path.join(dst_root, x)

            if x.endswith('.j2'):
                with open(src_file) as f:
                    data = jinja2.Template(f.read()).render(**project_data)
                with open(dst_file[:-3], 'w') as f:
                    print(data, file=f)
            else:
                shutil.copy(src_file, dst_file)

# -------------------------------------------------------------------------------------------------------------------- #

def chain_attrs(key: str) -> list:
    return list(chain.from_iterable(x for app in list_apps() if (x := app.get_attr(key))))

# -------------------------------------------------------------------------------------------------------------------- #
