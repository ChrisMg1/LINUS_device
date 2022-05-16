# -*- coding: utf-8 -*-
"""
Created on Mon May 16 08:08:39 2022

@author: chris
"""

import os
import sys
from cv2 import VideoCapture, imshow, imwrite, destroyWindow, destroyAllWindows
from random import randbytes

print(os.name)
print(sys.version)


def take_pic(pic_file):
    cam_port = 0
    cam = VideoCapture(cam_port)
    result, image = cam.read()
    imshow("key_pic", image)            
    imwrite(pic_file, image)
    destroyWindow("key_pic")
    cam.release()
    destroyAllWindows()
    

def generate_key(out_path, out_file, key_type = 'byte', key_size = 1024):
    """Generate key of specific type and length to an out file. Available types are picture (pic), sound (wave)
    or bytes (byte). The latter is distinguished in software and hardware random number generator"""
    key_file = out_path + out_file
    
    
    if (key_type == 'pic'):
        
        # initialize key file
        text_file = open(key_file, "wb")
        text_file.write(b'')
        text_file.close()
        
        # concatenate arbitrary pictures until requested filesize is reached
        while (os.path.getsize(key_file) < key_size):
            print('size before: '+str(os.path.getsize(key_file)))
            take_pic(out_path+'temp_pic_to_concatenate.jpg')        
            read_file1 = open(key_file, "ab")
            read_file2 = open(out_path+'temp_pic_to_concatenate.jpg', "rb")
            
            for i in read_file2:
                read_file1.write(i)
                
                
            read_file2.close()
        
        # clean (truncate, close)
        os.remove(out_path+'temp_pic_to_concatenate.jpg')
        read_file1.truncate(key_size)
        read_file1.close()
        return None

    if (key_type == 'byte'):
        try:
            rng_file = open("/dev/hwrng", "rb")
            random_bytes = rng_file.read(key_size)
        except:
            print('no hardware rng found, using software')
            random_bytes = randbytes(key_size)        
        finally:
            text_file = open(key_file, "wb")
            text_file.write(random_bytes)
            text_file.close()
            return None
    
    if (key_type == 'sound'):
        # todo
        return None

path = 'C:/Users/chris/Documents/'
file = 'cm_key_temp'


ret = generate_key(path, file, 'byte', 1028)

print(ret)
