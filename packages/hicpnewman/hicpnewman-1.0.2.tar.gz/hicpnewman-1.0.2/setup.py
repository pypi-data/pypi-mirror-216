from setuptools import setup, find_packages, find_namespace_packages
  
# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    ]

# specify requirements of your package here
REQUIREMENTS = [
    'os',
    'datetime',
    'tempfile',
    'subprocess',
    'json',
    'argparse',
    'typing',
    'dataclasses',
    'setuptools',
    'dataclasses_json'
]
  
# calling the setup function 
setup(name='hicpnewman',
      version='1.0.2',
      description='a newman collection runner for hicp',
      url='https://kms-solutions.net',
      author='Antoine Buisson',
      author_email='antoine.buisson@kmse-tech.com',
      packages = ['hicpnewman'],
      package_data={'hicpnewman': ['config/*', 'templates/aggregated/*', 'templates/full/*', 'templates/original/*']},
        entry_points ={
            'console_scripts': [
                'hicpnewman = hicpnewman.hicpnewman_argparser:main'
            ]
        },
      license='MIT',
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='newman hicp runner'
      )