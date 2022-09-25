# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 21:09:58 2022

@author: chris
"""

import redis

LINUS_redit_host = '192.168.137.75'
LINUS_redit_port = 6379

# create the redis connection
r_conn = redis.Redis( host = LINUS_redit_host, port = LINUS_redit_port)

# create a key-value pair with key as name and value as "amalgjose"
r_conn.set('name', '22deadbeef')

# retrieve the value by using the key
value = r_conn.get('name')
print("cm Value from Redis -->", value)