# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# If your documentation needs a minimal Sphinx version, state it here.
import sphinx_compas_theme

#
# needs_sphinx = "1.0"
from compas_mobile_robot_reloc import __version__

# -- General configuration ------------------------------------------------

project = "Total station robot localization"
copyright = "Gramazio Kohler Research"
author = "Anton T Johansson"
version = release = __version__

master_doc = "index"

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
templates_path = [
    "_templates",
]
exclude_patterns: list = []

pygments_style = "sphinx"
show_authors = True
add_module_names = True
language = None

# -- Extension configuration ------------------------------------------------

extensions = [
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "matplotlib.sphinxext.plot_directive",
]

# autodoc options
autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__",
    "exclude-members": "__weakref__",
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_mock_imports = ["Rhino"]
autodoc_member_order = "alphabetical"

autoclass_content = "class"


# autosummary options

autosummary_generate = True

# napoleon options

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False


# intersphinx options

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", "https://docs.python.org/3/objects.inv"),
    "compas": (
        "https://compas.dev/compas/latest",
        "https://compas.dev/compas/latest/objects.inv",
    ),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "compaspkg"
html_theme_path = sphinx_compas_theme.get_html_theme_path()

html_theme_options = {
    "package_name": "compas_mobile_robot_reloc",
    "package_title": project,
    "package_version": release,
    "package_repo": "https://github.com/gramaziokohler/compas_mobile_robot_reloc",  # noqa: E501
}

html_context: dict = {}
html_static_path: list = []
html_extra_path = [".nojekyll"]
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = True
html_add_permalinks = ""
html_experimental_html5_writer = True
html_compact_lists = True
