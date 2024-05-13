import socket
from common.constants import PACKET_SIZE, SYN, ACK, FIN
from common.utils import *
from datetime import datetime
import time

'''
    Description:
        Server side of the application
    Arguments:
        args: the given command line arguments.
    Returns nothing
'''
def server_mode(args):
    packet_to_dicard = args.discard

    HOST, PORT = args.ip, args.port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print(f"Server listening on port {PORT}")


    data, addr = server_socket.recvfrom(PACKET_SIZE)
    handle_conn(server_socket, addr, data)
    next_seq = 1
    start_time = time.time()
    file_data = b''
    total_bytes = 0 # Variable to help correctly calculate the throughput

    while True:
        packet = server_socket.recv(PACKET_SIZE)
        packet_size = len(packet)
        seq_num, ack_num, flags, data = parse_packet(packet)

        if flags & FIN:
            with open('file.jpg', 'wb') as f:
                f.write(file_data)
            print(total_bytes)
            throughput = total_bytes / 1000 / 1000 / (time.time() - start_time)
            print(f'\nThe throughput is {round(throughput, 2)} Mbps\n')
            handle_conn(server_socket, addr, packet)
            break

        # Discard the packet that was specified with the -d flag. Then sets the value to -1 to avoid discarding again.
        if seq_num == packet_to_dicard:
            packet_to_dicard = -1
        elif seq_num == next_seq:
            print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- packet {seq_num} is recieved')

            file_data += data
            total_bytes += packet_size

            ack_packet = make_packet(ack_num, seq_num, ACK)
            server_socket.sendto(ack_packet, addr)
            print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- sending ACK for the recieved packet {seq_num}')
            next_seq += 1
        # If the packet is out of order, dicard it
        else:
            print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- out of order packet {seq_num} is recieved')



'''
    Description:
        Function to handle both connection and teardown with the client.
        As informed on Zulip, no sequence or ackowledgement numbers are 
        required in the connection handling
    Arguments:
        server_socket: socket-object needed to send and recieve packets
        addr: client IP and port
        packet: packet to be handled
    Return nothing
'''
def handle_conn(server_socket, addr, packet):
    while True:
        _, _, flags, _ = parse_packet(packet)

        if flags & SYN:
            print(f'New connection from {addr}')

            print("SYN packet recieved")
            syn_ack_packet = make_packet(0, 0, SYN | ACK)
            server_socket.sendto(syn_ack_packet, addr)
            print("SYN ACK packet sent")
        elif flags & ACK:
            print("ACK packet recieved")
            print("Connection established")
            break
        elif flags & FIN:
            print("FIN packet recieved")
            ack_packet = make_packet(0, 0, FIN | ACK)
            server_socket.sendto(ack_packet, addr)
            print("FIN-ACK packet sent")
            print("Connection closed")
            break
        packet = server_socket.recv(PACKET_SIZE)
        