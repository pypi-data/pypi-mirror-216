from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ezAdmin',
  version='0.0.1',
  description='An easier way of PYUAC module',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='EzGame Guy',
  author_email='lephuchung9267@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ezAdmin', 
  packages=find_packages(),
  install_requires=[''] 
)