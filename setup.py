#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
from os import path

import setuptools

here = path.abspath(path.dirname(__file__))


def _read(*names, **kwargs):
    return io.open(
        path.join(here, *names), encoding=kwargs.get("encoding", "utf8")
    ).read()


pkg_name = "compas_mobile_robot_reloc"

long_description = _read("README.md")

requirements = [
    "compas >= 0.19.3, <1.0",
]

extras_require = {
    "dev": [
        "black >= 20.8b1",
        "doc8",
        "flake8",
        "invoke >= 1.4.1",
        "isort >= 5.6.4",
        "mypy >= 0.790",
        "pydocstyle",
        "pytest >= 3.2",
        "recommonmark >=0.6",
        "Rhino-Stubs",
        "sphinx >=1.6",
        "sphinx_compas_theme >= 0.4",
        "setuptools_scm[toml] >= 4.1.2",
    ]
}

docs_url = "https://gramaziokohler.github.io/{}".format(pkg_name)
repo_url = "https://github.com/gramaziokohler/{}".format(pkg_name)

setuptools.setup(
    name=pkg_name,
    description="Robot localization using external measuring device (total station).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=docs_url,
    author="Gramazio Kohler Research",
    maintainer="Anton Tetov",
    maintainer_email="anton@tetov.se",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: IronPython",
    ],
    keywords=["architecture", "engineering", "fabrication", "construction"],
    project_urls={
        "Repository": repo_url,
        "Issues": repo_url + "/issues",
        "Documentation": docs_url,
    },
    packages=[pkg_name],
    package_data={pkg_name: ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.8",  # usage in IronPython is supported, see note in README
)
