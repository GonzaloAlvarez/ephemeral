# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

RUBY_VERSION="2.4.1"

def gem_install(ctx, gem_name):
    if not os.path.isfile('{}/gem'.format(ctx.vars.bin_path)):
        ctx.func.puts('Installing rubyenv version {}'.format(RUBY_VERSION))
        ctx.func.run('{} {}/rubyenv install {}'.format(ctx.vars.python, ctx.vars.bin_path, RUBY_VERSION))
    installed_gem, installed_gem_err, installed_gem_res = ctx.func.run_background('{}/gem list {} -i'.format(ctx.vars.bin_path, gem_name))
    if "false" in installed_gem.decode("utf-8"):
        ctx.func.puts('Installing [{}] gem'.format(gem_name))
        ctx.func.run('{}/gem install {}'.format(ctx.vars.bin_path, gem_name))

def setup(ctx):
    ctx.func.pip_install(ctx, 'six')
    ctx.func.pip_install(ctx, 'future')
    ctx.func.pip_install(ctx, 'rubyenv')
    ctx.func.gem_install = gem_install

def run(ctx):
    ctx.func.puts('Installing rubyenv version {}'.format(RUBY_VERSION))
    ctx.func.run_background('{} {}/rubyenv install {}'.format(ctx.vars.python, ctx.vars.bin_path, RUBY_VERSION))
