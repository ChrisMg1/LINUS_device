# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 18:21:12 2022

@author: chris
"""

import pandas as pd
import ast
from cm_crypto_module import cm_otp_encrypt



use_key_sink = 'C:/Users/chris/Documents/cm_key.jpg'

pd.set_option('display.max_columns', None)

cp_file = 'C:/Users/chris/Documents/nc_receive.txt'

# todo: Read byter b'\...

## import data frame
data = pd.read_csv(cp_file, sep=" ;", header=None, quotechar='"', engine='python', encoding='utf-8')

print(data)

## parse transmited data (tuple to df)
data[1] = data[1].apply(ast.literal_eval)



## make cloumns proper format
data.rename(columns = {0:'receive time'}, inplace = True)
data[['source ip', 'send time', 'encrypted', 'ciphertext']] = pd.DataFrame(data[1].tolist(), index=data.index)
#data['send time'] = pd.to_datetime(data['send time'],format='%Y-%m-%d %H:%M:%S.%f')
#data['receive time'] = pd.to_datetime(data['receive time'],format='%Y-%m-%d %H:%M:%S.%f')


## ...and delete raw input
del data[1]
print(data)


## calculate time estimate
data['time diff'] = data['receive time'] - data['send time']
data['time diff [s]'] = ( data['receive time'] - data['send time'] ).dt.total_seconds()




## decipher, where approropriate (#todo: avoid looping through df)
for index, row in data.iterrows():
    # todo: apply function
    if str(data.loc[index, 'key']) != 'False':
        data.loc[index, 'cleartext'] = cm_otp_encrypt(data.loc[index, 'ciphertext'], use_key_sink, data.loc[index, 'key'])[0]
    else:
        data.loc[index, 'cleartext'] = data.loc[index, 'ciphertext']

print(data)

# plot time difference sed-receive, grouped by originating IPs
boxplot = data.boxplot(column=['time diff [s]'], by=['source ip'])
