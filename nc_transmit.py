# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:07:02 2022

@author: chris
"""

import config
import socket
import sys
import time


static = True


if (static):
    hostname = config.dest_uri
    port = config.dest_port
else:
    hostname = sys.argv[1]
    port = int(sys.argv[2])

def nc_transmit(hn, p, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hn, p))
    s.sendall(content.encode())
    time.sleep(0.5)
    s.shutdown(socket.SHUT_WR)
    s.close()


nc_transmit(config.dest_uri, config.dest_port, config.to_print)