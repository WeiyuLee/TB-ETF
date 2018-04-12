# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:58:57 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import pickle

print("========== Preprocess Start ==========")

### Import data
tasharep = pd.read_csv('./Data/UTF-8/tasharep.csv') # training data
taetfp = pd.read_csv('./Data/UTF-8/taetfp.csv') # training data

print('original tasharep: ',tasharep.shape)
print('original taetfp: ',taetfp.shape)

tasharep_ID = tasharep.ID.unique()
taetfp_ID = taetfp.ID.unique()

Date = tasharep.Date.unique()

tasharep_date_group = tasharep.groupby("Date")
taetfp_date_group = taetfp.groupby("Date")

all_data_dict = {}

for date_idx in range(len(Date)):
    idx = tasharep_date_group.groups[Date[date_idx]]

    valid_data = tasharep.ix[idx]
    
    curr_data = pd.DataFrame(columns=["ID"])
    curr_data["ID"] = tasharep_ID

    curr_data = pd.merge(valid_data, curr_data, how="outer", on="ID")
    curr_data = curr_data.sort_values("ID")
    curr_data["Date"] = Date[date_idx]
    
    all_data_dict[Date[date_idx]] = curr_data

print("Dumping data ...")    
f = open('./Data/all_data.pkl', 'wb')
pickle.dump(all_data_dict, f, True)  
pickle.dump(tasharep_ID, f, True)  
pickle.dump(Date, f, True)  
f.close()  
    
print("========== Preprocess Done! ==========")