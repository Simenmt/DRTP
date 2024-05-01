import socket
from datetime import datetime
from common.utils import *
from common.constants import PACKET_SIZE, SYN, ACK, FIN 

def client_mode(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.5)

    seq_num, ack_num = establish_conn(client_socket, (args.ip, args.port))

    send_data(client_socket, seq_num, ack_num, (args.ip, args.port), args.file, args.window)

    close_conn(client_socket, (args.ip, args.port), seq_num, ack_num)


def establish_conn(client_socket, addr):
    syn_packet = make_packet(1, 1, SYN)
    client_socket.sendto(syn_packet, addr)
    print("SYN packet sent")

    while True:
        try:
            packet = client_socket.recv(PACKET_SIZE)
        except (TimeoutError, ConnectionResetError) as err:
            print(err)
            print("Connection failed")
            exit(1)
        seq_num, ack_num, flags, data = parse_packet(packet)
        if flags & SYN and flags & ACK:
            print("SYN-ACK packet recieved")
            break
        
    ack_packet = make_packet(ack_num, seq_num + 1, ACK)
    client_socket.sendto(ack_packet, addr)
    print("ACK packet sent")
    print("Connection established\n")
    return ack_num + 1, seq_num

def close_conn(client_socket, addr, seq_num, ack_num):
    fin_packet = make_packet(ack_num, seq_num + 1, FIN)
    client_socket.sendto(fin_packet, addr)
    print("FIN packet sent")

    while True:
        packet = client_socket.recv(PACKET_SIZE)
        seq_num, ack_num, flags, _ = parse_packet(packet)
        if flags & ACK:
            print("ACK packet recieved")
            break

    while True:
        packet = client_socket.recv(PACKET_SIZE)
        seq_num, ack_num, flags, _ = parse_packet(packet)
        if flags & FIN:
            print("FIN packet recived")
            break

    ack_packet = make_packet(ack_num, seq_num + 1, ACK)
    client_socket.sendto(ack_packet, addr)
    print("ACK packet is sent")
    print("Connection closed")


def send_data(client_socket, seq_num, ack_num, addr, file_name, window_size):
    print('Data transfer:\n')
    with open(file_name, 'rb') as f:
        file_data = f.read()

    base_seq = seq_num
    packets = dict()
    i = 0
    while i < len(file_data):
        while seq_num <  base_seq + window_size:
            chunk = file_data[i:i + DATA_SIZE]
            packet = make_packet(seq_num, ack_num + 1, 0, chunk)

            packets[seq_num] = packet
            client_socket.sendto(packet, addr)
            print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- packet with seq = {seq_num} is sent, sliding window = {packets.keys()}')
            seq_num += 1
            i += DATA_SIZE

        packets, base_seq = recv_ack(client_socket, packets, addr, base_seq)

    # To recieve the ACK's of the last packets before closing the connection
    while len(packets) > 0:
        packets, base_seq = recv_ack(client_socket, packets, addr, base_seq)
    
    return seq_num, ack_num


def recv_ack(client_socket, packets, addr, base_seq):
    try:
        packet = client_socket.recv(PACKET_SIZE)
        _, ack_num, flags, _ = parse_packet(packet)
        if flags & ACK:
            if ack_num in packets.keys():
                print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- ACK for packet = {ack_num} is recieved')
                if ack_num == base_seq:
                    base_seq += 1
                del packets[ack_num]
                
                
    except TimeoutError:
        print("RTO occured")

        for seq_num, packet in packets.items():
            print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- retransmitting packet with seq {seq_num}')
            client_socket.sendto(packet, addr)

    return packets, base_seq