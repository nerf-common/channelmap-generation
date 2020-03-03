from setuptools import setup
from os import path

import re

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSIONFILE = "py_channelmap/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)

if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="py_channelmap",
    version=verstr,
    packages=["py_channelmap"],
    install_requires=[
        "numpy==1.16.*",
    ],
    author="Marine Chaput",
    author_email="marine.chaput@nerf.be",
    description="Nerf tools: channelmap for sorting",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers=[
                "Development Status :: 3 - Alpha",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: GPL3 License",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 3.5",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                ],
    python_requires=">=3.5",
    license="GPL3",
    zip_safe=False,
    include_package_data=True,
)
