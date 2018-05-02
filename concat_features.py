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
print("Loading ./Data/org_meta_data.pkl...")
f = open('./Data/org_meta_data.pkl', 'rb')  
tasharep_ID = pickle.load(f)
member_ID = pickle.load(f)
Date = pickle.load(f)
curr_feature_list = pickle.load(f)
scale_factor = pickle.load(f)
f.close()

print("Loading ./Data/org_feature_data.pkl...")
org_data = pd.read_pickle('./Data/org_feature_data.pkl')

feature_list.extend(curr_feature_list)

### Read TA features
print("Loading ./Data/ta_meta_data.pkl...")
f = open('./Data/ta_meta_data.pkl', 'rb')  
tasharep_ID = pickle.load(f)
member_ID = pickle.load(f)
Date = pickle.load(f)
time_period = pickle.load(f)
curr_feature_list = pickle.load(f)
f.close()

print("Loading ./Data/ta_feature_data.pkl...")
ta_data = pd.read_pickle("./Data/ta_feature_data.pkl")

feature_list.extend(curr_feature_list)

### Read UD features
print("Loading ./Data/ud_meta_data.pkl...")
f = open('./Data/ud_meta_data.pkl', 'rb')  
tasharep_ID = pickle.load(f)
member_ID = pickle.load(f)
Date = pickle.load(f)
curr_feature_list = pickle.load(f)
f.close()

print("Loading ./Data/ud_feature_data.pkl...")
ud_data = pd.read_pickle("./Data/ud_feature_data.pkl")

feature_list.extend(curr_feature_list)

print("Combining data...")
output_df = concat_features(org_data, ta_data, Date, member_ID)
output_df = concat_features(output_df, ud_data, Date, member_ID)

print("Cleaning data...")
## Drop nan values
output_df = output_df.drop(output_df.columns[0:(time_period-1)*3], axis=1)
Date = output_df.columns.values.tolist()

print("Dumping data ...")    
f = open('./Data/all_mata_data.pkl', 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(feature_list, f, True)  
pickle.dump(scale_factor, f, True)  
f.close()  

output_df.to_pickle("./Data/all_feature_data.pkl")  

print("========== Combining Features Process Done ==========")
