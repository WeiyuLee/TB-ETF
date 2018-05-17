# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:58:57 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from tqdm import tqdm

import config as conf
import pattern_features as pa
import ta_features as ta
import ud_features as ud
import lt_features as lt
import nm_features as nm

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

###############################################################################
### Normalize the all the stock data before ta_preprocess
Nm_conf = conf.config('feature_conf').config['Nm']
if Nm_conf["enable"] is True and Nm_conf["type"] == [0]:
    Nm_method = Nm_conf["method"]
    tmp_nor_price, price_scaler = nm.nm_scale_data(np.array(tasharep[["open_price", "max", "min", "close_price"]]), Nm_method, is1D=True)
    tasharep[["open_price", "max", "min", "close_price"]] = tmp_nor_price
    tmp_nor_trade, trade_scaler = nm.nm_scale_data(np.array(tasharep["trade"]), Nm_method, is1D=True)
    tasharep["trade"] = tmp_nor_trade
###############################################################################    

### Slice the data by IDs, and make a dict.  
all_data_dict = {}
for ID_idx in range(len(tasharep_ID)):
    idx = tasharep_ID_group.groups[tasharep_ID[ID_idx]]

    curr_ID_data = tasharep.iloc[idx]   
    curr_ID_data.index = curr_ID_data.Date
    
    all_data_dict[tasharep_ID[ID_idx]] = curr_ID_data

print("========== Making Dataframe ==========")    
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
    output_df, ta_feature_list = ta.ta_preprocess(member_ID, Date, output_df)
    feature_list.extend(ta_feature_list)

    ### Drop nan values
    print("Cleaning data...")
    time_period = max(conf.config('feature_conf').config['MA']["timeperiod"])
    output_df = output_df.drop(output_df.columns[0:(time_period-1)*6], axis=1)
    Date = output_df.columns.values.tolist()

### Calculate Pattern features
PATTERN_conf = conf.config('feature_conf').config['PATTERN']
if PATTERN_conf["enable"] is True:
    output_df, pattern_feature_list = pa.pattern_preprocess(member_ID, Date, output_df)
    feature_list.extend(pattern_feature_list)

### Calculate LT features
LT_conf = conf.config('feature_conf').config['LT']
if LT_conf["enable"] is True:
    output_df, lt_feature_list = lt.lt_preprocess(member_ID, Date, output_df)
    feature_list.extend(lt_feature_list)

### Concat exchange rate
EXCH_conf = conf.config('feature_conf').config['EXCH']
if EXCH_conf["enable"] is True:
    print("========== Concat Exchange Rate Data ==========")
    exch_data = pd.read_pickle(EXCH_conf["file_path"])
    ID_pbar = tqdm(range(len(member_ID)))
    for ID_idx in ID_pbar:
        for Date_idx in range(len(Date)):       
            curr_date_stock_data = output_df.loc[member_ID[ID_idx]][Date[Date_idx]]
            output_df.loc[member_ID[ID_idx]][Date[Date_idx]] = np.append(curr_date_stock_data, exch_data.loc[Date[Date_idx]])
    feature_list.extend(exch_data.columns.tolist())

### Concat The Weighted Price Index of the Taiwan Stock Exchange
TAIEX_conf = conf.config('feature_conf').config['TAIEX']
if TAIEX_conf["enable"] is True:
    print("========== Concat TAIEX Data ==========")
    taiex_data = pd.read_pickle(TAIEX_conf["file_path"])
    ID_pbar = tqdm(range(len(member_ID)))
    for ID_idx in ID_pbar:
        for Date_idx in range(len(Date)):       
            curr_date_stock_data = output_df.loc[member_ID[ID_idx]][Date[Date_idx]]
            output_df.loc[member_ID[ID_idx]][Date[Date_idx]] = np.append(curr_date_stock_data, taiex_data.loc[Date[Date_idx]])
    feature_list.extend(taiex_data.columns.tolist())
    
### Concat other stocks' features
STOCKS_conf = conf.config('feature_conf').config['STOCKS']
if STOCKS_conf["enable"] is True:
    print("========== Concat Other Stocks Data ==========")
    stock_list = STOCKS_conf["stocks"]
    curr_target_TS = get_stock_time_series(output_df, "0050")
    unit_f_list = ['open_price', 'max', 'min', 'close_price', 'trade']
    
    for ID in stock_list:
        curr_member_TS = get_stock_time_series(output_df, ID)        
        curr_target_TS = np.append(curr_target_TS, curr_member_TS[:, 0:5], axis=1)
            
        for f_list in unit_f_list:
            feature_list.append(ID + "_" + f_list)
            
    output_df = set_stock_time_series(output_df, "0050", curr_target_TS)

#### Add Test data
#Fs = 800
#f = 5
#sample = len(Date)
#x = np.arange(sample)
#y = np.sin(2 * np.pi * f * x / Fs)    
#curr_test_df = pd.DataFrame(index=["0000"], columns=Date)
#for Date_idx in range(len(Date)):     
#    curr_test_df[Date[Date_idx]] = [[y[Date_idx], y[Date_idx], y[Date_idx], y[Date_idx], y[Date_idx]]]
#
#output_df = pd.concat([output_df, curr_test_df], axis=0)           
#member_ID = member_ID.append(pd.Series(["0000"]))
#member_ID = member_ID.reset_index()
#member_ID = member_ID.drop(columns="index")
#member_ID = member_ID.squeeze()

### Calculate UD features
UD_conf = conf.config('feature_conf').config['UD']
if UD_conf["enable"] is True:
    output_df, ud_feature_list = ud.ud_preprocess(member_ID, Date, output_df)
    feature_list.extend(ud_feature_list)

###############################################################################
### Normalize the data after ta_preprocess
Nm_conf = conf.config('feature_conf').config['Nm']
if Nm_conf["enable"] is True and Nm_conf["type"] == [1]:
    Nm_method = Nm_conf["method"]
    ID_pbar = tqdm(range(len(member_ID)))
    for ID_idx in ID_pbar:
        curr_stock_TS = get_stock_time_series(output_df, member_ID[ID_idx])
        
        curr_stock_TS, scaler = nm.nm_preprocess(curr_stock_TS, feature_list)
        
        if member_ID[ID_idx] == "0050":
            price_scaler = scaler["price"]
            trade_scaler = scaler["trade"]
               
        output_df = set_stock_time_series(output_df, member_ID[ID_idx], curr_stock_TS)
###############################################################################
        
### Plot data
curr_TS = get_stock_time_series(output_df, "0050")
curr_UD_shift = curr_TS[:, -3:]
curr_UD_shift = np.delete(curr_UD_shift, 0, axis=0)
curr_TS[:, -3:] = np.insert(curr_UD_shift, -1, curr_UD_shift[-1,:], axis=0)

tmp_df = pd.DataFrame(curr_TS)
tmp_corr_mat = np.abs(tmp_df.corr())
tmp_corr_mat.index = feature_list
tmp_corr_mat.columns = feature_list

plt.plot(curr_TS[100:200,3])
plt.plot(curr_TS[100:200,81])
plt.plot(curr_TS[100:200,82])
#plt.plot(curr_TS[100:200,82])
#plt.plot(curr_TS[100:200,83])
#plt.plot(curr_TS[100:200,4])
#plt.plot(curr_TS[100:200,85]/5)

#fake_list = ["sine_value", "sine_value", "sine_value", "sine_value", "sine_value", "UD_0", "UD_1", "UD_2"]
#feature_list = fake_list

### Dump Data   
print("Dumping data ...")    
if Nm_conf["enable"] is True:
    file_postfix = '_Nm_' + str(Nm_conf["type"][0]) + '_' + Nm_method + '_' + str(len(feature_list)) + '.pkl'
else:
    file_postfix = "_" + str(len(feature_list)) + '.pkl'
f = open('./Data/all_meta_data' + file_postfix, 'wb')
pickle.dump(tasharep_ID, f, True)  
pickle.dump(member_ID, f, True)  
pickle.dump(Date, f, True)  
pickle.dump(feature_list, f, True)  
if Nm_conf["enable"] is True:   
    pickle.dump(price_scaler, f, True)
    pickle.dump(trade_scaler, f, True)   
else:
    pickle.dump(["404"], f, True)
    pickle.dump(["404"], f, True)    
f.close()  

output_df.to_pickle('./Data/all_feature_data' + file_postfix)  
   
print("========== Preprocess Done! ==========")