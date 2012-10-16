A simplified package manager.

::

    pkg [command] [options]

    pkg install  # pip install .
    pkg install <name>  # pip install <name>
    pkg install <github url|bitbucket url|googlecode url>  # pip install <repo>
    pkg develop  # pip install -e .

::

    pkg test [options] # install test dependencies and run setup.py [test|nosetests]

::

    # publish will register the package if its not already present on pypi
    pkg publish  # python setup.py sdist upload
    pkg publish disqus  # python setup.py sdist upload -r disqus
    pkg register
    pkg register disqus
