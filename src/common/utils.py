from .constants import PACKET_SIZE, SYN, ACK, FIN, RST, DATA_SIZE, HEADER_SIZE
import struct

'''
    Description:
        Function to create a packet using the struct-module
    Arguments:
        seq_num: sequence number of the packet
        ack_num: acknowledgment number of the packet
        flags: flags to be set in the packet; ACK, SYN, FIN or RST
        data: data to be sent. No data as default because of packets only meant for connection handling
    Returns the created packet
'''
def make_packet(seq_num, ack_num, flags, data=b''):
    header = struct.pack('HHH', seq_num, ack_num, flags)
    packet = header + data
    return packet

'''
    Description:
        Function to correctly unpack a recieved packet using the struct-module.
        'HHH' determines the size of 6 bytes (H = unsigned short, 2 bytes)
    Arguments:
        packet: the packet to be parsed
    Returns a tuple of the contents of the packet
'''
def parse_packet(packet):
    seq_num, ack_num, flags = struct.unpack('HHH', packet[:HEADER_SIZE])

    data = packet[HEADER_SIZE:]
    return seq_num, ack_num, flags, data