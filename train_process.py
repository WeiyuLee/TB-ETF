# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 10:57:13 2018

@author: Weiyu_Lee
"""

### Waiting for LSTM model 

import numpy as np
import pandas as pd
import pickle

#f = open('./Data/all_data.pkl', 'rb')  
#all_data_dict = pickle.load(f)
#tasharep_ID = pickle.load(f)
#Date = pickle.load(f)
#
#member_data = pd.read_csv('./Data/0050_ratio.csv') 
#member_ID = member_data["ID"].astype(str)
#
#output_df = pd.DataFrame()
#for ID_idx in range(len(member_ID)):
#    curr_id_data = all_data_dict[member_ID[ID_idx]]    
#
#    curr_id_df = pd.DataFrame(index=[member_ID[ID_idx]], columns=Date)
#    for Date_idx in range(len(Date)):         
#        if (curr_id_data.index == Date[Date_idx]).sum() > 0:
#            curr_features = curr_id_data.loc[Date[Date_idx]]
#            curr_id_df[Date[Date_idx]] = [curr_features]
#    
#    output_df = pd.concat([output_df, curr_id_df], axis=0)       
#    print("{}/{}".format(ID_idx, len(member_ID)))

#all_data_by_date = {}
#for Date_idx in range(len(Date)):
#    curr_all_data_by_date = pd.DataFrame()
#    
#    for ID_idx in range(len(tasharep_ID)):
#        curr_id_data = all_data_dict[tasharep_ID[ID_idx]]
#        #curr_id_date_data = curr_id_data[curr_id_data["Date"] == Date[Date_idx]]
#        if (curr_id_data.index == Date[Date_idx]).sum() > 0:
#            curr_id_date_data = curr_id_data.loc[Date[Date_idx]]
#        else:
#            continue
#        
#        curr_all_data_by_date = pd.concat([curr_all_data_by_date, curr_id_date_data], axis=1)       
#       
#    curr_all_data_by_date = curr_all_data_by_date.T
#    curr_all_data_by_date.index = curr_all_data_by_date.ID
#    all_data_by_date[Date[Date_idx]] = curr_all_data_by_date
#    print("{}/{}".format(Date_idx, len(Date)))