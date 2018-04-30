# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:33:44 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import pickle
import talib

from tqdm import tqdm

print("========== TA Preprocess Start ==========")

f = open('./Data/all_data.pkl', 'rb')  
tasharep_ID = pickle.load(f)
member_ID = pickle.load(f)
Date = pickle.load(f)
_ = pickle.load(f)
_ = pickle.load(f)
org_data = pickle.load(f)

ID_pbar = tqdm(range(len(member_ID)))
output_df = pd.DataFrame()
for ID_idx in ID_pbar:
#for ID_idx in range(1298, len(member_ID)):
    curr_ID_data = org_data.loc[member_ID[ID_idx]]
    
    curr_close_price_seq = []
    for Date_idx in range(len(Date)):
        try:
#            print("try {}_{}".format(ID_idx, Date[Date_idx]))
#            print(curr_ID_data[Date[Date_idx]])
            curr_close_price = curr_ID_data[Date[Date_idx]][3]
#            print(curr_close_price)
        except:
#            print("except {}_{}".format(ID_idx, Date[Date_idx]))
            curr_close_price = 0
        
        curr_close_price_seq.append(curr_close_price)            

#    print("member_ID[{}] = {}".format(ID_idx, member_ID[ID_idx]))
#    print(curr_close_price_seq)
            
    curr_close_price_seq = np.array(curr_close_price_seq)
    
    curr_SMA_seq = talib.MA(curr_close_price_seq, 30, matype=0)
    curr_EMA_seq = talib.MA(curr_close_price_seq, 30, matype=1)
    curr_WMA_seq = talib.MA(curr_close_price_seq, 30, matype=2)
    curr_DEMA_seq = talib.MA(curr_close_price_seq, 30, matype=3)
    curr_TEMA_seq = talib.MA(curr_close_price_seq, 30, matype=4)
    
    curr_ID_df = pd.DataFrame(index=[member_ID[ID_idx]], columns=Date)
    for Date_idx in range(len(Date)):
        curr_ID_df[Date[Date_idx]] = [[ curr_SMA_seq[Date_idx], 
                                        curr_EMA_seq[Date_idx], 
                                        curr_WMA_seq[Date_idx], 
                                        curr_DEMA_seq[Date_idx], 
                                        curr_TEMA_seq[Date_idx]]]

    output_df = pd.concat([output_df, curr_ID_df], axis=0)               
    ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))

feature_list = ["SMA_30", "EMA_30", "WMA_30", "DEMA_30", "TEMA_30"]

print("Dumping data ...")    
f = open('./Data/ta_feature.pkl', 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(feature_list, f, True)  
pickle.dump(output_df, f, True)  
f.close()  
    
print("========== TA Preprocess Done! ==========")    
    