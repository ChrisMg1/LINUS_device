# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 18:21:12 2022

@author: chris
"""

import pandas as pd
import ast
from cm_crypto_module import cm_otp_encrypt_sha, cm_generate_key

## load key file (secret)
use_key_sink = 'C:/Users/chris/Documents/cm_key.jpg'

pd.set_option('display.max_columns', None)

cp_file = 'C:/Users/chris/Documents/nc_receive.txt'

# todo: Read byter b'\...

## import data frame
data = pd.read_csv(cp_file, sep=" ;", header=None, quotechar='"', engine='python', encoding='utf-8')

## parse transmited data (tuple to df)
data[1] = data[1].apply(ast.literal_eval)

## make cloumns proper format...
data.rename(columns = {0:'receive time'}, inplace = True)
data[['source ip', 'send time', 'encrypted', 'ciphertext']] = pd.DataFrame(data[1].tolist(), index=data.index)

## ...and delete raw input
del data[1]

## calculate time estimate
data['time diff [ms]'] = ( data['receive time'] - data['send time'] )

## decipher, where approropriate (#todo: avoid looping through df)
for index, row in data.iterrows():
    # todo: apply function
    if data.loc[index, 'encrypted']:
        ## recover key from salts and secret
        data.loc[index, 'key'] = cm_generate_key(use_key_sink, data.loc[index, 'source ip'], data.loc[index, 'send time'])
        
        ## decrypt message
        data.loc[index, 'cleartext'] = cm_otp_encrypt_sha(data.loc[index, 'ciphertext'], data.loc[index, 'key'])
    else:
        data.loc[index, 'cleartext'] = data.loc[index, 'ciphertext']

print(data, data.dtypes)

# plot time difference sed-receive, grouped by originating IPs
boxplot = data.boxplot(column=['time diff [ms]'], by=['source ip'])
