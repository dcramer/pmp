As pip installs packages, pmp manages projects.

It provides a simple extensible command interface designed to influence good behavior in project management using existing tools (and minor hacks/additions).

Optional Behaviors
------------------

* vendor packages vs using an external virtualenv (vendor/)
  * have bin/python deal with sites (as buildout does) so only items listed in lockfile (version specific) get bound
* manage package version via publish? (project/VERSION?)
* maintain a lockfile/requirements file (similar to requirements.txt, also used by the install commands)
  * this could happen via a second command, or via install

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

    # add to lockfile
    pmp require [name]

::

    # update any top-level dependencies which have a newer version within range
    # requires lockfile
    pmp update 

::

    # generates a new setup.py, etc. for you
    pmp it
