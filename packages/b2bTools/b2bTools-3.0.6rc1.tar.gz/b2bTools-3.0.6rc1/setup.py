#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os
import sys

parent_path = os.path.relpath(".")
path_to_file = os.path.join(parent_path, "README.md")

with open(path_to_file, "r") as f:
    long_description = f.read()

setuptools.setup(
    name="b2bTools",
    version="3.0.6-rc1",
    author="Wim Vranken",
    author_email="Wim.Vranken@vub.be",
    description="bio2Byte software suite to predict protein biophysical properties from their amino-acid sequences",
    license="OSI Approved :: GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Jose Gavalda-Garcia, Adrian Diaz, Wim Vranken",
    maintainer_email="jose.gavalda.garcia@vub.be, adrian.diaz@vub.be, wim.vranken@vub.be",
    url="https://bio2byte.be",
    project_urls={
        # "Bug Tracker": "https://bitbucket.org/bio2byte/b2btools/issues",
        "Documentation": "https://bio2byte.be/b2btools/package-documentation",
        # "Source": "https://bitbucket.org/bio2byte/b2btools/",
        "HTML interface" : "https://bio2byte.be/b2btools"
    },
    packages=setuptools.find_packages(exclude=("**/test/**",)),
    include_package_data=True,
    keywords="b2bTools,biology,bioinformatics,bio-informatics,fasta,proteins,protein-folding",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable"
    ],
    python_requires=">=3.7, <3.10",
    install_requires=[
        "biopython==1.81",
        "certifi==2023.5.7",
        "charset-normalizer==3.1.0",
        "cycler==0.11.0",
        "exceptiongroup==1.1.1",
        "fonttools==4.38.0",
        "idna==3.4",
        "importlib-metadata==6.7.0",
        "iniconfig==2.0.0",
        "joblib==1.2.0",
        "kiwisolver==1.4.4",
        "matplotlib==3.5.3",
        "networkx==2.6.3",
        'numpy>=1.22' if sys.version_info >= (3, 9) else 'numpy>=1.21',
        "packaging==23.1",
        "pandas==1.1.5",
        "Pillow==9.5.0",
        "pluggy==1.2.0",
        "pomegranate==0.14.8",
        "pyparsing==3.1.0",
        "python-dateutil==2.8.2",
        "pytz==2023.3",
        "PyYAML==6.0",
        "requests==2.31.0",
        "scikit-learn==1.0.1",
        "scipy==1.7.3",
        "six==1.16.0",
        "threadpoolctl==3.1.0",
        "tomli==2.0.1",
        "torch==1.13.1",
        "torchvision==0.14.1",
        "tqdm==4.65.0",
        "typing_extensions==4.6.3",
        "urllib3==1.26.6",
        "zipp==3.15.0",
    ]
)
