#!/usr/bin/env python

from setuptools import setup

setup(
    name='virtualenvwrapper.configvar',
    version='0.0.3',
    description='Plugin for virtualenvwrapper to automatically '
                'export config vars found in your project level '
                '.env file.',
    author='Sean Brant',
    author_email='brant.sean@gmail.com',
    url='https://github.com/seanbrant/virtualenvwrapper.configvar',
    namespace_packages=['virtualenvwrapper'],
    packages=['virtualenvwrapper'],
    install_requires=[
        'virtualenv',
        'virtualenvwrapper>=2.11',
    ],
    entry_points={
        'virtualenvwrapper.pre_activate': [
            'configvars = virtualenvwrapper.configvars:pre_activate',
        ],
        'virtualenvwrapper.pre_activate_source': [
            'configvars = virtualenvwrapper.configvars:pre_activate_source',
        ],
        'virtualenvwrapper.post_deactivate': [
            'configvars = virtualenvwrapper.configvars:post_deactivate',
        ],
        'virtualenvwrapper.post_deactivate_source': [
            'configvars = virtualenvwrapper.configvars:post_deactivate_source',
        ],
    }
)
