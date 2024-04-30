import socket
from time import sleep
from common.constants import PACKET_SIZE, SYN, ACK, FIN, RST
from common.utils import *

def server_mode(args):
    print(f'{args.ip}, {args.port}')

    HOST, PORT = args.ip, args.port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print(f"Server listening on port {PORT}")

    while True:
    
        data, addr = server_socket.recvfrom(PACKET_SIZE)
        prev_seq, ack_num = handle_conn(server_socket, addr, data)
        while True:
            packet = server_socket.recv(PACKET_SIZE)
            seq_num, ack_num, flags, data = parse_packet(packet)

            if flags & FIN:
                handle_conn(server_socket, addr, packet)
                break

            print(f'SEQ_NUM: {seq_num}')
            print(f'ACK_SEQ: {ack_num}')
            print(f'PREV_SEQ: {prev_seq}')
            if seq_num == prev_seq + 1:
                with open('file.jpg', 'ab') as f:
                    f.write(data)
                prev_seq = seq_num
                ack_packet = make_packet(ack_num, seq_num + 1, ACK)
                server_socket.sendto(ack_packet, addr)


                
        





def handle_conn(server_socket, addr, packet):
    while True:
        #packet = server_socket.recv(PACKET_SIZE)

        seq_num, ack_num, flags, _ = parse_packet(packet)

        if flags & SYN:
            print(f'New connection from {addr}')

            print("SYN packet recieved")
            syn_ack_packet = make_packet(1, seq_num + 1, SYN | ACK)
            server_socket.sendto(syn_ack_packet, addr)
            print("SYN ACK packet sent")
        elif flags & ACK:
            print("ACK packet recieved")
            print("Connection established")
            break
        elif flags & FIN:
            print("FIN packet recieved")
            ack_packet = make_packet(ack_num, seq_num + 1, ACK)
            server_socket.sendto(ack_packet, addr)
            print("ACK packet sent")
            fin_packet = make_packet(seq_num + 1, ack_num, FIN)
            server_socket.sendto(fin_packet, addr)
            print("FIN packet sent")
            print("Connection closed")
            packet = server_socket.recv(PACKET_SIZE)

            break
        packet = server_socket.recv(PACKET_SIZE)
        seq_num, ack_num, flags, data = parse_packet(packet)
    return seq_num, ack_num
        