import argparse
import ipaddress
import os
from socket import *
import server
import client

def main():
    args = get_args()

    if not check_ip(args.ip):
        print("Invalid IP. It must in this format: 10.1.2.3")
        exit(1)

    if not validate_port(args.port):
        print("Invalid port. It must be within the range [1025,65535]")
        exit(1)

    if args.server:
        if args.file:
            print("unrecognized arguments for server: -f/--file")
            exit(1)
        server.server_mode(args)
    elif args.client:
        if args.discard:
            print("unrecognized arguments for client: -d/--discard")
            exit(1)
        client.client_mode(args)




'''
    Description:
        Borrowed function "ip_check.py" from the GitHub-repo for the course.
        Checks that the given IP address is a valid IPv4 address.
    Arguments:
        address: takes an IP-address as an argument.
    Returns True or False depending on the validation of the adddress
'''
def check_ip(address):
    try:
       ipaddress.ip_address(address)
       return True
    except ValueError:
       print(f"The IP address {address} is not valid")
       return False
    

# Function to validate that the given port number is valid.
# Returns True/False depending on the validation.
def validate_port(port):
    return not(port < 1025 or port > 65535)


"""
    Description:
        Adds the required options for the command.
    Returns the parsed args
"""
def get_args():
    parser = argparse.ArgumentParser(description="data args")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--server', action='store_true', help='run as server')
    group.add_argument('-c', '--client', action='store_true', help='run as client')


    parser.add_argument('-i', '--ip', type=str, default='10.0.1.2', help='port to use')
    parser.add_argument('-p', '--port', type=int, default=8080, help='IP address')
    parser.add_argument('-f', '--file', type=str, help='file to send')
    parser.add_argument('-w', '--window', type=int, default=3, help='window size')
    parser.add_argument('-d', '--discard', type=int, help='seqnum to discard once')
    
    
    return parser.parse_args()


"""
def get_args():
    # Opprett en toppnivå parser
    parser = argparse.ArgumentParser(description="data args")
    parser.add_argument('-i', '--ip', type=str, default='10.0.1.2', help='IP address to use')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Port to use')

    # Definer mutually exclusive group for server og klient flag
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--server', action='store_true', help='run as server')
    group.add_argument('-c', '--client', action='store_true', help='run as client')

    # Først parse de kjente argumentene
    args, unknown = parser.parse_known_args()

    # Deretter parse resten av argumentene basert på om vi er i server eller klient modus
    if args.server:
        server_parser = argparse.ArgumentParser()
        server_parser.add_argument('-w', '--window', type=int, default=3, help='Window size for server')
        server_parser.add_argument('-d', '--discard', type=int, help='Discard rate for server')
        server_args = server_parser.parse_args(unknown)
        args.window = server_args.window
        args.discard = server_args.discard
    elif args.client:
        client_parser = argparse.ArgumentParser()
        client_parser.add_argument('-f', '--file', type=str, required=True, help='File to send for client')
        client_args = client_parser.parse_args(unknown)
        args.file = client_args.file

    return args
"""



if __name__ == "__main__":
    main()