from py_channelmap import probes

hdw = probes.read_from("test.channelmap")

hdw.create_channel_map(path="./channelmap", map_format="prb")
hdw.draw()
