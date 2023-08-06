from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'A python library for ensuring the safety and security of ML models'
LONG_DESCRIPTION = 'A python library for ensuring the safety and security of ML models and their outputs for the Arabic and Islamic community'

# Setting up
setup(
    name="zein",
    version=VERSION,
    author="Mohamed Elsayed",
    author_email="<mohamedelsayed3487@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data= {
      'zein': ['data/*.csv'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=['pandas'],
    keywords=['python','arabic filtering', 'text filtering', 'profanity check'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
