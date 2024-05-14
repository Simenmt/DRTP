A file-transer application written in Python using the socket and struct modules

The application is run in the command-line with the following commands:
    To run the application in server-mode:
    python/python3 application.py -s [-i ip address] [-p port] [-d packet to discard]

    To run the application in client-mode:
    python/python3 application.py -c [-i ip address] [-p port] [-f file to transer] [-w window size]

Example output of an typical run of the application:

h2$ 'python3 application.py -s -i 10.0.1.2 -p 8080'

Server listening on port 8080
New connection from ('10.0.0.1', 53070)
SYN packet recieved
SYN ACK packet sent
ACK packet recieved

Connection established

11:55:34.479112 -- packet 1 is recieved
11:55:34.479326 -- sending ACK for the recieved packet 1
11:55:34.479345 -- packet 2 is recieved
11:55:34.479380 -- sending ACK for the recieved packet 2
11:55:34.479388 -- packet 3 is recieved
11:55:34.479399 -- sending ACK for the recieved packet 3
11:55:34.479412 -- packet 4 is recieved
11:55:34.479424 -- sending ACK for the recieved packet 4
11:55:34.479431 -- packet 5 is recieved
11:55:34.479441 -- sending ACK for the recieved packet 5
11:55:34.582332 -- packet 6 is recieved
11:55:34.582734 -- sending ACK for the recieved packet 6
11:55:34.582790 -- packet 7 is recieved
11:55:34.582845 -- sending ACK for the recieved packet 7
11:55:34.582866 -- out of order packet 9 is recieved
11:55:34.582876 -- out of order packet 10 is recieved
11:55:34.686702 -- out of order packet 11 is recieved
11:55:34.687110 -- out of order packet 12 is recieved
11:55:35.184281 -- packet 8 is recieved
11:55:35.184470 -- sending ACK for the recieved packet 8
11:55:35.184514 -- packet 9 is recieved
11:55:35.184545 -- sending ACK for the recieved packet 9
...
...
11:56:26.929767 -- packet 1830 is recieved
11:56:26.931675 -- sending ACK for the recieved packet 1830
11:56:26.931741 -- packet 1831 is recieved
11:56:26.933387 -- sending ACK for the recieved packet 1831
11:56:26.933426 -- packet 1832 is recieved
11:56:26.934857 -- sending ACK for the recieved packet 1832
11:56:27.030875 -- packet 1833 is recieved
11:56:27.035176 -- sending ACK for the recieved packet 1833
11:56:27.035397 -- packet 1834 is recieved
11:56:27.037145 -- sending ACK for the recieved packet 1834
11:56:27.037201 -- packet 1835 is recieved
11:56:27.038466 -- sending ACK for the recieved packet 1835
11:56:27.038484 -- packet 1836 is recieved
11:56:27.039674 -- sending ACK for the recieved packet 1836
11:56:27.039705 -- packet 1837 is recieved
11:56:27.040676 -- sending ACK for the recieved packet 1837

The throughput is 0.12 Mbps

FIN packet recieved
FIN-ACK packet sent
Connection closed