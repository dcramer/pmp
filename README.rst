As pip installs packages, pmp manages packages.

Optional Behaviors
------------------

* vendor packages vs using an external virtualenv (vendor/)
  * have bin/python deal with sites (as buildout does) so only items listed in lockfile (version specific) get bound
* manage package version via publish? (project/VERSION?)
* maintain a lockfile/requirements file (similar to requirements.txt, also used by the install commands)

CLI
---

::

    pmp [command] [options]

::

    pmp install  # pip install .
    pmp install <name>  # pip install <name>
    pmp install <github url|bitbucket url|googlecode url>  # pip install <repo>

::

    pmp develop  # pip install -e .

::

    pmp test [options] # install test dependencies and run setup.py [test|nosetests]

::

    # publish will register the package if its not already present on pypi
    pmp publish  # python setup.py sdist upload
    pmp publish disqus  # python setup.py sdist upload -r disqus

::

    pmp register
    pmp register disqus

::

    pmp add-pypi [name] [url]  # register remote pypi, attempt to fix bad urls you enter


Concepts
--------

::

    pmp require [name]  # add to lockfile
