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
        try:
            data, addr = server_socket.recvfrom(PACKET_SIZE)
            handle_conn(server_socket, addr, data)
        except:
            print("HALLOOOOO")
            continue

        while True:
            packet = server_socket.recv(PACKET_SIZE)
            
            seq_num, ack_num, flags, data = parse_packet(packet)
            #
            print(f'FLAGS: {flags}')
            #
            if flags == FIN:
                handle_conn(server_socket, addr, packet)
                break
                
        





def handle_conn(server_socket, addr, packet):
    print(f'New connection from {addr}')
    while True:
        #packet = server_socket.recv(PACKET_SIZE)

        seq_num, ack_num, flags, data = parse_packet(packet)

        if flags & SYN:
            print("SYN packet recieved")
            syn_ack_packet = make_packet(0, seq_num + 1, SYN | ACK)
            server_socket.sendto(syn_ack_packet, addr)
            print("SYN ACK packet sent")
            sleep(2)
        elif flags & ACK:
            print("ACK packet recieved")
            print("Connection established")
            break
        elif flags & FIN:
            #
            print("HER ER JEG NÅ")
            #
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
        