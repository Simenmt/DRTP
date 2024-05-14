A file-transer application written in Python using the socket and struct modules

The application is run in the command-line with the following commands:

    To run the application in server-mode:
    python/python3 application.py -s [-i ip address] [-p port] [-d packet to discard]

    To run the application in client-mode:
    python/python3 application.py -c [-i ip address] [-p port] [-f file to transer] [-w window size]

Example output of an typical run of the application:

Server:

```console
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
```

Client:

```console
h1$ 'python3 application.py -c -i 10.0.1.2 -p 8080 -f iceland_safiqul.jpg -w 5'

SYN packet sent
SYN-ACK packet recieved
ACK packet sent
Connection established

Data transfer:

11:55:34.369603 -- packet with seq = 1 is sent, sliding window = {1}
11:55:34.369667 -- packet with seq = 2 is sent, sliding window = {1, 2}
11:55:34.369683 -- packet with seq = 3 is sent, sliding window = {1, 2, 3}
11:55:34.369707 -- packet with seq = 4 is sent, sliding window = {1, 2, 3, 4}
11:55:34.369720 -- packet with seq = 5 is sent, sliding window = {1, 2, 3, 4, 5}
11:55:34.479508 -- ACK for packet = 1 is recieved
11:55:34.479627 -- packet with seq = 6 is sent, sliding window = {2, 3, 4, 5, 6}
11:55:34.479649 -- ACK for packet = 2 is recieved
11:55:34.479667 -- packet with seq = 7 is sent, sliding window = {3, 4, 5, 6, 7}
11:55:34.479676 -- ACK for packet = 3 is recieved
11:55:34.479691 -- packet with seq = 8 is sent, sliding window = {4, 5, 6, 7, 8}
11:55:34.479698 -- ACK for packet = 4 is recieved
11:55:34.479711 -- packet with seq = 9 is sent, sliding window = {5, 6, 7, 8, 9}
11:55:34.479717 -- ACK for packet = 5 is recieved
11:55:34.479735 -- packet with seq = 10 is sent, sliding window = {6, 7, 8, 9, 10}
11:55:34.582938 -- ACK for packet = 6 is recieved
11:55:34.583052 -- packet with seq = 11 is sent, sliding window = {7, 8, 9, 10, 11}
11:55:34.583070 -- ACK for packet = 7 is recieved
...
...
11:56:26.825471 -- packet with seq = 1830 is sent, sliding window = {1826, 1827, 1828, 1829, 1830}
11:56:26.826659 -- ACK for packet = 1826 is recieved
11:56:26.826688 -- packet with seq = 1831 is sent, sliding window = {1827, 1828, 1829, 1830, 1831}
11:56:26.827834 -- ACK for packet = 1827 is recieved
11:56:26.827863 -- packet with seq = 1832 is sent, sliding window = {1828, 1829, 1830, 1831, 1832}
11:56:26.928514 -- ACK for packet = 1828 is recieved
11:56:26.928578 -- packet with seq = 1833 is sent, sliding window = {1829, 1830, 1831, 1832, 1833}
11:56:26.930023 -- ACK for packet = 1829 is recieved
11:56:26.930114 -- packet with seq = 1834 is sent, sliding window = {1830, 1831, 1832, 1833, 1834}
11:56:26.931770 -- ACK for packet = 1830 is recieved
11:56:26.931874 -- packet with seq = 1835 is sent, sliding window = {1831, 1832, 1833, 1834, 1835}
11:56:26.933540 -- ACK for packet = 1831 is recieved
11:56:26.933601 -- packet with seq = 1836 is sent, sliding window = {1832, 1833, 1834, 1835, 1836}
11:56:26.934951 -- ACK for packet = 1832 is recieved
11:56:26.935002 -- packet with seq = 1837 is sent, sliding window = {1833, 1834, 1835, 1836, 1837}
11:56:27.035375 -- ACK for packet = 1833 is recieved
11:56:27.037202 -- ACK for packet = 1834 is recieved
11:56:27.038528 -- ACK for packet = 1835 is recieved
11:56:27.039756 -- ACK for packet = 1836 is recieved
11:56:27.040639 -- ACK for packet = 1837 is recieved

DATA finished


FIN packet sent
FIN-ACK packet recieved
Connection closed
```

Example of an output while using the -d flag to discard the chosen packet:

Server:

```console
h2$ 'python3 application.py -s -i 10.0.1.2 -p 8080 -d 6'

Server listening on port 8080
New connection from ('10.0.0.1', 47561)
SYN packet recieved
SYN ACK packet sent
ACK packet recieved
Connection established

13:37:23.068013 -- packet 1 is recieved
13:37:23.068116 -- sending ACK for the recieved packet 1
13:37:23.068143 -- packet 2 is recieved
13:37:23.068185 -- sending ACK for the recieved packet 2
13:37:23.068197 -- packet 3 is recieved
13:37:23.068215 -- sending ACK for the recieved packet 3
13:37:23.068230 -- packet 4 is recieved
13:37:23.068248 -- sending ACK for the recieved packet 4
13:37:23.068257 -- packet 5 is recieved
13:37:23.068273 -- sending ACK for the recieved packet 5
13:37:23.169363 -- out of order packet 7 is recieved
13:37:23.169394 -- out of order packet 8 is recieved
13:37:23.169405 -- out of order packet 9 is recieved
13:37:23.169415 -- out of order packet 10 is recieved
13:37:23.671860 -- packet 6 is recieved
13:37:23.672269 -- sending ACK for the recieved packet 6
13:37:23.672300 -- packet 7 is recieved
13:37:23.672359 -- sending ACK for the recieved packet 7
...
...
13:38:01.708538 -- packet 1830 is recieved
13:38:01.709959 -- sending ACK for the recieved packet 1830
13:38:01.805536 -- packet 1831 is recieved
13:38:01.807399 -- sending ACK for the recieved packet 1831
13:38:01.807926 -- packet 1832 is recieved
13:38:01.809655 -- sending ACK for the recieved packet 1832
13:38:01.809697 -- packet 1833 is recieved
13:38:01.811183 -- sending ACK for the recieved packet 1833
13:38:01.811218 -- packet 1834 is recieved
13:38:01.813494 -- sending ACK for the recieved packet 1834
13:38:01.813526 -- packet 1835 is recieved
13:38:01.814959 -- sending ACK for the recieved packet 1835
13:38:01.910026 -- packet 1836 is recieved
13:38:01.912065 -- sending ACK for the recieved packet 1836
13:38:01.912101 -- packet 1837 is recieved
13:38:01.913519 -- sending ACK for the recieved packet 1837
1836516

The throughput is 0.05 Mbps

FIN packet recieved
FIN-ACK packet sent
Connection closed
```

Client:

```console
h1$ 'python3 application.py -c -i 10.0.1.2 -p 8080 -f iceland_safiqul.jpg -w 5'

SYN packet sent
SYN-ACK packet recieved
ACK packet sent
Connection established

Data transfer:

13:37:22.966853 -- packet with seq = 1 is sent, sliding window = {1}
13:37:22.966923 -- packet with seq = 2 is sent, sliding window = {1, 2}
13:37:22.966939 -- packet with seq = 3 is sent, sliding window = {1, 2, 3}
13:37:22.966963 -- packet with seq = 4 is sent, sliding window = {1, 2, 3, 4}
13:37:22.966977 -- packet with seq = 5 is sent, sliding window = {1, 2, 3, 4, 5}
13:37:23.068221 -- ACK for packet = 1 is recieved
13:37:23.068299 -- packet with seq = 6 is sent, sliding window = {2, 3, 4, 5, 6}
13:37:23.068317 -- ACK for packet = 2 is recieved
13:37:23.068489 -- packet with seq = 7 is sent, sliding window = {3, 4, 5, 6, 7}
13:37:23.068517 -- ACK for packet = 3 is recieved
13:37:23.068550 -- packet with seq = 8 is sent, sliding window = {4, 5, 6, 7, 8}
13:37:23.068563 -- ACK for packet = 4 is recieved
13:37:23.068585 -- packet with seq = 9 is sent, sliding window = {5, 6, 7, 8, 9}
13:37:23.068596 -- ACK for packet = 5 is recieved
13:37:23.068625 -- packet with seq = 10 is sent, sliding window = {6, 7, 8, 9, 10}
13:37:23.571098 -- RTO occured
13:37:23.571161 -- retransmitting packet with seq 6
13:37:23.571234 -- retransmitting packet with seq 7
13:37:23.571253 -- retransmitting packet with seq 8
13:37:23.571269 -- retransmitting packet with seq 9
13:37:23.571284 -- retransmitting packet with seq 10
13:37:23.672736 -- ACK for packet = 6 is recieved
13:37:23.672878 -- packet with seq = 11 is sent, sliding window = {7, 8, 9, 10, 11}
13:37:23.672897 -- ACK for packet = 7 is recieved
...
...
13:38:01.608085 -- packet with seq = 1830 is sent, sliding window = {1826, 1827, 1828, 1829, 1830}
13:38:01.704390 -- ACK for packet = 1826 is recieved
13:38:01.704509 -- packet with seq = 1831 is sent, sliding window = {1827, 1828, 1829, 1830, 1831}
13:38:01.706061 -- ACK for packet = 1827 is recieved
13:38:01.706144 -- packet with seq = 1832 is sent, sliding window = {1828, 1829, 1830, 1831, 1832}
13:38:01.707506 -- ACK for packet = 1828 is recieved
13:38:01.707569 -- packet with seq = 1833 is sent, sliding window = {1829, 1830, 1831, 1832, 1833}
13:38:01.708479 -- ACK for packet = 1829 is recieved
13:38:01.708510 -- packet with seq = 1834 is sent, sliding window = {1830, 1831, 1832, 1833, 1834}
13:38:01.710134 -- ACK for packet = 1830 is recieved
13:38:01.710172 -- packet with seq = 1835 is sent, sliding window = {1831, 1832, 1833, 1834, 1835}
13:38:01.807651 -- ACK for packet = 1831 is recieved
13:38:01.807742 -- packet with seq = 1836 is sent, sliding window = {1832, 1833, 1834, 1835, 1836}
13:38:01.809836 -- ACK for packet = 1832 is recieved
13:38:01.809935 -- packet with seq = 1837 is sent, sliding window = {1833, 1834, 1835, 1836, 1837}
13:38:01.811134 -- ACK for packet = 1833 is recieved
13:38:01.813637 -- ACK for packet = 1834 is recieved
13:38:01.814934 -- ACK for packet = 1835 is recieved
13:38:01.912208 -- ACK for packet = 1836 is recieved
13:38:01.913253 -- ACK for packet = 1837 is recieved

DATA finished


FIN packet sent
FIN-ACK packet recieved
Connection closed
```

In cases where the server is not running or the client for some other reason is not able to connect to the given IP and port, you should expect
this simple output:

```console
h1$ 'python3 application.py -c -i 10.0.1.2 -p 8080 -f iceland_safiqul.jpg'

SYN packet sent
Connection failed
```