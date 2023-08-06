import sys

import nox

nox.options.sessions = [
    'tests_wagtail41',
    'tests_wagtail50',
]

dj32 = nox.param('3.2', id='dj32')
dj42 = nox.param('4.2', id='dj42')


def install_and_run_tests(session):
    session.install('-r', 'requirements-test.txt')
    session.install('-e', '.[components]')
    tests = session.posargs or ['tests/']
    session.run(
        'pytest',
        '--cov',
        '--cov-config=pyproject.toml',
        '--cov-report=',
        *tests,
        env={'COVERAGE_FILE': f'.coverage.{session.name}'},
    )
    session.notify('coverage')


@nox.session
@nox.parametrize('django', [dj32])
def tests_wagtail41(session, django):
    if sys.version_info.minor >= 11:
        session.skip("Django 3.2 does not support Python 3.11+")
    session.install(f'django=={django}')
    session.install('wagtail~=4.1.6')
    install_and_run_tests(session)


@nox.session
@nox.parametrize('django', [dj32, dj42])
def tests_wagtail50(session, django):
    if django == '3.2' and sys.version_info.minor >= 11:
        session.skip("Django 3.2 does not support Python 3.11+")
    session.install(f'django=={django}')
    session.install('wagtail~=5.0.1')
    install_and_run_tests(session)


@nox.session
def coverage(session):
    session.install('coverage[toml]')
    session.run('coverage', 'combine')
    session.run('coverage', 'report', '--show-missing')
    session.run('coverage', 'xml')
    session.run('coverage', 'erase')


@nox.session
def lint(session):
    session.install('pre-commit')
    session.run(
        'pre-commit',
        'run',
        '--all-files',
        '--show-diff-on-failure',
        '--hook-stage=manual',
        *session.posargs,
    )
