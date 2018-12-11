
def setup(ctx):
    ctx.func.pkg_install(ctx, 'rubyenv')
    ctx.func.gem_install(ctx, 'ghi')

def run(ctx):
    ctx.func.run('{}/ghi {}'.format(ctx.vars.bin_path, " ".join(ctx.vars.vargs)))
