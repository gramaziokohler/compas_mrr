# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import os
import sys
from pathlib import Path
from shutil import rmtree

from invoke import task
from invoke.exceptions import UnexpectedExit

try:
    input = raw_input  # type: ignore [name-defined] # noqa: F821
    # flake8 reports F821 for prev line for parts of comment??
except NameError:
    pass

BASE_FOLDER = Path(__file__).parent

OUT_DIR = BASE_FOLDER / "dist"
DOCS_OUT_DIR = OUT_DIR / "docs"


class Log(object):
    def __init__(self, out=sys.stdout, err=sys.stderr):
        self.out = out
        self.err = err

    def flush(self):
        self.out.flush()
        self.err.flush()

    def write(self, message):
        self.flush()
        self.out.write(message + "\n")
        self.out.flush()

    def info(self, message):
        self.write("[INFO] %s" % message)

    def warn(self, message):
        self.write("[WARN] %s" % message)


log = Log()


@task(default=True)
def help(ctx):
    """List available tasks and usage."""
    ctx.run("invoke --list")
    log.write('Use "invoke -h <taskname>" to get detailed help for a task.')


@task(
    help={
        "docs": "True to clean up generated documentation, otherwise False",
        "bytecode": "True to clean up compiled python files, otherwise False.",
        "builds": "True to clean up build/packaging artifacts, otherwise False.",
    }
)
def clean(ctx, docs=True, bytecode=True, builds=True):
    """Clean the local copy from compiled artifacts."""
    with chdir(BASE_FOLDER):
        if builds:
            ctx.run("python setup.py clean")

        if bytecode:
            for root, dirs, files in os.walk(BASE_FOLDER):
                for f in files:
                    if f.endswith(".pyc"):
                        os.remove(os.path.join(root, f))
                if ".git" in dirs:
                    dirs.remove(".git")

        folders = []

        if docs:
            folders.append(BASE_FOLDER / "docs/reference")

        folders.append(OUT_DIR)

        if bytecode:
            for t in ("src", "tests"):
                folders += BASE_FOLDER.joinpath(t).glob("**/__pycache__")

        if builds:
            folders.append(BASE_FOLDER / "src/rapid_clay_formations_fab.egg-info/")

        for folder in folders:
            rmtree(folder, ignore_errors=True)


@task(
    help={
        "rebuild": "True to clean all previously built docs before starting.",
        "doctest": "True to run doctests.",
        "check_links": "True to check all web links in docs for validity.",
    }
)
def docs(ctx, doctest=False, rebuild=True, check_links=False):
    """Build package's HTML documentation."""
    if rebuild:
        clean(ctx)

    with chdir(BASE_FOLDER):
        if doctest:
            ctx.run("sphinx-build -b doctest docs build/docs")

        ctx.run(
            "sphinx-apidoc --separate --module-first --no-toc --force --no-headings "
            + "-o docs/reference src/compas_mobile_robot_reloc"
        )
        ctx.run(f"sphinx-build -b html docs {DOCS_OUT_DIR}")

        if check_links:
            ctx.run(f"sphinx-build -b linkcheck docs {DOCS_OUT_DIR}")


@task()
def check(ctx):
    """Check the consistency of documentation, coding style and a few other things."""
    with chdir(BASE_FOLDER):
        log.write("Pep517 check")
        ctx.run("python -m pep517.check .")

        log.write("Running all pre-commit hooks on whole repository.")
        ctx.run("pre-commit run --all-files")


@task(
    help={
        "checks": "True to run all checks before testing, otherwise False.",
        "coverage": "True to generate coverage report using pytest-cov",
        "doctest": "Run doctests as well.",
        "verbose": "Run pytest with -vv level verbosity.",
    }
)
def test(ctx, checks=False, doctest=False, coverage=False, verbose=True):
    """Run all tests."""
    if checks:
        check(ctx)

    with chdir(BASE_FOLDER):
        cmd = ["pytest"]
        if doctest:
            cmd.append("--doctest-modules")
        if verbose:
            cmd.append("-vv")
        if coverage:
            cmd.append("--cov src/compas_mobile_robot_reloc --cov-report xml:cov.xml")

        ctx.run(" ".join(cmd))


@task
def prepare_changelog(ctx):
    """Prepare changelog for next release."""
    UNRELEASED_CHANGELOG_TEMPLATE = (
        "## Unreleased\n\n### Added\n\n### Changed\n\n### Removed\n\n\n## "
    )

    with chdir(BASE_FOLDER):
        # Preparing changelog for next release
        with open("CHANGELOG.md", "r+") as changelog:
            content = changelog.read()
            changelog.seek(0)
            changelog.write(content.replace("## ", UNRELEASED_CHANGELOG_TEMPLATE, 1))

        ctx.run(
            'git add CHANGELOG.md && git commit -m "Prepare changelog for next release"'
        )


@task
def build(ctx):
    """Build project."""
    ctx.run("python -m pep517.build .")


@task
def raise_if_dirty(ctx):
    """Raise if there's modified or untracked files in repository."""
    try:
        ctx.run('test -z "$(git status --porcelain)"')
    except UnexpectedExit:
        raise Exception("Working directory contains changes or untracked files.")


@task(
    pre=[raise_if_dirty, check, test, build, docs],
    help={"new_version": "Version number to release"},
)
def release(ctx, new_version):
    """Releases the project in one swift command."""
    # Bump version and git tag it
    ctx.run("git -s tag {}".format(new_version))

    prepare_changelog(ctx)


@contextlib.contextmanager
def chdir(dirname=None):
    current_dir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(current_dir)
