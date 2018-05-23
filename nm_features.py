# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:25:09 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd

import config as conf

from sklearn import preprocessing

def nm_transfer_to_ratio(data):
    
    data = data.reshape(-1, 1)
    
    data_shift = data.copy()
    data_shift = np.insert(data_shift, 0, data_shift[0])
    data_shift = np.delete(data_shift, -1)
    data_shift = data_shift.reshape(-1, 1)
    
    # data_ratio = t / (t - 1)
    data_ratio = (data / data_shift) - 1
    
    #data_ratio = data_ratio.reshape(-1)
    
    return data_ratio

def nm_scale_data(data, method="Standard", is1D=False):
    
    dim = data.shape

    if is1D is True:
        data = data.reshape(-1, 1)
    
    if method is "Standard":        
        N = preprocessing.StandardScaler()
    elif method is "MinMax":        
        N = preprocessing.MinMaxScaler()

    isnan = np.isnan(data).any()
    if isnan == True:
        nan_idx =  np.argwhere(np.isnan(data))
        start_idx = nan_idx[-1][0] + 1
        
        # If all the data is NaN, return NaN without scaling.
        if start_idx == len(data):
            scaled_data = data
        else:
            non_nan_data = data[start_idx:]
            scaled_data = N.fit_transform(non_nan_data)
            scaled_data = np.append(data[:start_idx], scaled_data) 
    else:
        scaled_data = N.fit_transform(data)

    if len(dim) > 1:
        scaled_data = scaled_data.reshape(dim[0], dim[1])
    else:
        scaled_data = scaled_data.reshape(-1)
        
    return scaled_data, N

def nm_preprocess(curr_stock_TS, feature_list):
    Nm_conf = conf.config('feature_conf').config['Nm']
    
    print("\nScaling all the data ... ratio: [{}], type: [{}], method: [{}]".format(Nm_conf["ratio_enable"], Nm_conf["type"], Nm_conf["method"]))
    
    if Nm_conf["ratio_enable"] is True:
        for f_idx in range(5):        
            # avoid divide zero
            zero_idx = np.where(curr_stock_TS[:, f_idx] == 0)[0]
            if len(zero_idx) > 0:
                curr_stock_TS[:, f_idx][zero_idx] = 1
                            
            # Add ratio features 
            curr_ratio = nm_transfer_to_ratio(curr_stock_TS[:, f_idx])
            curr_stock_TS = np.append(curr_stock_TS, curr_ratio, axis=1)
    
    scaler = {}
    Nm_method = Nm_conf["method"]
    
    # Scale price
    curr_stock_TS[:, 0:4], price_scaler = nm_scale_data(curr_stock_TS[:, 0:4], method=Nm_method, is1D=True)
    scaler["price"] = price_scaler
    
    # Scale trade
    curr_stock_TS[:, 4], trade_scaler = nm_scale_data(curr_stock_TS[:, 4], method=Nm_method, is1D=True)
    scaler["trade"] = trade_scaler
    
    special_list = ["MACD", "KDJ", "ADOSC", "UD", "taiex", "exch", "pa"]
    
    TA_conf = conf.config('feature_conf').config['TA']
    if TA_conf["enable"] is True and TA_conf["Nm"] is True:
        
        # Scale ta_features with single column
        for curr_feature in feature_list[5:]:
            curr_type = curr_feature.split("_")[0]
            
            if curr_type in special_list:
                # Scale these features later
                continue
            else:
                f_idx = feature_list.index(curr_feature)
                curr_stock_TS[:, f_idx], tmp_scaler = nm_scale_data(curr_stock_TS[:, f_idx], method=Nm_method, is1D=True)
                scaler[curr_feature] = tmp_scaler
            
        # Scale single ta_features with multiple columns
        MACD_conf = conf.config('feature_conf').config['MACD']
        if MACD_conf["enable"] is True:            
            MACD_period_num = len(MACD_conf["period"])
        
            for i in range(MACD_period_num):
                curr_fast_period = MACD_conf["period"][i][0]
                curr_slow_period = MACD_conf["period"][i][1]
                curr_signal_period = MACD_conf["period"][i][2]
                
                curr_MACD_fast_str = "MACD_" + str(curr_fast_period) + "_" + str(curr_slow_period) + "_" + str(curr_signal_period) + "_fast"
                
                f_idx = feature_list.index(curr_MACD_fast_str)
                curr_stock_TS[:, f_idx:f_idx+3], tmp_scaler = nm_scale_data(curr_stock_TS[:, f_idx:f_idx+3], method=Nm_method, is1D=True)
                scaler[curr_MACD_fast_str] = tmp_scaler
                
        KDJ_conf = conf.config('feature_conf').config['KDJ']
        if KDJ_conf["enable"] is True:            
            KDJ_period_num = len(KDJ_conf["period"])
        
            for i in range(KDJ_period_num):
                curr_fastk_period = KDJ_conf["period"][i][0]
                curr_slowk_period = KDJ_conf["period"][i][1]
                curr_slowd_period = KDJ_conf["period"][i][2]
                
                curr_KDJ_slowk_str = "KDJ_" + str(curr_fastk_period) + "_" + str(curr_slowk_period) + "_" + str(curr_slowd_period) + "_slowk"
                
                f_idx = feature_list.index(curr_KDJ_slowk_str)
                curr_stock_TS[:, f_idx:f_idx+2], tmp_scaler = nm_scale_data(curr_stock_TS[:, f_idx:f_idx+2], method=Nm_method, is1D=True)            
                scaler[curr_KDJ_slowk_str] = tmp_scaler
                
        ADOSC_conf = conf.config('feature_conf').config['ADOSC']
        if ADOSC_conf["enable"] is True:            
            ADOSC_period_num = len(ADOSC_conf["period"])
        
            for i in range(ADOSC_period_num):
                curr_fast_period = ADOSC_conf["period"][i][0]
                curr_slow_period = ADOSC_conf["period"][i][1]
                
                curr_ADOSC_fast_str = "ADOSC_" + str(curr_fast_period) + "_" + str(curr_slow_period)
                
                f_idx = feature_list.index(curr_ADOSC_fast_str)
                curr_stock_TS[:, f_idx], tmp_scaler = nm_scale_data(curr_stock_TS[:, f_idx], method=Nm_method, is1D=True)                        
                scaler[curr_ADOSC_fast_str] = tmp_scaler

    PATTERN_conf = conf.config('feature_conf').config['PATTERN']
    if PATTERN_conf["enable"] is True and PATTERN_conf["Nm"] is True:                
        
        # Scale pattern features
        for curr_feature in feature_list[5:]:
            curr_type = curr_feature.split("_")[0]
            
            if curr_type is "pa":
                f_idx = feature_list.index(curr_feature)
                curr_stock_TS[:, f_idx], tmp_scaler = nm_scale_data(curr_stock_TS[:, f_idx], method=Nm_method, is1D=True)
                scaler[curr_feature] = tmp_scaler
                
    return curr_stock_TS, scaler
            
            
            
            
            
            
            
            
            
            
            
            
            