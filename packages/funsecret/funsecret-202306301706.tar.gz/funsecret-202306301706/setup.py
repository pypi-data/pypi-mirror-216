import subprocess
import sys
from os import path

from setuptools import find_packages, setup

import time

install_requires = ['darkbuild', 'sqlalchemy']

setup(name='funsecret',
      version=time.strftime("%Y%m%d%H%M", time.localtime()),
      description='funsecret',
      author='bingtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',
      packages=find_packages(),
      install_requires=install_requires,
      )
