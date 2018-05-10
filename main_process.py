# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:58:57 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

import config as conf
import ta_features as ta
import ud_features as ud

from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

def change_raw_columns_name(inputfile:pd.DataFrame):
    
    inputfile.columns = ["ID", "Date", "name", "open_price", "max", "min", "close_price", "trade"]

def get_stock_time_series(data_df, stock_id):
    
    curr_ID_data = data_df.loc[stock_id]

    output = np.array(curr_ID_data[0])
    for i in range(1, len(curr_ID_data.index)):
        output = np.vstack((output, curr_ID_data[i]))
        
    return output    

def set_stock_time_series(data_df, stock_id, input_TS):
    
    for i in range(len(data_df.loc[stock_id].index)):
        data_df.loc[stock_id][i] = input_TS[i, :]
        
    return data_df    

def scale_data(data, is1D=False):
    
    dim = data.shape

    if is1D is True:
        data = data.reshape(-1, 1)
        
    N = StandardScaler()
    scaled_data = N.fit_transform(data)

    if len(dim) > 1:
        scaled_data = scaled_data.reshape(dim[0], dim[1])
    else:
        scaled_data = scaled_data.reshape(-1)
        
    return scaled_data, N
    
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

tasharep["ID"] = tasharep["ID"].astype(str)
tasharep["ID"] = tasharep["ID"].str.strip()

tasharep["Date"] = tasharep["Date"].astype(str)
tasharep["Date"] = tasharep["Date"].str.strip()

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
member_data = pd.read_csv('./Data/0050_ratio.csv', dtype=str) 
member_ID = member_data["ID"].astype(str)
member_ID = member_ID.str.strip()
#member_ID = tasharep_ID

### Normalize the data before ta_preprocess
Nm_conf = conf.config('feature_conf').config['Nm']
if Nm_conf["enable"] is True and Nm_conf["type"] == [0]:
    print("Scaling data (before) ...")
    tmp_nor_price, price_scaler = scale_data(np.array(tasharep[["open_price", "max", "min", "close_price"]]), is1D=True)
    tasharep[["open_price", "max", "min", "close_price"]] = tmp_nor_price
    tmp_nor_trade, trade_scaler = scale_data(np.array(tasharep["trade"]), is1D=True)
    tasharep["trade"] = tmp_nor_trade
    
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
            curr_ID_df[Date[Date_idx]] = [[np.NAN, np.NAN, np.NAN, np.NAN, np.NAN]]
            #curr_ID_df[Date[Date_idx]] = [[0, 0, 0, 0, 0]]
        
    output_df = pd.concat([output_df, curr_ID_df], axis=0)       
    ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))

feature_list = ['open_price', 'max', 'min', 'close_price', 'trade']

### Calculate TA features
TA_conf = conf.config('feature_conf').config['TA']
if TA_conf["enable"] is True:
    output_df, ta_feature_list = ta.ta_preprocess(tasharep_ID, member_ID, Date, output_df)
    feature_list.extend(ta_feature_list)

### Calculate UD features
UD_conf = conf.config('feature_conf').config['UD']
if UD_conf["enable"] is True:
    output_df, ud_feature_list = ud.ud_preprocess(tasharep_ID, member_ID, Date, output_df)
    feature_list.extend(ud_feature_list)

### Drop nan values
print("Cleaning data...")
time_period = max(conf.config('feature_conf').config['MA']["timeperiod"])
output_df = output_df.drop(output_df.columns[0:(time_period-1)*6], axis=1)
Date = output_df.columns.values.tolist()

### Normalize the data after ta_preprocess
Nm_conf = conf.config('feature_conf').config['Nm']
if Nm_conf["enable"] is True and Nm_conf["type"] == [1]:
    print("Scaling data (after) ...")
    ID_pbar = tqdm(range(len(member_ID)))
    for ID_idx in ID_pbar:
        curr_stock_TS = get_stock_time_series(output_df, member_ID[ID_idx])
        
        # scale price
        curr_stock_TS[:, 0:4], price_scaler = scale_data(curr_stock_TS[:, 0:4], is1D=True)
        # scale trade
        curr_stock_TS[:, 4], trade_scaler = scale_data(curr_stock_TS[:, 4], is1D=True)
        # scale ta features
        curr_stock_TS[:, 5:-4], ta_scaler = scale_data(curr_stock_TS[:, 5:-4], is1D=False)
        
        output_df = set_stock_time_series(output_df, member_ID[ID_idx], curr_stock_TS)
        
### Plot data
curr_TS = get_stock_time_series(output_df, "0050")
plt.plot(curr_TS[0:100,3])
plt.plot(curr_TS[0:100,6])
plt.plot(curr_TS[0:100,7])
plt.plot(curr_TS[0:100,8])

### Dump Data   
print("Dumping data ...")    
f = open('./Data/all_meta_data.pkl', 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(feature_list, f, True)  
if Nm_conf["enable"] is True:   
    pickle.dump(price_scaler, f, True)
    pickle.dump(trade_scaler, f, True)   
f.close()  

output_df.to_pickle('./Data/all_feature_data.pkl')  
   
print("========== Preprocess Done! ==========")