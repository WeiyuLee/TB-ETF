# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:01:21 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import config as conf

def get_stock_time_series(data_df, stock_id):
    
    curr_ID_data = data_df.loc[stock_id]

    output = np.array(curr_ID_data[0])
    for i in range(1, len(curr_ID_data.index)):
        output = np.vstack((output, curr_ID_data[i]))
        
    return output    

ID_conf = conf.config('feature_conf').config['ID']
#ETF_ID = ID_conf["ID"]
#ETF_ID_list = ["0050"]
ETF_ID_list = ["0050", "0052", "0053", "0054", "0055", "0056", "0057", "0058", "0059", 
               "006201", "006203", "006204", "006208"]

output_date = {}
for ETF_ID in ETF_ID_list:
    Nm_conf = conf.config('feature_conf').config['Nm']
    if Nm_conf["enable"] is True:
        Nm_method = Nm_conf["method"]
        file_postfix = '_Nm_' + str(Nm_conf["type"][0]) + '_' + Nm_method + '_' + str(94) + "_" + ETF_ID + '.pkl'
    else:
        file_postfix = "_" + str(94) + '.pkl'
    
    src_file_path = './Data/all_feature_data' + file_postfix
    meta_file_path = './Data/all_meta_data' + file_postfix
    
    data = pd.read_pickle(src_file_path)
    
    f = open(meta_file_path, "rb")
    tasharep_ID = pickle.load(f)
    member_ID = pickle.load(f)
    Date = pickle.load(f)
    feature_list = pickle.load(f)
    price_scaler = pickle.load(f)
    trade_scaler = pickle.load(f)
    
    f_idx = 59 # MACD
    
    src_time_period = ['20000101', '20180511']
#    eval_time_period = ['20180511', '20180518']
    eval_time_period = ['20180402', '20180518']
    eval_time_len = Date.index(eval_time_period[1]) - Date.index(eval_time_period[0]) + 1
    
    total_acc = 0
    for day_shift in range(eval_time_len-5):
    
        eval_start_date = Date.index(eval_time_period[0]) + day_shift
        target_start_date = eval_start_date - 21
        
        target_time_period = [Date[target_start_date], Date[eval_start_date]]
        next_time_period = [Date[eval_start_date], Date[eval_start_date + 5]]       
            
        date_mask = (data.columns > src_time_period[0]) & (data.columns <= src_time_period[1])
        src_data = data.iloc[:, date_mask]
        
        date_mask = (data.columns > target_time_period[0]) & (data.columns <= target_time_period[1])
        target_data = data.iloc[:, date_mask]
        
        date_mask = (data.columns > next_time_period[0]) & (data.columns <= next_time_period[1])
        next_data = data.iloc[:, date_mask]
        
        src_TS = get_stock_time_series(src_data, ETF_ID)
        target_TS = get_stock_time_series(target_data, ETF_ID)
        next_TS = get_stock_time_series(next_data, ETF_ID)
        overall_TS = get_stock_time_series(data, ETF_ID)
        
        target_xcorr = np.correlate(src_TS[:, f_idx], target_TS[:, f_idx], mode='valid')
#        next_xcorr = np.correlate(src_TS[:, f_idx], next_TS[:, f_idx], mode='valid')
        
        target_len = len(target_TS)
        max_target_xcorr_idx = target_xcorr.argsort()[::-1]
        predict_target_idx = max_target_xcorr_idx + target_len
        
        next_len = len(next_TS)
        max_next_xcorr_idx = next_xcorr.argsort()[::-1]
        
    #    plt.plot(target_xcorr)
    #    plt.savefig("target_xcorr_{}.png".format(ETF_ID))
        
        #for idx in max_target_xcorr_idx[:10]:
        #    plt.figure()
        #    plt.plot(target_TS[:, 84])
        #    plt.plot(src_TS[max_target_xcorr_idx[idx]:max_target_xcorr_idx[idx]+target_len, 84])
        
        #plt.figure()
        #plt.plot(target_xcorr)
        #plt.plot(next_xcorr)
        
        top_num = 10
        acc = []
        label = np.argmax(next_TS[:, -3:], axis=-1)
        for idx in max_target_xcorr_idx[:top_num]:
            predict = np.argmax(overall_TS[predict_target_idx[idx]:predict_target_idx[idx]+next_len, -3:], axis=-1)
            acc.append(sum(label == predict) / next_len)
            
        max_acc_idx = np.argsort(acc)[::-1]
        output_xcorr_idx = [max_target_xcorr_idx[acc_idx] for acc_idx in max_acc_idx]
    
        top_num = 3
        avg_acc = 0
        acc = []
        for idx in output_xcorr_idx[:top_num]:
            #plt.figure()
            #plt.plot(next_TS[:, 84])
            #plt.plot(overall_TS[predict_target_idx[idx]:predict_target_idx[idx]+next_len, 84])   
            #plt.figure()
            #plt.plot(overall_TS[predict_target_idx[idx]:predict_target_idx[idx]+next_len, 3])
            
            predict = np.argmax(overall_TS[predict_target_idx[idx]:predict_target_idx[idx]+next_len, -3:], axis=-1)
            acc.append(sum(label == predict) / next_len)
            
            avg_acc = avg_acc + acc[-1]
            #print("Acc.: [{}]".format(acc[-1]))
            
        print("Avg. Acc.: [{}]".format(avg_acc/top_num))
    
        total_acc = total_acc + avg_acc/top_num
    
    print("[{}] Overall Acc.: [{}]".format(ETF_ID, total_acc/(eval_time_len-5)))
    output_date[ETF_ID] = [Date[i] for i in output_xcorr_idx[:10]]

f = open('./Data/xcorr_date_data.pkl', 'wb')
pickle.dump(output_date, f, True)  
f.close()




