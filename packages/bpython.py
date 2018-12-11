
def setup(ctx):
    ctx.func.pip_install(ctx, 'bpython')

def run(ctx):
    ctx.func.run_sys('{} {}/bpython {}'.format(ctx.vars.python, ctx.vars.bin_path, " ".join(ctx.vars.vargs)))
