Deployment
==========

If you wish to create a new version manually, the process is:

1. Update version info in ``setup.py``

1. Install the requirements in requirements_dev.txt

1. Set up a config file at ~/.pypirc

1. Generate a universal distribution that worksin py2 and py3 (see setup.cfg)

    ::

        python setup.py sdist bdist_wheel

1. Upload the distributions

    ::

        twine upload dist/* -r pypi (or pypitest)


