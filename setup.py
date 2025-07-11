#!/usr/bin/env python3
"""
Setup script for Context Builder
Makes context_builder directly executable via pip install
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='context-builder',
    version='1.0.0',
    description='Transform your codebase into AI-ready implementation guides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Context Builder Team',
    author_email='hello@contextbuilder.dev',
    url='https://github.com/yourusername/context-builder',
    py_modules=['context_builder'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'context_builder=context_builder:main',
            'ctx=context_builder:main',  # Short alias
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Markup :: Markdown',
    ],
    keywords='ai development documentation context builder implementation guide',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/context-builder/issues',
        'Source': 'https://github.com/yourusername/context-builder',
        'Documentation': 'https://github.com/yourusername/context-builder#readme',
    },
)
