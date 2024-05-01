import socket
from time import sleep
from common.constants import PACKET_SIZE, SYN, ACK, FIN, RST
from common.utils import *
from datetime import datetime
import time

def server_mode(args):
    packet_to_dicard = args.discard
    print(f'{args.ip}, {args.port}')

    HOST, PORT = args.ip, args.port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print(f"Server listening on port {PORT}")

    while True:
        start_time = time.time()
        file_size = 0

        data, addr = server_socket.recvfrom(PACKET_SIZE)
        seq_num, ack_num = handle_conn(server_socket, addr, data)
        next_seq = ack_num + 1

        while True:
            packet = server_socket.recv(PACKET_SIZE)
            seq_num, ack_num, flags, data = parse_packet(packet)

            if flags:
                throughput = file_size / 1000 / 1000 / (time.time() - start_time)
                print(f'\nThe throughput is {round(throughput, 2)} Mbps\n')
                handle_conn(server_socket, addr, packet)
                break


            if seq_num == packet_to_dicard:
                packet_to_dicard = -1
            elif seq_num == next_seq:
                print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- packet {seq_num} is recieved')

                file_size += len(data)

                with open('file.jpg', 'ab') as f:
                    f.write(data)
                ack_packet = make_packet(ack_num, seq_num, ACK)
                server_socket.sendto(ack_packet, addr)
                print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- sending ACK for the recieved packet {seq_num}')
                next_seq += 1

            else:
                try:
                    print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- out of order packet {seq_num} is recieved')
                    ack_packet = make_packet(ack_num, next_seq - 1, ACK)
                    server_socket.sendto(ack_packet, addr)
                except NameError:
                    continue



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
    return seq_num, ack_num
        