# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
from traceback import print_exc

# -- Project information -----------------------------------------------------

project = "sluth"
copyright = "2024, ben avrahami"
author = "ben avrahami"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.intersphinx", "sphinx.ext.autosectionlabel"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

python_use_unqualified_type_names = True
add_module_names = False
autosectionlabel_prefix_document = True

extensions.append('sphinx.ext.linkcode')
import os
import subprocess
from importlib.util import find_spec

from sluth import NodeWalk

release = "main"
if rtd_version := os.environ.get("READTHEDOCS_GIT_IDENTIFIER"):
    release = rtd_version
else:
    # try to get the current branch name
    try:
        release = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
    except Exception:
        pass

base_url = "https://github.com/bentheiii/sluth"  # The base url of the repository
root_dir = find_spec("sluth").submodule_search_locations[0]

def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    try:
        fn = f"{root_dir}/{info['module']}.py"
        walk = NodeWalk.from_file(fn)
        parts = info["fullname"].split(".")
        for part in parts:
            try:
                walk = walk[part]
            except KeyError:
                return None
    except Exception as e:
        print(f"error getting link code {info}")
        print_exc()
        raise
    path = f"{fn}#L{walk.lineno}-L{walk.end_lineno}"
    return f"{base_url}/blob/{release}/{path}"


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
