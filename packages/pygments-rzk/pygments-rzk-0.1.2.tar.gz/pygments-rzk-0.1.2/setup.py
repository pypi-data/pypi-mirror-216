#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='pygments-rzk',
    version='0.1.2',
    description='Pygments lexer for Rzk language (of proof assistant for synthetic ∞-categories).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='pygments rzk lexer',
    license='BSD 3',

    author='Nikolai Kudasov',
    author_email='nickolay.kudasov@gmail.com',

    url='https://github.com/fizruk/pygments-rzk',

    packages=find_packages(),
    install_requires=['pygments >= 1.4'],

    entry_points='''[pygments.lexers]
                    rzklexer=pygments_rzk:RzkLexer''',

    classifiers=[
        'Environment :: Plugins',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
