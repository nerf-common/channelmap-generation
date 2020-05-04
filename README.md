[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# py-channelmap

Python tools to create channelmaps:

- for different probes :
    - Neuropixels (from spikeGLX and later from OpenEphys)
    - Tetrodes
    - More to come ...

The focus is set on an uniform way to create a channelmap without worrying of the implementation behind.
Because of the probe class and the probe template, the way to create and display a channelmap is always identical with the exception of indicating the type of probes used and their options.

## Installation

### User mode

```bash
  pip install git+https://github.com/nerf-common/channelmap-generation.git
```

### Developper mode

```bash
  git clone https://github.com/nerf-common/channelmap-generation.git
  cd channelmap-generation
  python setup.py build_ext --inplace
  pip install -e .
```


## Usage


**Neuropixels probes from spikeGLX**

```python
from py_channelmap import probes
```

```python
hdw = probes("neuropixels", "*.ap.meta")
```

**Tetrodes**

1 mandatory argument :
- number of tetrodes used

1 optional argument:
- spacing : space between column (default : 200)

```python
  hdw =  probes("tetrodes", nb_tetrode, spacing = spacing)
```

**Create and draw your channelmap**

2 optional arguments:
- path = saving path of the channelmap. Sometime this parameter is already set in the implementation (neuropixels), sometime not (tetrodes),
Using this option will override others paths previously generated.
- map_format : format to save
    - channelmap (default) : csv format with headers
    - mat : matlab format
    - prb : prb format
    
It will generate the adequat channelmap file + a txt file linking the hardware electrod id with the acquisition number (often called channel id in the channelmap)

```
  hdw.create_channel_map(path=path, map_format="channelmap")
  hdw.draw()
```
