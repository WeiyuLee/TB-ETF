# -*- coding: utf-8 -*-
"""
Created on Wed May  2 17:43:06 2018

@author: Weiyu_Lee
"""

import numpy as np
import pandas as pd

import config as conf

from tqdm import tqdm

def ud_preprocess(tasharep_ID, member_ID, Date, org_data):
    
    print("========== UD Preprocess Start ==========")
    
    UD_conf = conf.config('feature_conf').config['UD']
    if UD_conf["enable"] is False:
        
        print("UD features are disabled.")
    else:
        ID_pbar = tqdm(range(len(member_ID)))

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
                    
                org_data.loc[member_ID[ID_idx]][Date[Date_idx]].extend(encode)
                
            ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))
        
        feature_list = ["UD_0", "UD_1", "UD_2"]
        
    print("========== UD Preprocess Done! ==========")   
    
    return org_data, feature_list