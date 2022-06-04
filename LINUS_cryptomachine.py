# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 20:43:10 2022

@author: chris
"""


import urllib.request
import plac
from datetime import datetime
from pathlib import Path
import socket
import time
#from ast import literal_eval as make_tuple
from cm_crypto_module import cm_otp_encrypt

def nc_transmit(hn, p, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hn, p))
    s.sendall(content.encode())
    time.sleep(0.5)
    s.shutdown(socket.SHUT_WR)
    s.close()


@plac.opt('port', "Destination Port", type=int)
@plac.opt('uri', "Destination URI", type=str)
@plac.opt('key', "Key index", type=int)
@plac.opt('message', "Message / Payload", type=str)
@plac.opt('file', "Key file", type=Path)
@plac.flg('encrypt', "Encrypt Message")


def main(port=4455, uri='ebhzandffhs5ewae.myfritz.net', key=0, message='test', file='./cm_key.jpg', encrypt=False):
    """Send a message to Christoph's Raspberry with or without encryption. Version 0.1"""

    if (encrypt):
        message = str(cm_otp_encrypt(message, file, key)[0])
        encrypt_m = 'enabled'
    else: 
        encrypt_m = 'disabled'
    
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print_out = '("' + message + '",' + str(key) + ',"' + external_ip + '","' + str(datetime.now()) + '")\n'

    
    
    nc_transmit(uri, port, print_out)
    
    print('The following message was sent:\n', print_out, '\nEncryption was', encrypt_m, '\n')
    
    #tup = make_tuple(print_out)
    
    #print(tup[0], tup[2], tup[1])
    

if __name__ == '__main__':
    
    plac.call(main)