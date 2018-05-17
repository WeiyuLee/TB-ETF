# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:52:19 2018

@author: Weiyu_Lee
"""
import numpy as np
import talib
from tqdm import tqdm

import config as conf

def pattern_preprocess(member_ID, Date, org_data):
    
    print("========== Pattern Preprocess Start ==========")
    
    PATTERN_conf = conf.config('feature_conf').config['PATTERN']
    if PATTERN_conf["enable"] is False:
        
        print("Pattern features are disabled.")
        
    else:    
    
        feature_list = ["CDL2CROWS", "CDL3BLACKCROWS", "CDL3INSIDE", "CDL3LINESTRIKE", "CDL3OUTSIDE",
                        "CDL3STARSINSOUTH", "CDL3WHITESOLDIERS", "CDLABANDONEDBABY", "CDLADVANCEBLOCK", "CDLBELTHOLD",
                        "CDLBREAKAWAY", "CDLCLOSINGMARUBOZU", "CDLCONCEALBABYSWALL", "CDLCOUNTERATTACK", "CDLDARKCLOUDCOVER",
                        "CDLDOJI", "CDLDOJISTAR", "CDLDRAGONFLYDOJI", "CDLENGULFING", "CDLEVENINGDOJISTAR",
                        "CDLEVENINGSTAR", "CDLGAPSIDESIDEWHITE", "CDLGRAVESTONEDOJI", "CDLHAMMER", "CDLHANGINGMAN",
                        "CDLHARAMI", "CDLHARAMICROSS", "CDLHIGHWAVE", "CDLHIKKAKE", "CDLHIKKAKEMOD",
                        "CDLHOMINGPIGEON", "CDLIDENTICAL3CROWS", "CDLINNECK", "CDLINVERTEDHAMMER", "CDLKICKING",
                        "CDLKICKINGBYLENGTH", "CDLLADDERBOTTOM", "CDLLONGLEGGEDDOJI", "CDLLONGLINE", "CDLMARUBOZU",
                        "CDLMATCHINGLOW", "CDLMATHOLD", "CDLMORNINGDOJISTAR", "CDLMORNINGSTAR", "CDLONNECK",
                        "CDLPIERCING", "CDLRICKSHAWMAN", "CDLRISEFALL3METHODS", "CDLSEPARATINGLINES", "CDLSHOOTINGSTAR",
                        "CDLSHORTLINE", "CDLSPINNINGTOP", "CDLSTALLEDPATTERN", "CDLSTICKSANDWICH", "CDLTAKURI",
                        "CDLTASUKIGAP", "CDLTHRUSTING", "CDLTRISTAR", "CDLUNIQUE3RIVER", "CDLUPSIDEGAP2CROWS", "CDLXSIDEGAP3METHODS"]

        for f_idx in range(len(feature_list)):
            feature_list[f_idx] = "pa_" + feature_list[f_idx]

        ID_pbar = tqdm(range(len(member_ID)))
        for ID_idx in ID_pbar:
            curr_ID_data = org_data.loc[member_ID[ID_idx]]
            
            curr_open_price_seq = []
            curr_high_price_seq = []
            curr_low_price_seq = []
            curr_close_price_seq = []
            curr_trade_price_seq = []
            
            for Date_idx in range(len(Date)):
                try:
                    curr_open_price = curr_ID_data[Date[Date_idx]][0]
                    curr_high_price = curr_ID_data[Date[Date_idx]][1]
                    curr_low_price = curr_ID_data[Date[Date_idx]][2]
                    curr_close_price = curr_ID_data[Date[Date_idx]][3]
                    curr_trade_price = curr_ID_data[Date[Date_idx]][4]
                except:
                    curr_open_price = float(np.NAN)
                    curr_high_price = float(np.NAN)
                    curr_low_price = float(np.NAN)
                    curr_close_price = float(np.NAN)
                    curr_trade_price = float(np.NAN)
                
                curr_open_price_seq.append(curr_open_price)        
                curr_high_price_seq.append(curr_high_price)        
                curr_low_price_seq.append(curr_low_price)        
                curr_close_price_seq.append(curr_close_price)            
                curr_trade_price_seq.append(curr_trade_price)            
            
            curr_open_price_seq = np.array(curr_open_price_seq)
            curr_high_price_seq = np.array(curr_high_price_seq)
            curr_low_price_seq = np.array(curr_low_price_seq)
            curr_close_price_seq = np.array(curr_close_price_seq)
            curr_trade_price_seq = np.array(curr_trade_price_seq)
                        
            CDL2CROWS_seq = talib.CDL2CROWS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDL3BLACKCROWS_seq = talib.CDL3BLACKCROWS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDL3INSIDE_seq = talib.CDL3INSIDE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDL3LINESTRIKE_seq = talib.CDL3LINESTRIKE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDL3OUTSIDE_seq = talib.CDL3OUTSIDE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDL3STARSINSOUTH_seq = talib.CDL3STARSINSOUTH(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDL3WHITESOLDIERS_seq = talib.CDL3WHITESOLDIERS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLABANDONEDBABY_seq = talib.CDLABANDONEDBABY(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLADVANCEBLOCK_seq = talib.CDLADVANCEBLOCK(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLBELTHOLD_seq = talib.CDLBELTHOLD(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLBREAKAWAY_seq = talib.CDLBREAKAWAY(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLCLOSINGMARUBOZU_seq = talib.CDLCLOSINGMARUBOZU(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLCONCEALBABYSWALL_seq = talib.CDLCONCEALBABYSWALL(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLCOUNTERATTACK_seq = talib.CDLCOUNTERATTACK(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLDARKCLOUDCOVER_seq = talib.CDLDARKCLOUDCOVER(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLDOJI_seq = talib.CDLDOJI(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLDOJISTAR_seq = talib.CDLDOJISTAR(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLDRAGONFLYDOJI_seq = talib.CDLDRAGONFLYDOJI(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLENGULFING_seq = talib.CDLENGULFING(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLEVENINGDOJISTAR_seq = talib.CDLEVENINGDOJISTAR(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLEVENINGSTAR_seq = talib.CDLEVENINGSTAR(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLGAPSIDESIDEWHITE_seq = talib.CDLGAPSIDESIDEWHITE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLGRAVESTONEDOJI_seq = talib.CDLGRAVESTONEDOJI(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHAMMER_seq = talib.CDLHAMMER(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHANGINGMAN_seq = talib.CDLHANGINGMAN(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHARAMI_seq = talib.CDLHARAMI(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHARAMICROSS_seq = talib.CDLHARAMICROSS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHIGHWAVE_seq = talib.CDLHIGHWAVE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHIKKAKE_seq = talib.CDLHIKKAKE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHIKKAKEMOD_seq = talib.CDLHIKKAKEMOD(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLHOMINGPIGEON_seq = talib.CDLHOMINGPIGEON(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLIDENTICAL3CROWS_seq = talib.CDLIDENTICAL3CROWS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLINNECK_seq = talib.CDLINNECK(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLINVERTEDHAMMER_seq = talib.CDLINVERTEDHAMMER(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLKICKING_seq = talib.CDLKICKING(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLKICKINGBYLENGTH_seq = talib.CDLKICKINGBYLENGTH(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLLADDERBOTTOM_seq = talib.CDLLADDERBOTTOM(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLLONGLEGGEDDOJI_seq = talib.CDLLONGLEGGEDDOJI(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLLONGLINE_seq = talib.CDLLONGLINE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLMARUBOZU_seq = talib.CDLMARUBOZU(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLMATCHINGLOW_seq = talib.CDLMATCHINGLOW(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLMATHOLD_seq = talib.CDLMATHOLD(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLMORNINGDOJISTAR_seq = talib.CDLMORNINGDOJISTAR(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLMORNINGSTAR_seq = talib.CDLMORNINGSTAR(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLONNECK_seq = talib.CDLONNECK(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLPIERCING_seq = talib.CDLPIERCING(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLRICKSHAWMAN_seq = talib.CDLRICKSHAWMAN(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLRISEFALL3METHODS_seq = talib.CDLRISEFALL3METHODS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLSEPARATINGLINES_seq = talib.CDLSEPARATINGLINES(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLSHOOTINGSTAR_seq = talib.CDLSHOOTINGSTAR(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLSHORTLINE_seq = talib.CDLSHORTLINE(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLSPINNINGTOP_seq = talib.CDLSPINNINGTOP(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLSTALLEDPATTERN_seq = talib.CDLSTALLEDPATTERN(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLSTICKSANDWICH_seq = talib.CDLSTICKSANDWICH(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLTAKURI_seq = talib.CDLTAKURI(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLTASUKIGAP_seq = talib.CDLTASUKIGAP(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLTHRUSTING_seq = talib.CDLTHRUSTING(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLTRISTAR_seq = talib.CDLTRISTAR(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLUNIQUE3RIVER_seq = talib.CDLUNIQUE3RIVER(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLUPSIDEGAP2CROWS_seq = talib.CDLUPSIDEGAP2CROWS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)
            
            CDLXSIDEGAP3METHODS_seq = talib.CDLXSIDEGAP3METHODS(curr_open_price_seq, curr_high_price_seq, curr_low_price_seq, curr_close_price_seq)  
            
            for Date_idx in range(len(Date)):
                temp_ta_features = []
                temp_ta_features.append(CDL2CROWS_seq[Date_idx])
                temp_ta_features.append(CDL3BLACKCROWS_seq[Date_idx])
                temp_ta_features.append(CDL3INSIDE_seq[Date_idx])
                temp_ta_features.append(CDL3LINESTRIKE_seq[Date_idx])
                temp_ta_features.append(CDL3OUTSIDE_seq[Date_idx])
                temp_ta_features.append(CDL3STARSINSOUTH_seq[Date_idx])
                temp_ta_features.append(CDL3WHITESOLDIERS_seq[Date_idx])
                temp_ta_features.append(CDLABANDONEDBABY_seq[Date_idx])
                temp_ta_features.append(CDLADVANCEBLOCK_seq[Date_idx])
                temp_ta_features.append(CDLBELTHOLD_seq[Date_idx])
                temp_ta_features.append(CDLBREAKAWAY_seq[Date_idx])
                temp_ta_features.append(CDLCLOSINGMARUBOZU_seq[Date_idx])
                temp_ta_features.append(CDLCONCEALBABYSWALL_seq[Date_idx])
                temp_ta_features.append(CDLCOUNTERATTACK_seq[Date_idx])
                temp_ta_features.append(CDLDARKCLOUDCOVER_seq[Date_idx])
                temp_ta_features.append(CDLDOJI_seq[Date_idx])
                temp_ta_features.append(CDLDOJISTAR_seq[Date_idx])
                temp_ta_features.append(CDLDRAGONFLYDOJI_seq[Date_idx])
                temp_ta_features.append(CDLENGULFING_seq[Date_idx])
                temp_ta_features.append(CDLEVENINGDOJISTAR_seq[Date_idx])
                temp_ta_features.append(CDLEVENINGSTAR_seq[Date_idx])
                temp_ta_features.append(CDLGAPSIDESIDEWHITE_seq[Date_idx])
                temp_ta_features.append(CDLGRAVESTONEDOJI_seq[Date_idx])
                temp_ta_features.append(CDLHAMMER_seq[Date_idx])
                temp_ta_features.append(CDLHANGINGMAN_seq[Date_idx])
                temp_ta_features.append(CDLHARAMI_seq[Date_idx])
                temp_ta_features.append(CDLHARAMICROSS_seq[Date_idx])
                temp_ta_features.append(CDLHIGHWAVE_seq[Date_idx])
                temp_ta_features.append(CDLHIKKAKE_seq[Date_idx])
                temp_ta_features.append(CDLHIKKAKEMOD_seq[Date_idx])
                temp_ta_features.append(CDLHOMINGPIGEON_seq[Date_idx])
                temp_ta_features.append(CDLIDENTICAL3CROWS_seq[Date_idx])
                temp_ta_features.append(CDLINNECK_seq[Date_idx])
                temp_ta_features.append(CDLINVERTEDHAMMER_seq[Date_idx])
                temp_ta_features.append(CDLKICKING_seq[Date_idx])
                temp_ta_features.append(CDLKICKINGBYLENGTH_seq[Date_idx])
                temp_ta_features.append(CDLLADDERBOTTOM_seq[Date_idx])
                temp_ta_features.append(CDLLONGLEGGEDDOJI_seq[Date_idx])
                temp_ta_features.append(CDLLONGLINE_seq[Date_idx])
                temp_ta_features.append(CDLMARUBOZU_seq[Date_idx])                
                temp_ta_features.append(CDLMATCHINGLOW_seq[Date_idx])                
                temp_ta_features.append(CDLMATHOLD_seq[Date_idx])
                temp_ta_features.append(CDLMORNINGDOJISTAR_seq[Date_idx])
                temp_ta_features.append(CDLMORNINGSTAR_seq[Date_idx])
                temp_ta_features.append(CDLONNECK_seq[Date_idx])
                temp_ta_features.append(CDLPIERCING_seq[Date_idx])
                temp_ta_features.append(CDLRICKSHAWMAN_seq[Date_idx])
                temp_ta_features.append(CDLRISEFALL3METHODS_seq[Date_idx])
                temp_ta_features.append(CDLSEPARATINGLINES_seq[Date_idx])
                temp_ta_features.append(CDLSHOOTINGSTAR_seq[Date_idx])
                temp_ta_features.append(CDLSHORTLINE_seq[Date_idx])
                temp_ta_features.append(CDLSPINNINGTOP_seq[Date_idx])
                temp_ta_features.append(CDLSTALLEDPATTERN_seq[Date_idx])
                temp_ta_features.append(CDLSTICKSANDWICH_seq[Date_idx])
                temp_ta_features.append(CDLTAKURI_seq[Date_idx])
                temp_ta_features.append(CDLTASUKIGAP_seq[Date_idx])                
                temp_ta_features.append(CDLTHRUSTING_seq[Date_idx])
                temp_ta_features.append(CDLTRISTAR_seq[Date_idx])
                temp_ta_features.append(CDLUNIQUE3RIVER_seq[Date_idx])
                temp_ta_features.append(CDLUPSIDEGAP2CROWS_seq[Date_idx])
                temp_ta_features.append(CDLXSIDEGAP3METHODS_seq[Date_idx])
                
                try:
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]].extend(temp_ta_features)                   
                except:
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]] = [org_data[Date[Date_idx]].loc[member_ID[ID_idx]]]
                    org_data[Date[Date_idx]].loc[member_ID[ID_idx]].extend(temp_ta_features)   
            
            ID_pbar.set_description("Process: {}/{}".format(ID_idx+1, len(member_ID)))       
            
    print("========== Pattern Preprocess Done! ==========")    

    return org_data, feature_list            