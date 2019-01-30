# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

def setup(ctx):
    ctx.func.pip_install(ctx, 'bpython')

def run(ctx):
    ctx.func.run('{} {}/bpython {}'.format(ctx.vars.python, ctx.vars.bin_path, " ".join(ctx.vars.vargs)))
