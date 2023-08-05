# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'e-models',
    version      = '1.4',
    description  = 'Tools for helping build of extraction models with scrapy spiders.',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    license      = 'BSD',
    author       = 'Martin Olveyra',
    author_email = 'molveyra@gmail.com',
    url          = 'https://github.com/kalessin/emodels',
    packages     = find_packages(),
    install_requires=(
        "scrapy",
    ),
    scripts = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    package_data={"emodels": ["py.typed"]}
)
