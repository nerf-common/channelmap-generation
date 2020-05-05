"""
===============
Template probes
===============
"""
import os

import numpy as np

__all__ = ["template_probe"]


class template_probe:
    def __init__(self):
        self._xCoord = None
        self._yCoord = None
        self._kCoord = None
        self._elecInd = None
        self._connected = None
        self._chanMap = None
        self._chanMap0ind = None
        self._filename = None

    @property
    def filename(self):
        return self._filename

    @property
    def yCoord(self):

        if self._yCoord is None:
            self.create_channel_map()

        return self._yCoord

    @property
    def xCoord(self):

        if self._xCoord is None:
            self.create_channel_map()

        return self._xCoord

    @property
    def kCoord(self):

        if self._kCoord is None:
            self.create_channel_map()

        return self._kCoord

    @property
    def elecInd(self):

        if self._elecInd is None:
            self.create_channel_map()

        return self._elecInd

    @property
    def connected(self):
        if self._connected is None:
            self.create_channel_map()

        return self._connected

    @property
    def chanMap(self):
        if self._chanMap is None:
            self.create_channel_map()
        return self._chanMap

    @property
    def chanMap0ind(self):

        if self._chanMap0ind is None:
            self.create_channel_map()

        return self._chanMap0ind

    def create_channel_map(self):
        print("not implemented at this level")
        pass


class unknown_probe(template_probe):
    @classmethod
    def from_dict(cls, file):
        obj = cls()
        obj._filename = os.path.splitext(file)[0]
        obj._xCoord = []
        obj._yCoord = []
        obj._kCoord = []
        obj._connected = []
        obj._chanMap = []
        obj._chanMap0ind = []
        obj._filename = []
        if os.path.splitext(file)[1] == ".channelmap":
            with open(file, mode="r") as file:
                for index, rows in enumerate(file):
                    if index == 0:
                        continue
                    rows = rows.split(",")
                    obj._chanMap.append(int(rows[0]))
                    obj._chanMap0ind.append(int(rows[1]))
                    obj._connected.append(int(rows[2]))
                    obj._xCoord.append(int(rows[3]))
                    obj._yCoord.append(int(rows[4]))
                    obj._kCoord.append(int(rows[5]))
        else:
            raise ("This format does have a read function yet.")
        return obj

    def create_channel_map(self):
        self._chanMap = np.array(self._chanMap)
        self._chanMap0ind = np.array(self._chanMap0ind)
        self._connected = np.array(self._connected)
        self._xCoord = np.array(self._xCoord)
        self._yCoord = np.array(self._yCoord)
        self._kCoord = np.array(self._kCoord)
