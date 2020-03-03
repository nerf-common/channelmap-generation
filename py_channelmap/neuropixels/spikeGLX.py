"""
========
SpikeGLX
========

Generation of channel for probes from the spikeGLX metadata:
- neuropixels probes : 1.0 or 3A, 3B

"""
from pathlib import Path

import numpy as np
import regex as re

from ..template_probes import template_probe
from .readSGLX import ChannelCountsIM
from .readSGLX import OriginalChans
from .readSGLX import readMeta

__all__ = ["neuropixels"]


class neuropixels(template_probe):
    """ Neuropixels hardware definition

        Attributes
        ----------
        path : str
            path to the meta file from spikeGLX
    """

    def __init__(self, path):

        super().__init__()
        self.meta = readMeta(Path(path))

        try:
            self.pType = self.meta["'imDatPrb_type'"]
        except:
            self.pType = 0  # 3A probe

        self._filename = path.split(".")[0]
        self.shankSep = 250

    def create_channel_map(self):
        """ create a channel map based on the metadata

            Notes :
            ------
            - the type of neuropixels probes : 1.0 or 3A, 3B : Only one have been fully tested

            step 1: detect the type of neuropixels probes
            step 2: extract channels selected during the acquisition
            step 3: separate it in AP, LF or digital channel
            step 4: transform the channel in electrode physical id
            step 4: remove reference channels
            step 5: compute the position of each electrode selected
            step 6: package in a matlab file for kilosort and text file for the user
        """

        # get saved channels
        chans = OriginalChans(self.meta)
        AP, LF, SY = ChannelCountsIM(self.meta)
        chans = chans[0:AP]

        if self.pType <= 1:
            print("--- Neuropixel probe 1.0 or 3A ---")
            # Neuropixel 1.0 or 3A probe

            self._elecInd, self._connected = self.NP10_elecInd()

            # Trim elecInd and shankInd to include only saved channels
            self._elecInd = np.array(self._elecInd)[chans]
            shankind = np.zeros(len(self._elecInd))

            self.XYCoord10(self._elecInd)

        else:
            print("--- Neuropixel probe 2.0 ---")
            self._elecInd, shankind, bankMask, self._connected = self.NP20_elecInd()

            self._elecInd = np.array(self._elecInd[chans])
            shankind = np.array(shankind[chans])

            self.XYCoord20(self._elecInd)

        self._chanMap = np.arange(1, len(chans) + 1)
        self._chanMap0ind = np.arange(0, (len(chans)))
        self._xCoord = np.array(shankind * self.shankSep + self._xCoord)
        self._kCoord = shankind

    def NP20_elecInd(self):
        """ probe 2.0 single shank

        Notes :: Needs to be tested

        """
        if self.pType == 21:
            # single shank probe
            # imro table entries : (channel, bank, refType, electrode #)
            C = re.findall(r"\d*\s\d*\s\d*\s\d*", self.meta["imroTbl"])

            bankMask = np.zeros(len(C))
            chan = np.zeros(len(C))

            for i, element in enumerate(C):
                bankMask[i], chan[i], *_ = element.split(" ")[1]

            elecInd = chan
            shankInd = np.zeros(len(elecInd))

        else:
            C = re.findall(r"\d*\s\d*\s\d*\s\d*\s\d*", self.meta["imroTbl"])
            chan = [element.split(" ")[0] for element in C]
            elecInd = [element.split(" ")[3] for element in C]
            bankMask = [element.split(" ")[2] for element in C]
            shankInd = [element.split(" ")[1] for element in C]

        connected = np.zeros(len(elecInd))
        exchans = self.findDisabled()

        for exchan in exchans:
            connected[chan.index(exchan)] = 1

        return elecInd, shankInd, bankMask, connected

    def NP10_elecInd(self):
        """ probe 1.0 or 3B

        Already tested = sans reference channel
        """

        if "typeEnabled" in self.meta:
            C = re.findall(r"\d*\s\d*\s\d*\s\d*\s\d*", self.meta["imroTbl"])

        else:
            C = re.findall(r"\d*\s\d*\s\d*\s\d*\s\d*\s\d*", self.meta["imroTbl"])

        elecInd = np.zeros(len(C))
        chan = np.zeros(len(C))

        for i, element in enumerate(C):
            chan[i], bank, ref, *_ = element.split(" ")
            elecInd[i] = int(bank) * 384 + int(chan[i])

        connected = np.zeros(len(elecInd))

        exchans = self.findDisabled()

        for exchan in exchans:
            connected[np.where(chan == exchan)] = 1

        return elecInd, connected

    def findDisabled(self):
        """ Remove reference channels and disabled channels
        """

        C = re.findall(r"\d*:\d*:\d*:\d*", self.meta["snsShankMap"])

        enabled = np.zeros(len(C))
        for i, element in enumerate(C):
            enabled[i] = element.split(":")[3]

        chan = OriginalChans(self.meta)
        AP, _, _ = ChannelCountsIM(self.meta)

        exchan = [191]  # reference channel (1 by shank)
        for i in range(AP):
            if enabled[i] == 0:
                exchan.append(int(chan[i]))
        return exchan

    def XYCoord20(self, elecInd):
        """ Compute positions of an electrode in a probe 2.0
        """
        nElec = 1280
        vSep = 15
        hSep = 32

        elecPos = np.zeros((nElec, 2))
        elecPos[:, 0] = [(i % 2) * hSep for i in range(nElec)]
        elecPos[:, 1] = [vSep * int((i) / 2) for i in range(nElec)]

        self._xCoord = elecPos[elecInd, 0]
        self._yCoord = elecPos[elecInd, 1]

    def XYCoord10(self, electrodes):
        """ Compute positions of an electrode in a probe 1.0
        """

        self._xCoord = []
        self._yCoord = []

        for elecInd in electrodes:
            if int(elecInd) % 4 == 0:
                self._xCoord.append(43)
            elif int(elecInd) % 4 == 1:
                self._xCoord.append(11)
            elif int(elecInd) % 4 == 2:
                self._xCoord.append(59)
            else:
                self._xCoord.append(27)

            self._yCoord.append(int(elecInd / 2 + 1) * 20)
