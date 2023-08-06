from distutils.core import setup

from setuptools import setup, find_packages
setup(
  name = 'radomermbg',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  version = '0.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'background removal',   # Give a short description about your library
  author = 'SARVESH,SRIDHARAN,PRIYANKA', 
  url = '',                  # Type in your name
  author_email = 'cvradome@gmail.com',      # Type in your E-Mail
  keywords = ['background', 'subtraction'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'yolov8',
          'ultralytics',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7'
  ],
)