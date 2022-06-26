# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 20:43:10 2022

@author: chris
"""


import urllib.request
import plac
#import datetime
from pathlib import Path
import socket
import time
#from ast import literal_eval as make_tuple
from cm_crypto_module import cm_otp_encrypt, cm_generate_key, cm_otp_encrypt_sha

def nc_transmit(hn, p, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hn, p))
    s.sendall(content.encode())
    time.sleep(0.5) #todo: replace with datetime
    s.shutdown(socket.SHUT_WR)
    s.close()
    
def stringClean(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """    
    #s = s.replace(",", "_")
    #s = s.replace(";", "-")
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        s = s[1:-1]
    
    ## truncate or pad to specific length; three more bytes are needed for encoding (b'')
    ## 32 byte seems suitable because key from md5 has len 32
    s = '{:32.32}'.format(s)
    
    return s


@plac.opt('port', "Destination Port", type=int)
@plac.opt('uri', "Destination URI", type=str)
#@plac.opt('key', "Key index", type=int)
@plac.opt('message', "Message / Payload", type=str)
@plac.opt('file', "Key file", type=Path)
@plac.flg('encrypt', "Encrypt Message")


def main(port=4455, uri='ebhzandffhs5ewae.myfritz.net',
         message='testtesttesttest', file='./cm_key.jpg', encrypt=False):
    """Send a message to Christoph's Raspberry with or without encryption. V0.3"""

    message = stringClean(message).encode('utf-8')
    external_ip = urllib.request.urlopen('https://ident.me').read()
    
    ## timestamp of encryption (miliseconds since epoch)
    # enc_timestamp = (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    enc_timestamp = time.time()
    
    if (encrypt):
        my_key = cm_generate_key(file, external_ip, enc_timestamp)
        #message = str(cm_otp_encrypt(message, file, key)[0])
        message = str(cm_otp_encrypt_sha(message, my_key))
        encrypt_m = 'enabled'
    else: 
        #message = str(message.encode('utf-8'))
        encrypt_m = 'disabled'
    
    # todo: Reihenfolge Ändern !!    
        
    print_out = ';(' + str(external_ip) + ',' + str(enc_timestamp) + ',' + str(encrypt) + ',' + str(message) + ')\n'

    ## Optional: Concatenate n times
    # print_out = print_out*30
    
    nc_transmit(uri, port, print_out)
    
    print('The following message was sent:\n', print_out[1:], 
          '\nEncryption was', encrypt_m, '\nPayload length:', len(message),
          'Bytes (including b\'\')')
    
    #tup = make_tuple(print_out)
    
    #print(tup[0], tup[2], tup[1])
    

if __name__ == '__main__':
    
    plac.call(main)