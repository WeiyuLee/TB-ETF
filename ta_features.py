# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:33:44 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import talib

import config as conf

from tqdm import tqdm

def ta_preprocess(tasharep_ID, member_ID, Date, org_data):
    
    print("========== TA Preprocess Start ==========")
    
    feature_list = []
    TA_conf = conf.config('feature_conf').config['TA']
    if TA_conf["enable"] is False:
        
        print("TA features are disabled.")
        
    else:
        ID_pbar = tqdm(range(len(member_ID)))
        for ID_idx in ID_pbar:
            curr_ID_data = org_data.loc[member_ID[ID_idx]]
            
            curr_close_price_seq = []
            for Date_idx in range(len(Date)):
                try:
                    curr_close_price = curr_ID_data[Date[Date_idx]][3]
                except:
                    curr_close_price = float(np.NAN)
                
                curr_close_price_seq.append(curr_close_price)            
                   
            curr_close_price_seq = np.array(curr_close_price_seq)
                       
            # Moving Average
            MA_conf = conf.config('feature_conf').config['MA']
            if MA_conf["enable"] is True:
                MA_seqs = []
                MA_Type_num = len(MA_conf["MA_Type"])
                timeperiod_num = len(MA_conf["timeperiod"])
                
                for i in range(MA_Type_num):
                    curr_MA_Type = MA_conf["MA_Type"][i]
                    
                    for j in range(timeperiod_num):                   
                        curr_timeperiod = MA_conf["timeperiod"][j]
                        
                        if ID_idx == 0:
                            feature_list.append("MA_" + str(curr_MA_Type) + "_" + str(curr_timeperiod))
                        
                        curr_MA_seq = talib.MA(curr_close_price_seq, curr_timeperiod, matype=curr_MA_Type)
                        MA_seqs.append(curr_MA_seq.copy())
            
            # Moving Average Convergence/Divergence    
            MACD_conf = conf.config('feature_conf').config['MACD']
            if MACD_conf["enable"] is True:        
                MACD_seqs = []
                period_num = len(MACD_conf["period"])
                
                for i in range(period_num):
                    curr_fast_period = MACD_conf["period"][i][0]
                    curr_slow_period = MACD_conf["period"][i][1]
                    curr_signal_period = MACD_conf["period"][i][2]
                    
                    if ID_idx == 0:
                        feature_list.append("MACD_" + str(curr_fast_period) + "_" + str(curr_slow_period) + "_" + str(curr_signal_period) + "_fast")
                        feature_list.append("MACD_" + str(curr_fast_period) + "_" + str(curr_slow_period) + "_" + str(curr_signal_period) + "_slow")
                        feature_list.append("MACD_" + str(curr_fast_period) + "_" + str(curr_slow_period) + "_" + str(curr_signal_period) + "_signal")
                    
                    curr_MACD, curr_signal, curr_hist = talib.MACD(curr_close_price_seq, 
                                                                   fastperiod=curr_fast_period, 
                                                                   slowperiod=curr_slow_period, 
                                                                   signalperiod=curr_signal_period)
                    MACD_seqs.append([curr_MACD.copy(), curr_signal.copy(), curr_hist.copy()])

            for Date_idx in range(len(Date)):
                temp_ta_features = []
                
                if MA_conf["enable"] is True:
                    for i in range(MA_Type_num*timeperiod_num):
                        temp_ta_features.append(MA_seqs[i][Date_idx])
    
                if MACD_conf["enable"] is True:
                    for i in range(period_num):
                        temp_ta_features.append(MACD_seqs[i][0][Date_idx])
                        temp_ta_features.append(MACD_seqs[i][1][Date_idx])
                        temp_ta_features.append(MACD_seqs[i][2][Date_idx])
                try:
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]].extend(temp_ta_features)                   
                except:
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]] = [org_data[Date[Date_idx]].loc[member_ID[ID_idx]]]
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]].extend(temp_ta_features)                       
                    
            ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))
        
    print("========== TA Preprocess Done! ==========")    

    return org_data, feature_list