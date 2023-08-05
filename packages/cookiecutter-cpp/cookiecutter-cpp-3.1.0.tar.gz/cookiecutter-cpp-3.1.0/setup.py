# !/usr/bin/env python

from setuptools import setup
from pathlib import Path
this_folder = Path(__file__).parent

setup(
    name='cookiecutter-cpp',
    packages=[],
    version='3.1.0',
    description='Cookiecutter template for C++ with several libs ready to be used.',
    long_description=(this_folder / 'README.rst').read_text(),
    long_description_content_type='text/x-rst',
    author='Riccardo Petraglia (forked from https://github.com/audreyr/cookiecutter-pypackage)',
    license='BSD',
    author_email='riccardo.petraglia@gmail.com',
    url='https://github.com/grhawk/cookiecutter-cpp.git',
    keywords=['cookiecutter', 'template', 'package', 'c++', 'cpp', 'gtest', 'spdlog'],
    python_requires='>=3.8',
    setup_requires=['wheel'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ]
)
