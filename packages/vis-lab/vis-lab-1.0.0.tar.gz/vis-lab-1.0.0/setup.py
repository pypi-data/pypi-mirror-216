from setuptools import setup, find_packages
from os import path
# twine upload dist/*
# python setup.py bdist_wheel
# twine check dist/*
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9',
]
 
setup(
  name='vis-lab',
  version='1.0.0',
  description='a system reinforcement learning',
  url='',  
  author='Ngo Xuan Phong',
  author_email='phong@vis-laboratory.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='vis_game', 
  packages=find_packages(),
  install_requires=[
    'numpy',
    'numba '] ,
  python_requires='>=3.6',
  include_package_data=True
)