
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='matan',
    version='0.1.5.2.7.3dev2',
    license='GPLv3',
    author="Igor Cudnik",
    author_email='igor.cudnik@student.put.poznan.pl',
    description='Material analysis package to plot or extract properties like tensile modulus etc. ',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages('matan/'),
    package_dir={'': 'matan/'},
    url='https://codeberg.org/309631/matan',
    keywords=['material analysis',
              'ISO 527',
              'ISO 527-1',
              'polymers analysis',
              'material analysis',
              'tensile test'
              'charpy'],
    install_requires=[
          'numpy',
        'matplotlib'
      ],
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 1 - Planning',

    # Indicate who your project is intended for
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
],

)
