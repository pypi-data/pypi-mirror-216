from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Adobe_Lib_Manual',
  version='4.0',
  description='abc',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ajay Pandey',
  author_email='ajaypanday678@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='adobe', 
  packages=find_packages(),
  install_requires=[''] 
)