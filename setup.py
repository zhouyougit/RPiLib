import os
import sys

from setuptools import find_packages, setup

setup(
    name = 'RPiLib',
    version = '0.0.1',
    description = 'Raspberry Pi lib',
    keywords = 'Raspberry Pi lib',
    url = 'https://github.com/zhouyougit/RPiLib',
    author = 'zhouyou',
    author_email = 'zhouyoug@gmail.com',
    packages = find_packages(exclude = ['*.pyc'])
)
