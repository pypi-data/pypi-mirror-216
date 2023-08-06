from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TerminalPyAPI',
  version='1.0.1',
  description='TerminalPyAPI',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mithun Kumar',
  author_email='spkthomithun@hotmail.com',
  license='BSD 3-Clause', 
  classifiers=classifiers,
  keywords='Terminal', 
  packages=find_packages(),
  install_requires=[''] 
)