Cookbook
================

Sphinx-linkcode resolver
-------------------------

The following code can be added to a Sphinx `conf.py` file to add links to the source code of a project 
in a github repository. This snippet also accounts for ReadTheDocs builds and will use the current branch name,
if available, as the release version.

.. code-block::

    extensions.append('sphinx.ext.linkcode')
    import os
    import subprocess
    from importlib.util import find_spec
    from pathlib import Path

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

    base_url = "https://github.com/..."  # The base url of the repository
    root_dir = find_spec(project).submodule_search_locations[0]

    def linkcode_resolve(domain, info):
        if domain != "py":
            return None
        try:
            package_file = find_spec(f"{project}.{info['module']}").origin
            blob = project / Path(package_file).relative_to(root_dir)
            walk = NodeWalk.from_file(package_file)
            try:
                decl = walk.get_last(info["fullname"])
            except KeyError:
                return None
        except Exception as e:
            print(f"error getting link code {info}")
            print_exc()
            raise
        return f"{base_url}/blob/{release}/{blob}#L{decl.lineno}-L{decl.end_lineno}"