import pathlib

import invoke
from setuptools_scm import version_from_scm

from .utils import check_tools


def build(ctx, scm_root):
    if not version_from_scm(scm_root).exact:
        raise RuntimeError('dirty versions is not for release')
    ctx.run('python -m build --wheel', pty=True)
    packages = list(pathlib.Path('dist').glob('*'))
    if len(packages) != 1:
        raise RuntimeError('please cleanup (especially dist) before release')
    return packages


@invoke.task(aliases=['release'])
@check_tools('devpi', 'true')
def devpi_release(ctx, scm_root='.'):
    ctx.run(f'devpi upload {build(ctx, scm_root)[0]}', pty=True)


@invoke.task(aliases=['release'])
@check_tools('twine')
def pypi_release(ctx, scm_root='.'):
    ctx.run(f'twine upload {build(ctx, scm_root)[0]}', pty=True)
