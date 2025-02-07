#! /usr/bin/env python3

from setuptools import setup

setup(name="python-fbus",
      version="0.0.1",
      description="Fastwel FBUS Protocol v2.4",
      url="http://gitlab.main1325.ru/aaryadno/python-fbus",
      author="Alexey Ryadno",
      author_email="aryadno@mail.ru",
      license="MIT",
      packages=["fbus", "fbus.libs", "fbus.device"],
      package_data={"fbus": ["libs/*.dll", "libs/*.so"]},
      platforms=["Linux", "Windows"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: Microsoft :: Windows",
                   "Operating System :: POSIX :: Linux",
                   "Operating System :: POSIX",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11",
                  ],
     )
