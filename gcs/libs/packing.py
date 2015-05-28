import struct


packing24chars = '24s'

def pack_mes(m):
    return struct.pack(packing24chars, m)


def unpack_mes(m):
    return struct.unpack(packing24chars, m)
