# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

CREDENTIALS_FILENAME = 'awscreds.json'

def get_awscreds(ctx):
    if not os.path.isfile('{}/cognito-auth'.format(ctx.vars.bin_path)):
        ctx.func.pip_install(ctx, 'cognito-auth')
    credentials_file = os.path.join(ctx.vars.local_path, CREDENTIALS_FILENAME)
    ctx.func.run('{}/cognito-auth --login --json-output --to-file {}'.format(ctx.vars.bin_path, credentials_file))

def setup(ctx):
    ctx.func.pip_install(ctx, 'cognito_auth')
    ctx.func.get_awscreds = get_awscreds

def run(ctx):
    ctx.func.run('{}/cognito-auth {}'.format(ctx.vars.bin_path, " ".join(ctx.vars.vargs)))
