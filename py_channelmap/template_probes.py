"""
===============
Template probes
===============
"""


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
