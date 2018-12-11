import os

RUBY_VERSION="2.4.1"

def gem_install(ctx, gem_name):
    if not os.path.isfile('{}/gem'.format(ctx.vars.bin_path)):
        ctx.func.puts('Installing rubyenv version {}'.format(RUBY_VERSION))
        ctx.func.run('{} {}/rubyenv install {}'.format(ctx.vars.python, ctx.vars.bin_path, RUBY_VERSION))
    installed_gem = ctx.func.run_silent('{}/gem list {} -i'.format(ctx.vars.bin_path, gem_name))
    if "false" in installed_gem:
        ctx.func.puts('Installing [{}] gem'.format(gem_name))
        ctx.func.run('{}/gem install {}'.format(ctx.vars.bin_path, gem_name))

def setup(ctx):
    ctx.func.pip_install(ctx, 'six')
    ctx.func.pip_install(ctx, 'future')
    ctx.func.pip_install(ctx, 'rubyenv')
    ctx.func.gem_install = gem_install

def run(ctx):
    ctx.func.puts('Installing rubyenv version {}'.format(RUBY_VERSION))
    ctx.func.run_silent('{} {}/rubyenv install {}'.format(ctx.vars.python, ctx.vars.bin_path, RUBY_VERSION))
