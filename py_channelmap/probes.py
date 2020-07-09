"""
======
Probes
======

Utilities collection for probes :
- channelmap
- config files
- visualization
"""
import numpy as np
from scipy.io import savemat

from py_channelmap.neuropixels.spikeGLX import neuropixels
from py_channelmap.template_probes import unknown_probe
from py_channelmap.tetrodes import tetrode

__all__ = ["probes"]


class probes:
    """ first layer to manage the difference probes in the same way

    Attributes
    ----------

    keyword : str
        key word indicating which class called. For the moment, "neuropixels" and "tetrodes" are available

    **options : dict
        depending of the type of probes. For example: "neuropixels" needs the path of the data bin file

    """

    def __init__(self, probes_type, *options, **kwargs):

        if probes_type == "neuropixels":

            assert (
                "meta" in options[0]
            ), "this keyword take in input at least one other parameter : the path to the meta file from spikeGLX"

            self.probe = neuropixels(options[0])

        elif probes_type == "tetrodes":
            assert isinstance(
                options[0], int
            ), "this keyword take in input at least one other parameter : the number of tetrodes. Also, it can take one other optional parameter: the space between rows"

            self.probe = tetrode(*options, **kwargs)
        elif probes_type == "unknown":
            self.probe = unknown_probe.from_dict(options[0])
        else:
            raise (
                ValueError(
                    "Probe type not yet implemented: if interested by it, create an issue in the repo"
                )
            )

    @classmethod
    def read_from(cls, file):
        return cls("unknown", file)

    def create_channel_map(self, path=None, map_format="channelmap"):
        """ Launch the creation of the channel map on the right type of probe
        """
        self.probe.create_channel_map()

        filename = path if path is not None else self.probe.filename
        if path is None:
            raise (
                ValueError(
                    "No saving path specify both in the specification or in this method. Make use of the path option"
                )
            )
        if self.probe.elecInd:
            np.savetxt(
                filename + "_electrod_ind.txt",
                np.concatenate(
                    (
                        self.probe.elecInd.reshape((len(self.probe.elecInd), 1)),
                        self.probe.chanMap.reshape((len(self.probe.elecInd), 1)),
                    ),
                    axis=1,
                ),
                header="electrodes id",
                fmt="%-4d",
                delimiter="",
            )

        if map_format is "channelmap":
            self._channelmap_format(filename)
        elif map_format is "mat":
            self._mat_format(filename)
        elif map_format is "prb":
            self._pb_format(filename)

    def _pb_format(self, filename):
        channel = {}
        for index, chan in enumerate(self.probe.chanMap):
            channel.update(
                {
                    chan: [
                        self.probe.xCoord[index],
                        self.probe.yCoord[index],
                        self.probe.kCoord[index],
                    ]
                }
            )

        dict_channel = {
            1: {
                "channels": list(self.probe.chanMap[self.probe.connected == 0]),
                "geometry": channel,
            }
        }
        with open(filename + ".prb", "w") as file:
            text = "total_nb_channels = %s\n" % str(
                len(self.probe.chanMap)
            ) + "channel_groups = %s" % str(dict_channel)
            file.write(text)

    def _mat_format(self, filename):
        savemat(
            filename + ".mat",
            {
                "chanMap": self.probe.chanMap,
                "chanMap0ind": self.probe.chanMap0ind,
                "connected": self.probe.connected,
                "name": self.probe.filename + ".mat",
                "xcoords": self.probe.xCoord,
                "ycoords": self.probe.yCoord,
                "kcoords": self.probe.kCoord,
            },
        )

    def _channelmap_format(self, filename):
        with open(filename + ".channelmap", "w") as file:
            file.write("Probe,Data,Disconnect,X,Y,Shank\n")
            for i in range(len(self.probe.chanMap)):
                file.write(
                    str(int(self.probe.chanMap[i]))
                    + ","
                    + str(int(self.probe.chanMap0ind[i]))
                    + ","
                    + str(int(self.probe.connected[i]))
                    + ","
                    + str(int(self.probe.xCoord[i]))
                    + ","
                    + str(int(self.probe.yCoord[i]))
                    + ","
                    + str(int(self.probe.kCoord[i]))
                    + "\n"
                )

    def draw(self, plot_line=False, annotation=False):
        """ Draw the channel map computed
        """
        import matplotlib.pyplot as plt

        plt.figure()

        x = self.probe.xCoord
        y = self.probe.yCoord

        if plot_line:
            plt.plot(x, y, lw=0.3, alpha=0.3)

        plt.scatter(x, y)

        if annotation:
            for i in range(len(x)):
                plt.annotate(
                    str(int(self.probe.chanMap0ind[i])),
                    xy=(x[i], y[i]),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha="left",  # horizontal alignment
                    va="center",  # vertical alignment
                )

        plt.show()

    def get_depth(self, channel):
        return self.probe.yCoord[np.where(self.probe.chanMap, channel)]
