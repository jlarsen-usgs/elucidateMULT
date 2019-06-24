import sys
from setuptools import setup

if not sys.version_info[0] in [2, 3]:
    print('Sorry, emult is not supported in your Python version')
    print('  Supported versions: 2 and 3')
    print('  Your version of Python: {}'.format(sys.version_info[0]))
    sys.exit(1)  # return non-zero value for failure

long_description = ''


setup(name="emult",
      description='Elucidate mult is a package to convert mult file inputs to arrays',
      author="Joshua Larse",
      author_email='jlarsen@usgs.gov',
      url='https://github.com/jlarsen-usgs/elucidateMULT',
      license='CC0',
      platforms='Windows, Mac OS-X, Linux',
      install_requires=['enum34;python_version<"3.4"',
                        'numpy>=1.9',
                        'flopy'],
      packages=['emult'],
      include_package_data=True, # includes files listed in MANIFEST.in
      # use this version ID if .svn data cannot be found
      version="1.0",
      classifiers=['Topic :: Scientific/Engineering :: Hydrology'])
