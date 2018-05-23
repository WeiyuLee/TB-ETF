# -*- coding: utf-8 -*-
"""
Created on Tue May 15 16:27:16 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
from tqdm import tqdm

import nm_features as nm
import config as conf

def change_raw_columns_name(inputfile:pd.DataFrame):
    
    inputfile.columns = ["Date", "taiex_open_price", "taiex_max_price", "taiex_min_price", "taiex_close_price"]

TAIEX_conf = conf.config('feature_conf').config['TAIEX']

taiex = pd.read_csv("./Data/total_weight_index.csv")
if len(taiex.columns) > 5:
    taiex = taiex.iloc[:,0:5]
change_raw_columns_name(taiex)

print("========== TAIEX Preprocess Start ==========")

Date = taiex["Date"]
Date_pbar = tqdm(range(len(Date)))
for Date_idx in Date_pbar:
    tmp_date = Date[Date_idx].strip(" ")
    tmp_date = tmp_date.split("/")
    Date[Date_idx] = str(int(tmp_date[0]) + 1911) + tmp_date[1] + tmp_date[2]

# Use Date as index    
taiex.index = taiex["Date"]
taiex = taiex.drop(columns="Date")

# Scale the features
if TAIEX_conf["Nm"] is True:   
    Nm_conf = conf.config('feature_conf').config['Nm']
    Nm_method = Nm_conf["method"]        
    feature_list = taiex.columns.tolist()
    taiex.iloc[:,:], _ = nm.nm_scale_data(taiex.values, method=Nm_method, is1D=True)    
    file_postfix = "_Nm"
else:
    file_postfix = "_woNm"

    
taiex.to_pickle("./Data/taiex_data" + file_postfix + ".pkl")

print("========== TAIEX Preprocess Done ==========")