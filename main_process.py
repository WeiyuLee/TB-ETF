# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:58:57 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import pickle

from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

def change_raw_columns_name(inputfile:pd.DataFrame):
    
    inputfile.columns = ["ID", "Date", "name", "open_price", "max", "min", "close_price", "trade"]
    
print("========== Preprocess Start ==========")

### Import original data as str
tasharep = pd.read_csv('./Data/tasharep.csv', encoding = "big5-hkscs", dtype=str) # training data
taetfp = pd.read_csv('./Data/taetfp.csv', encoding = "big5-hkscs", dtype=str) # training data

# Change the column names (titles)
change_raw_columns_name(tasharep)
change_raw_columns_name(taetfp)

print('original tasharep: ',tasharep.shape)
print('original taetfp: ',taetfp.shape)

# Merge all the data
tasharep = pd.concat([tasharep, taetfp], axis=0)
tasharep.reset_index(drop=True, inplace=True)
print('merged tasharep: ',tasharep.shape)

### Remove the unnecessary comma or space and transform to float
tasharep.ID = tasharep.ID.astype(str)
tasharep.Date = tasharep.Date.astype(str)

tasharep["open_price"] = tasharep["open_price"].astype(str)
tasharep["open_price"] = tasharep["open_price"].str.strip()
tasharep["open_price"] = tasharep["open_price"].str.replace(",", "")
tasharep["open_price"] = tasharep["open_price"].astype(float)

tasharep["max"] = tasharep["max"].astype(str)
tasharep["max"] = tasharep["max"].str.strip()
tasharep["max"] = tasharep["max"].str.replace(",", "")
tasharep["max"] = tasharep["max"].astype(float)

tasharep["min"] = tasharep["min"].astype(str)
tasharep["min"] = tasharep["min"].str.strip()
tasharep["min"] = tasharep["min"].str.replace(",", "")
tasharep["min"] = tasharep["min"].astype(float)

tasharep["close_price"] = tasharep["close_price"].astype(str)
tasharep["close_price"] = tasharep["close_price"].str.strip()
tasharep["close_price"] = tasharep["close_price"].str.replace(",", "")
tasharep["close_price"] = tasharep["close_price"].astype(float)

tasharep["trade"] = tasharep["trade"].astype(str)
tasharep["trade"] = tasharep["trade"].str.strip()
tasharep["trade"] = tasharep["trade"].str.replace(",", "")
tasharep["trade"] = tasharep["trade"].astype(float)

# Get the ID list
tasharep_ID = tasharep.ID.unique()

# Get the Date list
Date = tasharep.Date.unique()

# Group the data by IDs
tasharep_ID_group = tasharep.groupby("ID")

### Load target IDs
#member_data = pd.read_csv('./Data/0050_ratio.csv') 
#member_ID = member_data["ID"].astype(str)
member_ID = tasharep_ID

### Normalize the data
N = StandardScaler()
tmp_nor_price = N.fit_transform(tasharep[["open_price", "max", "min", "close_price"]].T)
tasharep[["open_price", "max", "min", "close_price"]] = tmp_nor_price.T
tmp_nor_trade = N.fit_transform(tasharep["trade"].reshape(1, -1))
tasharep["trade"] = tmp_nor_trade.reshape(-1)

### Slice the data by IDs, and make a dict.  
all_data_dict = {}
for ID_idx in range(len(tasharep_ID)):
    idx = tasharep_ID_group.groups[tasharep_ID[ID_idx]]

    curr_ID_data = tasharep.iloc[idx]   
    curr_ID_data.index = curr_ID_data.Date
    
    all_data_dict[tasharep_ID[ID_idx]] = curr_ID_data
    
### Make a output Dataframe    
ID_pbar = tqdm(range(len(member_ID)))
output_df = pd.DataFrame()
for ID_idx in ID_pbar:
    curr_ID_data = all_data_dict[member_ID[ID_idx]]    

    curr_ID_df = pd.DataFrame(index=[member_ID[ID_idx]], columns=Date)
    for Date_idx in range(len(Date)):         
        try:
            curr_features = curr_ID_data.loc[Date[Date_idx]]
            curr_ID_df[Date[Date_idx]] = [curr_features[3:].tolist()]
        except:
            continue
        
    output_df = pd.concat([output_df, curr_ID_df], axis=0)       
    ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))

feature_list = ['open_price', 'max', 'min', 'close_price', 'trade']

print("Dumping data ...")    
f = open('./Data/all_data.pkl', 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(feature_list, f, True)  
pickle.dump(N, f, True)
pickle.dump(output_df, f, True)  
f.close()  
    
print("========== Preprocess Done! ==========")