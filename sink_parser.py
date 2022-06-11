# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 18:21:12 2022

@author: chris
"""

import pandas as pd
import ast
from cm_crypto_module import cm_otp_encrypt
import numpy as np

use_key_sink = 'C:/Users/chris/Documents/cm_key.jpg'

pd.set_option('display.max_columns', None)

cp_file = 'C:/Users/chris/Documents/nc_receive.txt'

# todo: Read byter b'\...

data = pd.read_csv(cp_file, sep=" ;", header=None, quotechar='"', engine='python', encoding='utf-8')


data[1] = data[1].apply(ast.literal_eval)


data[['ciphertext', 'key', 'source ip', 'send time']] = pd.DataFrame(data[1].tolist(), index=data.index)


del data[1]
data.rename(columns = {0:'receive time'}, inplace = True)

print(data)

print(data.columns)

for index, row in data.iterrows():
    # todo: apply function
    if str(data.loc[index, 'key']) != 'False':
        data.loc[index, 'cleartext'] = data.loc[index, 'key']
    else:
        data.loc[index, 'cleartext'] = data.loc[index, 'ciphertext']

print(data[['key', 'cleartext']])

print(data.columns)