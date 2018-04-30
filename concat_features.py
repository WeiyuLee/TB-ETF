# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:37:05 2018

@author: Weiyu_Lee
"""

import numpy as np
import pandas as pd 
import pickle

def concat_features(org_data, features, Date, member_ID):
    for ID_idx in range(len(member_ID)):
        curr_ID_data = org_data.loc[member_ID[ID_idx]]
        curr_ID_features = features.loc[member_ID[ID_idx]]
        
        for Date_idx in range(len(Date)):
            curr_ID_date_data = curr_ID_data[Date[Date_idx]]
            curr_ID_date_features = curr_ID_features[Date[Date_idx]]
            try:
                curr_ID_date_data.extend(curr_ID_date_features)
            except:
                curr_ID_date_data = [curr_ID_date_data]    
                curr_ID_date_data.extend(curr_ID_date_features)           
            
    return org_data            

print("========== Combining Features Process Start ==========")

feature_list = []

### Read orginal data
print("Loading ./Data/all_data.pkl...")
f = open('./Data/all_data.pkl', 'rb')  
tasharep_ID = pickle.load(f)
member_ID = pickle.load(f)
Date = pickle.load(f)
curr_feature_list = pickle.load(f)
scale_factor = pickle.load(f)
org_data = pickle.load(f)

feature_list.extend(curr_feature_list)

### Read TA features
print("Loading ./Data/ta_feature.pkl...")
f = open('./Data/ta_feature.pkl', 'rb')  
tasharep_ID = pickle.load(f)
member_ID = pickle.load(f)
Date = pickle.load(f)
curr_feature_list = pickle.load(f)
ta_data = pickle.load(f)

feature_list.extend(curr_feature_list)

output_df = concat_features(org_data, ta_data, Date, member_ID)

print("Dumping data ...")    
f = open('./Data/all_feature.pkl', 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(feature_list, f, True)  
pickle.dump(scale_factor, f, True)  
pickle.dump(output_df, f, True)  
f.close()  

print("========== Combining Features Process Done ==========")
