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

    def linkcode_resolve(domain, info):
        if domain != "py":
            return None
        try:
            fn = f"{project}/{info['module']}.py"
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