
def setup(ctx):
    ctx.func.pip_install(ctx, 'certifi')
    ctx.func.pip_install(ctx, 'urllib3')
    ctx.func.pip_install(ctx, 'dulwich', '--no-deps --global-option --pure') # Pure python implementation

def run(ctx):
    ctx.func.run('{} {}/dulwich {}'.format(ctx.vars.python, ctx.vars.bin_path, " ".join(ctx.vars.vargs)))
