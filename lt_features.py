# -*- coding: utf-8 -*-
"""
Created on Fri May 11 14:16:53 2018

@author: Weiyu_Lee
"""
import numpy as np
import pandas as pd
import datetime

import config as conf

from tqdm import tqdm

def lt_preprocess(member_ID, Date, org_data):
    
    print("========== Long Term Preprocess Start ==========")
    
    LT_conf = conf.config('feature_conf').config["LT"]
    if LT_conf["enable"] is False:
        
        print("LT features are disabled.")
    else:
        ID_pbar = tqdm(range(len(member_ID)))

        for ID_idx in ID_pbar:
            curr_ID_data = org_data.loc[member_ID[ID_idx]]
            
            year_data = []
            for j in range(6):                  
                week_data = []
                for i in range(60):
                    week_data.append([])
                year_data.append(week_data)
                
            for Date_idx in range(len(Date)):
                curr_date = datetime.datetime.strptime(Date[Date_idx], "%Y%m%d")
                curr_year_num = curr_date.isocalendar()[0]
                curr_week_num = curr_date.isocalendar()[1]
                               
                week_data = year_data[curr_year_num-2013]
                try:
                    week_data[curr_week_num].append(curr_ID_data[Date[Date_idx]][0:5])
                except:
                    week_data[curr_week_num].append([np.NAN, np.NAN, np.NAN, np.NAN, np.NAN])
            
            # Remove [] in the list
            #year_data = [x for x in year_data if x != []]
            for j in range(6):
                if year_data[j] == []:
                    continue
                else:
                    week_data = year_data[j]
                    #week_data = [x for x in week_data if x != []]
                
                    for i in range(len(week_data)):
                        if week_data[i] == []:
                            continue
                        else:
                            week_data[i] = np.vstack(week_data[i])
                            week_data[i] = [week_data[i][0, 0], 
                                            week_data[i][:, 0:4].max(),
                                            week_data[i][:, 0:4].min(),
                                            week_data[i][-1, 3],
                                            sum(week_data[i][:, 4])/5]         # Should be divided ?                  

            for Date_idx in range(len(Date)):
                curr_date = datetime.datetime.strptime(Date[Date_idx], "%Y%m%d")
                curr_year_num = curr_date.isocalendar()[0]
                curr_week_num = curr_date.isocalendar()[1]
                
                if year_data[curr_year_num-2013] == []:
                    continue
                else:
                    week_data = year_data[curr_year_num-2013]
                
                    if week_data[curr_week_num] != []:
                        #org_data.loc[member_ID[ID_idx]][Date[Date_idx]].extend(week_data[curr_week_num])
                        org_data.loc[member_ID[ID_idx]][Date[Date_idx]] = np.append(org_data.loc[member_ID[ID_idx]][Date[Date_idx]], week_data[curr_week_num])
                
            ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))
        
        feature_list = ["LT_open_price", "LT_max", "LT_min", "LT_close", "LT_trade"]
        
    print("========== Long Term Preprocess Done! ==========")   
    
    return org_data, feature_list
