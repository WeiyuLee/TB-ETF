# -*- coding: utf-8 -*-
"""
Created on Tue May 15 14:51:59 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import datetime
from tqdm import tqdm

import nm_features as nm
import config as conf

def change_raw_columns_name(inputfile:pd.DataFrame):
    
    inputfile.columns = ["Date", "exch_USD/NT", "exch_CNY/NT", "exch_EUR/USD", "exch_USD/JPY", "exch_GBP/USD", "exch_AUD/USD", "exch_USD/HKD", "exch_USD/CNY", "exch_USD/ZAR", "exch_NZD/USD"]

print("========== Exchange Rate Data Preprocess Start ==========")

EXCH_conf = conf.config('feature_conf').config['EXCH']

exchange_rate = pd.read_csv('./Data/total_exchange_rate.csv')
change_raw_columns_name(exchange_rate)

Date = exchange_rate["Date"]
Date_pbar = tqdm(range(len(Date)))
for Date_idx in Date_pbar:
    curr_date = datetime.datetime.strptime(Date[Date_idx], '%Y/%m/%d')
    Date[Date_idx] = curr_date.strftime("%Y%m%d")

# Use Date as index    
exchange_rate.index = exchange_rate["Date"]
exchange_rate = exchange_rate.drop(columns="Date")

# Drop the non-fullfill data
exchange_rate = exchange_rate.drop(columns="exch_CNY/NT")
exchange_rate = exchange_rate.drop(columns="exch_USD/CNY")
exchange_rate = exchange_rate.drop(columns="exch_USD/ZAR")
exchange_rate = exchange_rate.drop(columns="exch_NZD/USD")

# Scale the features
if EXCH_conf["Nm"] is True:
    Nm_conf = conf.config('feature_conf').config['Nm']
    Nm_method = Nm_conf["method"]    
    feature_list = exchange_rate.columns.tolist()
    for f in feature_list:
        curr_feature = exchange_rate[f]
        exchange_rate[f], _ = nm.nm_scale_data(curr_feature, method=Nm_method, is1D=True)    
    file_postfix = "_Nm"
else:
    file_postfix = "_woNm"

exchange_rate.to_pickle("./Data/exchange_rate_data" + file_postfix + ".pkl")

print("========== Exchange Rate Data Preprocess Done ==========")