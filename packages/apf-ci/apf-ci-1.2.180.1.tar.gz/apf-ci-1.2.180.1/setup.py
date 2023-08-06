"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

__author__ = 'LianGuoQing'

from setuptools import setup
from setuptools import find_packages
from codecs import open
from os import path

import apf_ci as ci

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install CIScript
    #
    # And where it will live on PyPI:
    # http://c.nuget.sdp.nd:8081/service/rest/repository/browse/pypi-release/CIScript/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name=ci.__title__,    # Required

    version=ci.__version__,    # Required
    description='App factory apf_ci build script',  # Required
    long_description=long_description,  # Optional

    # text/plain, text/x-rst, and text/markdown
    long_description_content_type='text/markdown',  # Optional (see note above)

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[('apf_ci-config',
                 ['data/config_dev.json', 'data/config_debug.json', 'data/config_beta.json', 'data/config.json']
                 )],
    license=ci.__license__,
    url=ci.__uri__,  # Optional

    author=ci.__author__,  # Optional
    author_email=ci.__email__,  # Optional

    classifiers=[  # Optional
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
  packages=find_packages(exclude=[ 'docs', 'tests*']),
    entry_points={  # Optional
        "apf_ci.commands": [
            "app-init = apf_ci.commands.app_init:main",
            "variable = apf_ci.commands.variable:main",
            "android-prepare = apf_ci.commands.android_prepare:main",
            "rn = apf_ci.commands.rn:main",
            "local-h5 = apf_ci.commands.local_h5:main",
            "h5-grain = apf_ci.commands.h5_grain:main",
            "rn-widget = apf_ci.commands.rn_widget:main",
            "android-build-prepare = apf_ci.commands.android_build_prepare:main",
            "subapp-config = apf_ci.commands.subapp_config:main",
            "h5-grain-config = apf_ci.commands.h5_grain_config:main",
            "h5-widget-resource = apf_ci.commands.h5_widget_resource:main",
            "react-widget-resource = apf_ci.commands.react_widget_resource:main",
            "dynamic-tab = apf_ci.commands.tab_build:main",
            "app-compare = apf_ci.commands.app_compare:main",
            "app-component-compare = apf_ci.commands.app_component_compare:main",
            "app-factory-flutter = apf_ci.commands.flutter:main"
        ],
        "console_scripts": [
            "%s = apf_ci.__main__:main" % ci.__title__,
        ]
    },
    # install_requires=["Pillow", "lxml", "inquirer"]
    install_requires=["jsonmerge","pyDes"]
)