# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 18:21:12 2022

@author: chris
"""

import pandas as pd
import ast

cp_file = 'C:/Users/chris/Documents/nc_receive.txt'

# todo: Read byter b'\...

data = pd.read_csv(cp_file, sep=" ;", header=None, quotechar='"', engine='python', encoding='utf-8')

print(data)


print(type(data[1][1]))
data[1] = data[1].apply(ast.literal_eval)
print(type(data[1][1]))


#data[2]= data[1]

#print(data[1][2])


#data[['b1', 'b2', 'b3', 'b4']] = pd.DataFrame(data[1].tolist(), index=data.index)

print (data)