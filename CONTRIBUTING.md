
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# How to contribute

## Open an issue :

1. specify in the title the implementation concerned (probe type and acquisition system)
2. An use-case allowing to easily reproduce a bug is always appreciate

Issue are always welcome, don't hesitate to share your thought about this module.

## Add a new probe type :

1. Fork the repository and open a pull request
2. develop a class implementation inherited from template_probe
with at least the create_channel_map method which populate the arguments :

- _yCoord = y position
- _xCoord = x position
- _kCoord = shank position
- _elecInd = electrode number
- _connected = 1 everywhere except if broken channel deactivated (0)
- _chanMap = channel number (data acquisition indice)
- _chanMap0ind = channel number starting from 0 instead of 1

3. Specify the keyword use to connect with your implementation and the different options. And modify accordingly the probes init
4. Add the documentation in your class and in the readme
5. Add your name in the contributing list below

## Improve the module

Some features idea for the future are :
- improve the channelmap drawing
- display specify channel in the channelmap order (?)
- Add unity tests
- ...

Contributors :
------------
