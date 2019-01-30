# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

def setup(ctx):
    ctx.func.pip_install(ctx, 'certifi')
    ctx.func.pip_install(ctx, 'urllib3')
    ctx.func.pip_install(ctx, 'dulwich', '--no-deps --global-option --pure') # Pure python implementation

def run(ctx):
    ctx.func.run('{} {}/dulwich {}'.format(ctx.vars.python, ctx.vars.bin_path, " ".join(ctx.vars.vargs)))
