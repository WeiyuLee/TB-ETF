# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:33:44 2018

@author: Weiyu_Lee
"""
import numpy as np
import talib
from tqdm import tqdm

import config as conf

def ta_MA(MA_conf, curr_close_price_seq):

    MA_seqs = []
    curr_feature_list = []
    
    MA_Type_num = len(MA_conf["MA_Type"])
    timeperiod_num = len(MA_conf["timeperiod"])
    
    for i in range(MA_Type_num):
        curr_MA_Type = MA_conf["MA_Type"][i]
        
        for j in range(timeperiod_num):                   
            curr_timeperiod = MA_conf["timeperiod"][j]           
            curr_feature_list.append("MA_" + str(curr_MA_Type) + "_" + str(curr_timeperiod))
            
            curr_MA_seq = talib.MA(curr_close_price_seq, curr_timeperiod, matype=curr_MA_Type)
            MA_seqs.append(curr_MA_seq.copy())    
                    
    return MA_seqs, curr_feature_list

def ta_HT_TRENDLINE(HT_TRENDLINE_conf, curr_close_price_seq):

    curr_feature_list = []
    
    HT_TRENDLINE_seqs = talib.HT_TRENDLINE(curr_close_price_seq)
    
    curr_feature_list.append("HT_TRENDLINE")   

    return HT_TRENDLINE_seqs, curr_feature_list

def ta_MIDPOINT(MIDPOINT_conf, curr_close_price_seq):

    MIDPOINT_seqs = []
    curr_feature_list = []
    
    MIDPOINT_period_num = len(MIDPOINT_conf["period"])
    
    for i in range(MIDPOINT_period_num):
        curr_period = MIDPOINT_conf["period"][0]
        
        curr_feature_list.append("MIDPOINT_" + str(curr_period))
        
        curr_MIDPOINT_seq = talib.MIDPOINT(curr_close_price_seq, timeperiod=curr_period) 
        
        MIDPOINT_seqs.append(curr_MIDPOINT_seq.copy())

    return MIDPOINT_seqs, curr_feature_list

def ta_MIDPRICE(MIDPRICE_conf, curr_high_price_seq, curr_low_price_seq):

    MIDPRICE_seqs = []
    curr_feature_list = []
    
    MIDPRICE_period_num = len(MIDPRICE_conf["period"])
    
    for i in range(MIDPRICE_period_num):
        curr_period = MIDPRICE_conf["period"][0]
        
        curr_feature_list.append("MIDPRICE_" + str(curr_period))
        
        curr_MIDPRICE_seq = talib.MIDPRICE(curr_high_price_seq, curr_low_price_seq, timeperiod=curr_period) 

        MIDPRICE_seqs.append(curr_MIDPRICE_seq.copy())

    return MIDPRICE_seqs, curr_feature_list

def ta_CCI(CCI_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq):

    CCI_seqs = []
    curr_feature_list = []
    
    CCI_period_num = len(CCI_conf["period"])
    
    for i in range(CCI_period_num):
        curr_period = CCI_conf["period"][0]
        
        curr_feature_list.append("CCI_" + str(curr_period))
        
        curr_CCI_seq = talib.CCI(curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, timeperiod=curr_period) 
        
        CCI_seqs.append(curr_CCI_seq.copy())

    return CCI_seqs, curr_feature_list

def ta_MACD(MACD_conf, curr_close_price_seq):

    MACD_seqs = []
    curr_feature_list = []
    
    MACD_period_num = len(MACD_conf["period"])
    
    for i in range(MACD_period_num):
        curr_fast_period = MACD_conf["period"][i][0]
        curr_slow_period = MACD_conf["period"][i][1]
        curr_signal_period = MACD_conf["period"][i][2]
        
        curr_feature_list.append("MACD_" + str(curr_fast_period) + "_" + str(curr_slow_period) + "_" + str(curr_signal_period) + "_fast")
        curr_feature_list.append("MACD_" + str(curr_fast_period) + "_" + str(curr_slow_period) + "_" + str(curr_signal_period) + "_slow")
        curr_feature_list.append("MACD_" + str(curr_fast_period) + "_" + str(curr_slow_period) + "_" + str(curr_signal_period) + "_signal")
        
        curr_MACD, curr_signal, curr_hist = talib.MACD(curr_close_price_seq, 
                                                       fastperiod=curr_fast_period, 
                                                       slowperiod=curr_slow_period, 
                                                       signalperiod=curr_signal_period)      
        
        MACD_seqs.append([curr_MACD.copy(), curr_signal.copy(), curr_hist.copy()])
    
    return MACD_seqs, curr_feature_list

def ta_RSI(RSI_conf, curr_close_price_seq):

    RSI_seqs = []
    curr_feature_list = []
    
    RSI_period_num = len(RSI_conf["period"])
    
    for i in range(RSI_period_num):
        curr_period = RSI_conf["period"][i]
        
        curr_feature_list.append("RSI_" + str(curr_period))
        
        curr_RSI = talib.RSI(curr_close_price_seq, timeperiod=curr_period) 

        RSI_seqs.append(curr_RSI.copy())

    return RSI_seqs, curr_feature_list

def ta_KDJ(KDJ_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq):

    KDJ_seqs = []
    curr_feature_list = []
    
    KDJ_period_num = len(KDJ_conf["period"])
    
    for i in range(KDJ_period_num):
        curr_fastk_period = KDJ_conf["period"][i][0]
        curr_slowk_period = KDJ_conf["period"][i][1]
        curr_slowd_period = KDJ_conf["period"][i][2]
        
        curr_feature_list.append("KDJ_" + str(curr_fastk_period) + "_" + str(curr_slowk_period) + "_" + str(curr_slowd_period) + "_slowk")
        curr_feature_list.append("KDJ_" + str(curr_fastk_period) + "_" + str(curr_slowk_period) + "_" + str(curr_slowd_period) + "_slowd")
        
        curr_slowk, curr_slowd = talib.STOCH(high=curr_high_price_seq,
                                             low=curr_low_price_seq,
                                             close=curr_close_price_seq, 
                                             fastk_period=curr_fastk_period, 
                                             slowk_period=curr_slowk_period, 
                                             slowk_matype=0,
                                             slowd_period=curr_slowd_period,
                                             slowd_matype=0)
        KDJ_seqs.append([curr_slowk.copy(), curr_slowd.copy()])

    return KDJ_seqs, curr_feature_list

def ta_AD(AD_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, curr_trade_price_seq):

    curr_feature_list = []
    
    AD_seqs = talib.AD(curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, curr_trade_price_seq)
    
    curr_feature_list.append("AD")   

    return AD_seqs, curr_feature_list

def ta_ADOSC(ADOSC_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, curr_trade_price_seq):

    ADOSC_seqs = []
    curr_feature_list = []
    
    ADOSC_period_num = len(ADOSC_conf["period"])
    
    for i in range(ADOSC_period_num):
        curr_fast_period = ADOSC_conf["period"][i][0]
        curr_slow_period = ADOSC_conf["period"][i][1]
        
        curr_feature_list.append("ADOSC_" + str(curr_fast_period) + "_" + str(curr_slow_period))
        
        curr_ADOSC_seqs = talib.ADOSC(curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, curr_trade_price_seq, fastperiod=curr_fast_period, slowperiod=curr_slow_period)
        
        ADOSC_seqs.append(curr_ADOSC_seqs.copy())
        
    return ADOSC_seqs, curr_feature_list

def ta_OBV(OBV_conf, curr_close_price_seq, curr_trade_price_seq):

    curr_feature_list = []
    
    OBV_seqs = talib.OBV(curr_close_price_seq, curr_trade_price_seq)
    
    curr_feature_list.append("OBV")   

    return OBV_seqs, curr_feature_list

def ta_HT_DCPERIOD(HT_DCPERIOD_conf, curr_close_price_seq):

    curr_feature_list = []
    
    HT_DCPERIOD_seqs = talib.HT_DCPERIOD(curr_close_price_seq)
    
    curr_feature_list.append("HT_DCPERIOD")   

    return HT_DCPERIOD_seqs, curr_feature_list

def ta_HT_DCPHASE(HT_DCPERIOD_conf, curr_close_price_seq):

    curr_feature_list = []
    
    HT_DCPHASE_seqs = talib.HT_DCPHASE(curr_close_price_seq)
    
    curr_feature_list.append("HT_DCPHASE")   

    return HT_DCPHASE_seqs, curr_feature_list

def ta_ATR(ATR_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq):

    ATR_seqs = []
    curr_feature_list = []
    
    ATR_period_num = len(ATR_conf["period"])
    
    for i in range(ATR_period_num):
        curr_period = ATR_conf["period"][i]
        
        curr_feature_list.append("ATR_" + str(curr_period))
        
        curr_ATR_seqs = talib.ATR(curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, timeperiod=curr_period)
        
        ATR_seqs.append(curr_ATR_seqs.copy())
        
    return ATR_seqs, curr_feature_list

def ta_NATR(NATR_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq):

    NATR_seqs = []
    curr_feature_list = []
    
    NATR_period_num = len(NATR_conf["period"])
    
    for i in range(NATR_period_num):
        curr_period = NATR_conf["period"][i]
        
        curr_feature_list.append("NATR_" + str(curr_period))
        
        curr_NATR_seqs = talib.ATR(curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, timeperiod=curr_period)
        
        NATR_seqs.append(curr_NATR_seqs.copy())
        
    return NATR_seqs, curr_feature_list

def ta_preprocess(member_ID, Date, org_data):
    
    print("========== TA Preprocess Start ==========")
    
    feature_list = []
    TA_conf = conf.config('feature_conf').config['TA']
    if TA_conf["enable"] is False:
        
        print("TA features are disabled.")
        
    else:
        ID_pbar = tqdm(range(len(member_ID)))
        for ID_idx in ID_pbar:
            curr_ID_data = org_data.loc[member_ID[ID_idx]]
            
            curr_high_price_seq = []
            curr_low_price_seq = []
            curr_close_price_seq = []
            curr_trade_price_seq = []
            
            for Date_idx in range(len(Date)):
                try:
                    curr_high_price = curr_ID_data[Date[Date_idx]][1]
                    curr_low_price = curr_ID_data[Date[Date_idx]][2]
                    curr_close_price = curr_ID_data[Date[Date_idx]][3]
                    curr_trade_price = curr_ID_data[Date[Date_idx]][4]
                except:
                    curr_high_price = float(np.NAN)
                    curr_low_price = float(np.NAN)
                    curr_close_price = float(np.NAN)
                    curr_trade_price = float(np.NAN)
                
                curr_high_price_seq.append(curr_high_price)        
                curr_low_price_seq.append(curr_low_price)        
                curr_close_price_seq.append(curr_close_price)            
                curr_trade_price_seq.append(curr_trade_price)            
            
            curr_high_price_seq = np.array(curr_high_price_seq)
            curr_low_price_seq = np.array(curr_low_price_seq)
            curr_close_price_seq = np.array(curr_close_price_seq)
            curr_trade_price_seq = np.array(curr_trade_price_seq)
            
            ########################### Overlap Studies ###########################           
            
            # Moving Average
            MA_conf = conf.config('feature_conf').config['MA']
            if MA_conf["enable"] is True:
                MA_seqs, MA_feature_list = ta_MA(MA_conf, curr_close_price_seq)
                if ID_idx == 0: feature_list.extend(MA_feature_list)
                
            # Hilbert Transform - Instantaneous Trendline
            HT_TRENDLINE_conf = conf.config('feature_conf').config['HT_TRENDLINE']
            if HT_TRENDLINE_conf["enable"] is True:        
                HT_TRENDLINE_seqs, HT_TRENDLINE_feature_list = ta_HT_TRENDLINE(HT_TRENDLINE_conf, curr_close_price_seq)                
                if ID_idx == 0: feature_list.extend(HT_TRENDLINE_feature_list)                            

            # MidPoint over period
            MIDPOINT_conf = conf.config('feature_conf').config['MIDPOINT']
            if MIDPOINT_conf["enable"] is True:        
                MIDPOINT_seqs, MIDPOINT_feature_list = ta_MIDPOINT(MIDPOINT_conf, curr_close_price_seq)
                if ID_idx == 0: feature_list.extend(MIDPOINT_feature_list)               

            # Midpoint Price over period
            MIDPRICE_conf = conf.config('feature_conf').config['MIDPRICE']
            if MIDPRICE_conf["enable"] is True:        
                MIDPRICE_seqs, MIDPRICE_feature_list = ta_MIDPRICE(MIDPRICE_conf, curr_high_price_seq, curr_low_price_seq)
                if ID_idx == 0: feature_list.extend(MIDPRICE_feature_list)               

            ######################### Momentum Indicators #########################

            # Commodity Channel Index
            CCI_conf = conf.config('feature_conf').config['CCI']
            if CCI_conf["enable"] is True:        
                CCI_seqs, CCI_feature_list = ta_CCI(CCI_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
                if ID_idx == 0: feature_list.extend(CCI_feature_list)               

            # Moving Average Convergence/Divergence    
            MACD_conf = conf.config('feature_conf').config['MACD']
            if MACD_conf["enable"] is True:        
                MACD_seqs, MACD_feature_list = ta_MACD(MACD_conf, curr_close_price_seq)                
                if ID_idx == 0: feature_list.extend(MACD_feature_list)

            # Relative Strength Index
            RSI_conf = conf.config('feature_conf').config['RSI']
            if RSI_conf["enable"] is True:        
                RSI_seqs, RSI_feature_list = ta_RSI(RSI_conf, curr_close_price_seq)
                if ID_idx == 0: feature_list.extend(RSI_feature_list)               

            # Stochastic (STOCH) KDJ
            KDJ_conf = conf.config('feature_conf').config['KDJ']
            if KDJ_conf["enable"] is True:        
                KDJ_seqs, KDJ_feature_list = ta_KDJ(KDJ_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
                if ID_idx == 0: feature_list.extend(KDJ_feature_list)               

            ########################## Volume Indicators ##########################

            # Chaikin A/D Line
            AD_conf = conf.config('feature_conf').config['AD']
            if AD_conf["enable"] is True:        
                AD_seqs, AD_feature_list = ta_AD(AD_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, curr_trade_price_seq)                
                if ID_idx == 0: feature_list.extend(AD_feature_list)

            # Chaikin A/D Oscillator
            ADOSC_conf = conf.config('feature_conf').config['ADOSC']
            if ADOSC_conf["enable"] is True:        
                ADOSC_seqs, ADOSC_feature_list = ta_ADOSC(ADOSC_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq, curr_trade_price_seq)                
                if ID_idx == 0: feature_list.extend(ADOSC_feature_list)

            # On Balance Volume
            OBV_conf = conf.config('feature_conf').config['OBV']
            if OBV_conf["enable"] is True:        
                OBV_seqs, OBV_feature_list = ta_OBV(OBV_conf, curr_close_price_seq, curr_trade_price_seq)                
                if ID_idx == 0: feature_list.extend(OBV_feature_list)
            
            ########################### Cycle Indicators ##########################

            # Hilbert Transform - Dominant Cycle Period
            HT_DCPERIOD_conf = conf.config('feature_conf').config['HT_DCPERIOD']
            if HT_DCPERIOD_conf["enable"] is True:        
                HT_DCPERIOD_seqs, HT_DCPERIOD_feature_list = ta_HT_DCPERIOD(HT_DCPERIOD_conf, curr_close_price_seq)                
                if ID_idx == 0: feature_list.extend(HT_DCPERIOD_feature_list)            

            # Hilbert Transform - Dominant Cycle Period
            HT_DCPHASE_conf = conf.config('feature_conf').config['HT_DCPHASE']
            if HT_DCPHASE_conf["enable"] is True:        
                HT_DCPHASE_seqs, HT_DCPHASE_feature_list = ta_HT_DCPHASE(HT_DCPHASE_conf, curr_close_price_seq)                
                if ID_idx == 0: feature_list.extend(HT_DCPHASE_feature_list)            
                
            ######################## Volatility Indicators ########################
            
            # Average True Range
            ATR_conf = conf.config('feature_conf').config['ATR']
            if ATR_conf["enable"] is True:        
                ATR_seqs, ATR_feature_list = ta_ATR(ATR_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)                
                if ID_idx == 0: feature_list.extend(ATR_feature_list)

            # Normalized Average True Range
            NATR_conf = conf.config('feature_conf').config['NATR']
            if NATR_conf["enable"] is True:        
                NATR_seqs, NATR_feature_list = ta_NATR(NATR_conf, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)                
                if ID_idx == 0: feature_list.extend(NATR_feature_list)
                
            # Append the features to the original DataFrame
            for Date_idx in range(len(Date)):
                temp_ta_features = []
                
                if MA_conf["enable"] is True:
                    for i in range(len(MA_feature_list)):
                        temp_ta_features.append(MA_seqs[i][Date_idx])

                if HT_TRENDLINE_conf["enable"] is True:        
                    temp_ta_features.append(HT_TRENDLINE_seqs[Date_idx])

                if MIDPOINT_conf["enable"] is True:        
                    for i in range(len(MIDPOINT_conf["period"])):
                        temp_ta_features.append(MIDPOINT_seqs[i][Date_idx])    

                if MIDPRICE_conf["enable"] is True:        
                    for i in range(len(MIDPRICE_conf["period"])):
                        temp_ta_features.append(MIDPRICE_seqs[i][Date_idx])                            

                if CCI_conf["enable"] is True:        
                    for i in range(len(CCI_conf["period"])):
                        temp_ta_features.append(CCI_seqs[i][Date_idx])    

                if MACD_conf["enable"] is True:
                    for i in range(len(MACD_conf["period"])):
                        temp_ta_features.append(MACD_seqs[i][0][Date_idx])
                        temp_ta_features.append(MACD_seqs[i][1][Date_idx])
                        temp_ta_features.append(MACD_seqs[i][2][Date_idx])

                if RSI_conf["enable"] is True:        
                    for i in range(len(RSI_conf["period"])):
                        temp_ta_features.append(RSI_seqs[i][Date_idx])    
    
                if KDJ_conf["enable"] is True:
                    for i in range(len(KDJ_conf["period"])):
                        temp_ta_features.append(KDJ_seqs[i][0][Date_idx])
                        temp_ta_features.append(KDJ_seqs[i][1][Date_idx])                       
               
                if AD_conf["enable"] is True:        
                    temp_ta_features.append(AD_seqs[Date_idx])
                
                if ADOSC_conf["enable"] is True:        
                    for i in range(len(ADOSC_conf["period"])):
                        temp_ta_features.append(ADOSC_seqs[i][Date_idx])    

                if OBV_conf["enable"] is True:        
                    temp_ta_features.append(OBV_seqs[Date_idx])

                if HT_DCPERIOD_conf["enable"] is True:        
                    temp_ta_features.append(HT_DCPERIOD_seqs[Date_idx])

                if HT_DCPHASE_conf["enable"] is True:        
                    temp_ta_features.append(HT_DCPHASE_seqs[Date_idx])

                if ATR_conf["enable"] is True:        
                    for i in range(len(ATR_conf["period"])):
                        temp_ta_features.append(ATR_seqs[i][Date_idx])    

                if NATR_conf["enable"] is True:        
                    for i in range(len(NATR_conf["period"])):
                        temp_ta_features.append(NATR_seqs[i][Date_idx])    
                        
                try:
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]].extend(temp_ta_features)                   
                except:
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]] = [org_data[Date[Date_idx]].loc[member_ID[ID_idx]]]
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]].extend(temp_ta_features)                       
                    
            ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))        
        
    print("========== TA Preprocess Done! ==========")    

    return org_data, feature_list