from setuptools import setup, find_packages

setup(name='mosaik-pv',
      version='1.0',
      description='PV simulator adapted for mosaik',
      long_description=(open('README.md', encoding='utf-8')).read(),
      author='Cornelius Steinbrink',
      author_email='mosaik@offis.de',
      url='https://gitlab.com/mosaik/components/energy/mosaik-pv',
      install_requires=[
          'numpy',
          'scipy',
          'arrow',
          'mosaik-api>=2.0',
      ],
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts':  [
              'mosaik-pv = mosaik_pv.mosaik:main',
          ],
      },
      classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
 )
