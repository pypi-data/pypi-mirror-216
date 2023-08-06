import sys
from os import path
import time
from setuptools import find_packages, setup


install_requires = ['GitPython']

setup(name='funbuild',
      version=time.strftime("%Y%m%d%H%M", time.localtime()),
      description='funbuild',
      author='bingtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',
      packages=find_packages(),
      package_data={"": ["*.js", "*.*"]},
      entry_points={'console_scripts': [
          'funbuild = funbuild.core:funbuild', ]},
      install_requires=install_requires,
      )
