# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 16:28:09 2022

@author: chris
"""

def simple_enc(ba1, ba2):
    """ XOR two byte strings """
    ret_bytes = bytes( [_a ^ _b for _a, _b in zip(ba1, ba2)])
    return ret_bytes

def cm_otp_encrypt(in_data, keyPath, keyIndex):
    """Encryption function with one-time-pad: Takes in the data to be encrypted, 
    the path to a key file and an Index of the key to be used. Returns encrypted data
    to be included in the frame"""
    with open(keyPath, "rb") as f:
        
        # Read the key file as byte object, whatever it is (e.g. txt, wav, etc.)
        cm_byteKEY = f.read()

        # Truncate to start at the right position (KexIndex)
        cm_byteKEY = cm_byteKEY[keyIndex:]        

        # Try to anticipate input data (byte: Perfect; string: Try to convert; else: bad atm....)
        if type(in_data) != bytes:
            try:
                in_data = in_data.encode('utf8')
            except:
                print("input neither byte nor string") 
        
        # en-/decrypt the input data (payload) according to OTP using the key with correct index
        cm_enc = bytes([a^b for a,b in zip(in_data, cm_byteKEY)])

    # return a key index for further use (drop at least used key, additionally "verschleiere")
    newIndex = keyIndex + len(in_data)
    return (cm_enc, newIndex)


use_msg = 'verySecretThings  '
use_key = 'C:/Users/chris/Documents/cm_key.txt'
use_idx = 0
