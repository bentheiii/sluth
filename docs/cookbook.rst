Cookbook
================

Sphinx-linkcode resolver
-------------------------

The following code can be added to a Sphinx `conf.py` file to add links to the source code of a project 
in a github repository.

.. code-block::

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
            blob = f"{project}/{info['module']}.py"
            file = f"{root_dir}/{info['module']}.py"
            walk = NodeWalk.from_file(file)
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
        path = f"{blob}#L{walk.lineno}-L{walk.end_lineno}"
        return f"{base_url}/blob/{release}/{path}"