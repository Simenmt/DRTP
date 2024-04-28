from .constants import PACKET_SIZE, SYN, ACK, FIN, RST, DATA_SIZE, HEADER_SIZE
import struct

def make_packet(seq_num, ack_num, flags, data=b''):
    header = struct.pack('HHH', seq_num, ack_num, flags)
    packet = header + data.ljust(DATA_SIZE, b'\0')
    return packet

def parse_packet(packet):
    seq_num, ack_num, flags = struct.unpack('HHH', packet[:HEADER_SIZE])

    data = packet[HEADER_SIZE:].rstrip(b'\0')
    return seq_num, ack_num, flags, data