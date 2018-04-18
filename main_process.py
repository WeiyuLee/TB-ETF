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

member_data = pd.read_csv('./Data/0050_ratio.csv') 
member_ID = member_data["ID"].astype(str)

print('original tasharep: ',tasharep.shape)
print('original taetfp: ',taetfp.shape)

tasharep.ID = tasharep.ID.astype(str)
tasharep.Date = tasharep.Date.astype(str)
taetfp.ID = taetfp.ID.astype(str)
taetfp.Date = taetfp.Date.astype(str)

tasharep_ID = tasharep.ID.unique()
taetfp_ID = taetfp.ID.unique()

Date = tasharep.Date.unique()

tasharep_ID_group = tasharep.groupby("ID")
taetfp_ID_group = taetfp.groupby("ID")

all_data_dict = {}

for ID_idx in range(len(tasharep_ID)):
    idx = tasharep_ID_group.groups[tasharep_ID[ID_idx]]

    curr_ID_data = tasharep.iloc[idx]
    curr_ID_data.index = curr_ID_data.Date
    
    all_data_dict[tasharep_ID[ID_idx]] = curr_ID_data

output_df = pd.DataFrame()
for ID_idx in range(len(member_ID)):
    curr_id_data = all_data_dict[member_ID[ID_idx]]    

    curr_id_df = pd.DataFrame(index=[member_ID[ID_idx]], columns=Date)
    for Date_idx in range(len(Date)):         
        if (curr_id_data.index == Date[Date_idx]).sum() > 0:
            curr_features = curr_id_data.loc[Date[Date_idx]]
            curr_id_df[Date[Date_idx]] = [curr_features]
    
    output_df = pd.concat([output_df, curr_id_df], axis=0)       
    print("{}/{}".format(ID_idx, len(member_ID)))

print("Dumping data ...")    
f = open('./Data/all_data.pkl', 'wb')
#pickle.dump(all_data_dict, f, True)  
pickle.dump(tasharep_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(output_df, f, True)  
f.close()  
    
print("========== Preprocess Done! ==========")