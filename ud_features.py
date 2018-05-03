# -*- coding: utf-8 -*-
"""
Created on Wed May  2 17:43:06 2018

@author: Weiyu_Lee
"""

import numpy as np
import pandas as pd
import pickle

from tqdm import tqdm

print("========== UD Preprocess Start ==========")

f = open('./Data/org_meta_data.pkl', 'rb')  
tasharep_ID = pickle.load(f)
member_ID = pickle.load(f)
Date = pickle.load(f)
_ = pickle.load(f)
_ = pickle.load(f)
org_data = pd.read_pickle('./Data/org_feature_data.pkl')

ID_pbar = tqdm(range(len(member_ID)))
output_df = pd.DataFrame()
for ID_idx in ID_pbar:
    curr_ID_data = org_data.loc[member_ID[ID_idx]]
    
    curr_close_price_seq = []
    for Date_idx in range(len(Date)):
        try:
            curr_close_price = curr_ID_data[Date[Date_idx]][3]
        except:
            curr_close_price = float(np.NAN)
        
        curr_close_price_seq.append(curr_close_price)            
           
    curr_close_price_seq_shift = curr_close_price_seq.copy()        
    del curr_close_price_seq_shift[0]    
    curr_close_price_seq_shift.insert(-1, 0)        

    curr_close_price_seq = np.array(curr_close_price_seq)  
    curr_close_price_seq_shift = np.array(curr_close_price_seq_shift)  
    
    diff = curr_close_price_seq_shift - curr_close_price_seq
    
    curr_ID_df = pd.DataFrame(index=[member_ID[ID_idx]], columns=Date)
    for Date_idx in range(len(Date)):
        if diff[Date_idx] > 0:
            encode = [0,0,1]
        elif diff[Date_idx] == 0:
            encode = [0,1,0]
        elif diff[Date_idx] < 0:    
            encode = [1,0,0]
            
        curr_ID_df[Date[Date_idx]] = [encode]

    output_df = pd.concat([output_df, curr_ID_df], axis=0)               
    ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))

feature_list = ["UD"]

print("Dumping data ...")    
f = open('./Data/ud_meta_data.pkl', 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(feature_list, f, True)  
f.close()  

output_df.to_pickle("./Data/ud_feature_data.pkl")
    
print("========== UD Preprocess Done! ==========")   