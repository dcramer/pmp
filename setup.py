from setuptools import setup, find_packages

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
for m in ('multiprocessing', 'billiard'):
    try:
        __import__(m)
    except ImportError:
        pass

tests_require = [
]


install_requires = [
    'pip',
]

setup(
    name='pmp',
    version='0.1.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    # url='http://www.getsentry.com',
    # description='A realtime logging and aggregation server.',
    long_description=__doc__,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    license='Apache License 2.0',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pmp = pmp.main:main',
        ],
    },
)
