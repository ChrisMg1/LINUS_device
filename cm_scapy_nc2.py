#!/usr/bin/env python
# The above line indicates that this is a python script.
# Author:  Ralph Bean <rbean@redhat.com>

# From: https://gist.github.com/ralphbean/4177812

# This line imports python objects from the scapy module

import sys
sys.path.append("/home/pi/.local/lib/python3.9/site-packages")


from scapy.all import sendp, TCP, IP

# Can we get scapy to talk with netcat?
# http://stackoverflow.com/questions/12062781/how-to-make-netcat-display-payload-of-packet
# Run "nc -l 9001"

# This will send one empty packet to tcp://127.0.0.1:9001
sendp(TCP(dport=4455) / IP(dst="169.254.253.229"))

# It doesn't do a full tcp handshake, though.  We have to use SocketStream for
# that.  http://trac.secdev.org/scapy/wiki/TCP
import socket
from scapy.all import StreamSocket, Raw

s = socket.socket()
s.connect(("169.254.253.229", 4455))

ss = StreamSocket(s, Raw)

ss.sr1(Raw("CM Hello World223443q\n"))


#  * What kind of payload is a zeromq SUB socket expecting?
#    (It's described here http://rfc.zeromq.org/spec:2 )
