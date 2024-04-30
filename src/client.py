import socket
from sqlite3 import DatabaseError
from common.utils import *
from common.constants import PACKET_SIZE, SYN, ACK, FIN, RST 

def client_mode(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.5)

    seq_num, ack_num = establish_conn(client_socket, (args.ip, args.port))

    send_data(client_socket, ack_num, seq_num, (args.ip, args.port), args.file)

    close_conn(client_socket, (args.ip, args.port), seq_num, ack_num)


def establish_conn(client_socket, addr):
    #
    print(addr)
    #
    syn_packet = make_packet(1, 1, SYN)
    client_socket.sendto(syn_packet, addr)
    print("SYN packet sent")

    while True:
        try:
            packet = client_socket.recv(PACKET_SIZE)
        except TimeoutError:
            print("Connection failed")
            exit(1)
        seq_num, ack_num, flags, data = parse_packet(packet)
        if flags & SYN and flags & ACK:
            print("SYN-ACK packet recieved")
            break
        
    ack_packet = make_packet(ack_num, seq_num + 1, ACK)
    client_socket.sendto(ack_packet, addr)
    print("ACK packet sent")
    print("Connection established")
    return ack_num + 1, seq_num

def close_conn(client_socket, addr, seq_num, ack_num):
    fin_packet = make_packet(ack_num, seq_num + 1, FIN)
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


def send_data(client_socket, seq_num, ack_num, addr, file_name):
    with open(file_name, 'rb') as f:
        file_data = f.read()
        
    for i in range(0, len(file_data), DATA_SIZE):
        chunk = file_data[i:i + DATA_SIZE]
        print(f'SEQ_NUM: {seq_num}')
        packet = make_packet(ack_num, seq_num + 1, 0, chunk)

        client_socket.sendto(packet, addr)
        seq_num += 1
        try:
            packet = client_socket.recv(PACKET_SIZE)
        except TimeoutError:
            packet = make_packet(seq_num, ack_num + 1, 0, chunk)

        seq_num, ack_num, flags, data = parse_packet(packet)
        
    return seq_num, ack_num
