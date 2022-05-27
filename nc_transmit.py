# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:07:02 2022

@author: chris
"""

# All parameters are stored in external file (not on github)
import config

import socket
import sys
import time


static = True


if (static):
    hostname = config.dest_uri
    port = config.dest_port
    print_out = config.to_print
else:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    print_out = sys.argv[3]

def nc_transmit(hn, p, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hn, p))
    s.sendall(content.encode())
    time.sleep(0.5)
    s.shutdown(socket.SHUT_WR)
    s.close()


nc_transmit(hostname, port, print_out)