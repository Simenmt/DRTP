import socket
from datetime import datetime
from common.utils import *
from common.constants import PACKET_SIZE, SYN, ACK, FIN 

'''
    Description:
        Client side of the application
    Arguments:
        args: the given command line arguments.
    Returns nothing
'''
def client_mode(args):
    addr = (args.ip, args.port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Sets the timeout for each socket-operation to 500ms
    client_socket.settimeout(0.5)

    establish_conn(client_socket, addr)

    send_data(client_socket, addr, args.file, args.window)

    close_conn(client_socket, addr)


'''
    Description:
        Function to handle the connection to the server using a three-way-handshake.
    Arguments:
        client_socket: socket-object needed to send and recieve packets
        addr: server IP and port
    Returns nothing
'''
def establish_conn(client_socket, addr):
    syn_packet = make_packet(0, 0, SYN)
    client_socket.sendto(syn_packet, addr)
    print("SYN packet sent")

    while True:
        try:
            packet = client_socket.recv(PACKET_SIZE)
        except (TimeoutError, ConnectionResetError) as err:
            print("Connection failed")
            exit(1)
        _, _, flags, _ = parse_packet(packet)
        if flags & SYN and flags & ACK:
            print("SYN-ACK packet recieved")
            break
        
    ack_packet = make_packet(0, 0, ACK)
    client_socket.sendto(ack_packet, addr)
    print("ACK packet sent")
    print("Connection established\n")


'''
    Description:
        Function to handle the closing of the connection with the server.
    Arguments:
        client_socket: socket-ovject needed to send and recieve packets
        addr: server IP and port
    Return nothing
'''
def close_conn(client_socket, addr):
    fin_packet = make_packet(0, 0, FIN)
    client_socket.sendto(fin_packet, addr)
    print("\nFIN packet sent")

    while True:
        packet = client_socket.recv(PACKET_SIZE)
        _, _, flags, _ = parse_packet(packet)
        if flags & ACK:
            print("FIN-ACK packet recieved")
            break
    print("Connection closed")

'''
    Description:
        Function to handle the sending of the file using a Go-Back-N logic, and with a 
        fixed sliding window size
    Arguments:
        client_socket: socket-object needed to handle the sending and reciving of packets
        seq_num: sequence number of the first packet to be sent
        ack_num: last revieved acknowledgement number from server
        addr: server IP and port
        file_name: name of the file to be sent
        window_size: size of the sliding window.
    Returns the most recent acknowledgement and sequence number 
'''
def send_data(client_socket, addr, file_name, window_size):
    print('Data transfer:\n')
    with open(file_name, 'rb') as f:
        file_data = f.read()

    base_seq = 1
    next_seq_num = 1
    ack_num = 1
    packets = dict()
    i = 0
    while i < len(file_data):
        while next_seq_num <  base_seq + window_size:
            chunk = file_data[i:i + DATA_SIZE]
            packet = make_packet(next_seq_num, ack_num + 1, 0, chunk)

            packets[next_seq_num] = packet
            client_socket.sendto(packet, addr)
            
            # To format the string in a prettier way
            keys_string = ", ".join(str(key) for key in packets.keys())
            print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- packet with seq = {next_seq_num} is sent, sliding window = {{{keys_string}}}')
            next_seq_num += 1
            i += DATA_SIZE
        try:
            base_seq = recv_ack(client_socket, packets)
        except TimeoutError:
            handle_rto(client_socket, packets, addr)

    # To recieve the ACK's of the last packets before closing the connection
    while len(packets) > 0:
        try:
            base_seq = recv_ack(client_socket, packets)
        except TimeoutError:
            handle_rto(client_socket, packets, addr)
    

'''
    Descirption:
        Function to handle incoming acks from the server
    Arguments:
        client_socket: the socket-object is needed to recieve the ack-packets.
        packets: the not yet ack'd packets
    Returns the number of the oldest not yet ack'd packet
'''
def recv_ack(client_socket, packets):
    packet = client_socket.recv(PACKET_SIZE)
    _, ack_num, flags, _ = parse_packet(packet)
    if flags & ACK:
        # If an duplicate ack is recieved, discard
        if ack_num in packets.keys():
            print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- ACK for packet = {ack_num} is recieved')
            for seq_num in packets.copy():
                del packets[seq_num]
                if seq_num == ack_num:
                    break
    return ack_num + 1

'''
    Description:
        Function to handle the situation if a timeout (500ms) occurs.
    Arguments:
        client_socket: the socket-object to resend packets
        packets: the not yet ack'd packets
        addr: server IP and port
    Returns nothing
'''   
def handle_rto(client_socket, packets, addr):
    print("RTO occured")

    for seq_num, packet in packets.items():
        print(f'{datetime.now().strftime("%H:%M:%S.%f")} -- retransmitting packet with seq {seq_num}')
        client_socket.sendto(packet, addr)