import socket
from common.utils import *
from common.constants import PACKET_SIZE, SYN, ACK, FIN, RST 

def client_mode(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(3)

    seq_num, ack_num = establish_conn(client_socket, (args.ip, args.port))

    close_conn(client_socket, (args.ip, args.port), seq_num, ack_num)


def establish_conn(client_socket, addr):
    #
    print(addr)
    #
    syn_packet = make_packet(0, 0, SYN)
    client_socket.sendto(syn_packet, addr)
    print("SYN packet sent")

    while True:
        packet = client_socket.recv(PACKET_SIZE)
        seq_num, ack_num, flags, data = parse_packet(packet)
        if flags & SYN and flags & ACK:
            print("SYN-ACK packet recieved")
            break
        
    ack_packet = make_packet(ack_num, seq_num + 1, ACK)
    client_socket.sendto(ack_packet, addr)
    print("ACK packet sent")
    print("Connection established")
    return seq_num + 1, ack_num

def close_conn(client_socket, addr, seq_num, ack_num):
    fin_packet = make_packet(seq_num, 0, FIN)
    client_socket.sendto(fin_packet, addr)
    print("FIN packet sent")

    while True:
        packet = client_socket.recv(PACKET_SIZE)
        seq_num, ack_num, flags, data = parse_packet(packet)
        if flags & ACK:
            print("ACK packet recieved")
            break

    while True:
        packet = client_socket.recv(PACKET_SIZE)
        seq_num, ack_num, flags, data = parse_packet(packet)
        if flags & FIN:
            print("FIN packet recived")
            break

    ack_packet = make_packet(ack_num, seq_num + 1, ACK)
    client_socket.sendto(ack_packet, addr)
    print("ACK packet is sent")
    print("Connection closed")