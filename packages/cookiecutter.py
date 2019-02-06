# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

COOKIECUTTER_CONFIG='''\
default_context:
    cookiecutters_dir: "{}"
    replay_dir: "{}"
'''

CONFIG_DIRNAME="cookiecutter"
CONFIG_FILENAME="cookiecutter.yml"

def setup(ctx):
    cookiec_folder = os.path.join(ctx.vars.local_path, CONFIG_DIRNAME)
    if not os.path.isdir(cookiec_folder):
        os.mkdir(cookiec_folder)
    cookiec_config = os.path.join(cookiec_folder, CONFIG_FILENAME)
    if not os.path.isfile(cookiec_config):
        with open(cookiec_config, "w") as conf_file:
            conf_file.write(COOKIECUTTER_CONFIG.format(cookiec_folder, cookiec_folder))

    ctx.func.pip_install(ctx, 'cookiecutter')

def run(ctx):
    cookiec_folder = os.path.join(ctx.vars.local_path, CONFIG_DIRNAME)
    cookiec_config = os.path.join(cookiec_folder, CONFIG_FILENAME)
    ctx.func.run('{} {}/cookiecutter --config-file {} {}'.format(ctx.vars.python, ctx.vars.bin_path, cookiec_config, " ".join(ctx.vars.vargs)), _env={'LC_ALL':'en_US.UTF-8','LANG':'en_US.UTF-8'})
