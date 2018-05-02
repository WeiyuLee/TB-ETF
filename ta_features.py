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

## Parameters
time_period = 30

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
           
    curr_close_price_seq = np.array(curr_close_price_seq)
    
    curr_SMA_seq = talib.MA(curr_close_price_seq, time_period, matype=0)
    curr_EMA_seq = talib.MA(curr_close_price_seq, time_period, matype=1)
    curr_WMA_seq = talib.MA(curr_close_price_seq, time_period, matype=2)
    curr_DEMA_seq = talib.MA(curr_close_price_seq, time_period, matype=3)
    curr_TEMA_seq = talib.MA(curr_close_price_seq, time_period, matype=4)
    
    curr_ID_df = pd.DataFrame(index=[member_ID[ID_idx]], columns=Date)
    for Date_idx in range(len(Date)):
        curr_ID_df[Date[Date_idx]] = [[ curr_SMA_seq[Date_idx], 
                                        curr_EMA_seq[Date_idx], 
                                        curr_WMA_seq[Date_idx], 
                                        curr_DEMA_seq[Date_idx], 
                                        curr_TEMA_seq[Date_idx]]]

    output_df = pd.concat([output_df, curr_ID_df], axis=0)               
    ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))

### Drop nan values
#output_df = output_df.drop(output_df.columns[0:(time_period-1)*3], axis=1)
#Date = output_df.columns.values.tolist()

### Checking for nan values
### Check 20130102 is NaN 
#NaN_ID_list = []
#print("Checking NaN values...")
#for ID_idx in ID_pbar:
#    curr_ID_data = org_data.loc[member_ID[ID_idx]]
#    temp = curr_ID_data["20130102"]
#    
#    if np.isnan(temp).any() == True:
##        print("[ID] = [{}]".format(member_ID[ID_idx]))
#        NaN_ID_list.append(member_ID[ID_idx])
#        
#print("NaN count = [{}]".format(NaN_ID_list.count))        
#
#temp_df = output_df.drop(NaN_ID_list, axis=0)
#temp_ID = temp_df.index
#temp_Date = output_df.columns
#
### Check island NaN
#nan_count = 0
#for ID_idx in range(len(temp_ID)):
#    curr_ID_data = temp_df.loc[temp_ID[ID_idx]]
#    
#    for Date_idx in range(len(temp_Date)):
#        curr_ID_Date_data = curr_ID_data[temp_Date[Date_idx]]
#        num_of_nan = np.isnan(curr_ID_Date_data).sum()
#        
#        if num_of_nan > 0:
#            print("[ID, Date] = [{}, {}]".format(temp_ID[ID_idx], temp_Date[Date_idx]))
#            print(org_data.loc[temp_ID[ID_idx]])
#            break           

feature_list = ["SMA_30", "EMA_30", "WMA_30", "DEMA_30", "TEMA_30"]

print("Dumping data ...")    
f = open('./Data/ta_meta_data.pkl', 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(time_period, f, True)  
pickle.dump(feature_list, f, True)  
f.close()  

output_df.to_pickle("./Data/ta_feature_data.pkl")
    
print("========== TA Preprocess Done! ==========")    
    