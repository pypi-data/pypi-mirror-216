"""
Asterisk Plus PBX Agent
"""
import re
from setuptools import setup
from setuptools.command.install import install
import os
from os.path import abspath, dirname, join


def get_version():
    try:
        version_file = open(
            os.path.join(
                os.path.dirname(__file__), 'asterisk_plus_agent.py')
        ).read()
        res = re.search("^__version__ = '(.+)'$", version_file, re.MULTILINE).groups(0)[0]
        return res
    except Exception:
        raise RuntimeError('Error parsing version string.')


def read_file(filename):
    '''Read the contents of a file located relative to setup.py'''
    with open(join(abspath(dirname(__file__)), filename)) as thefile:
        return thefile.read()


setup(
    author='Odooist',
    author_email='odooist@gmail.com',
    license='Odoo Enterprise Edition License v1.0',
    name='asterisk-plus-agent-test',
    version=get_version(),
    description=__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    url='https://odoopbx.com',
    install_requires=[
       'click',
       'httpx',
       'panoramisk',
       'aiorun',
       'aioboto3',
       'aio_odoorpc'
    ],
    py_modules=['asterisk_plus_agent'],
    entry_points='''
[console_scripts]
asterisk-plus-agent-test=asterisk_plus_agent:main
    ''',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)
