# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

def setup(ctx):
    ctx.func.pip_install(ctx, 'boto3')
    awscreds_path = '{}/{}'.format(ctx.vars.local_path, AWSCREDS_DIR)
    if AWSCREDS_DIR_ENVVAR in os.environ: # devo
        os.symlink(AWSCREDS_DIR_ENVVAR, awscreds_path)
    else:
        ctx.func.pkg_install(ctx, 'git')
        ctx.func.github_get(ctx, AWSCREDS_GITHUB_REPO, awscreds_path)

def run(ctx):
    awscreds_path = '{}/{}'.format(ctx.vars.local_path, AWSCREDS_DIR)
    ctx.func.run('{}/awscreds -f {}'.format(ctx.vars.bin_path, awscreds_path))
    ctx.func.run('{}/ghi {}'.format(ctx.vars.bin_path, " ".join(ctx.vars.vargs)))
