# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:00:04 2018

@author: Weiyu_Lee
"""

class config:

    def __init__(self, configuration):
		
        self.configuration = configuration
        self.config = {
        				  "Nm":{},            # Normalization

        				  "UD":{},            # Up, down features
        				  "LT":{},            # Long term features                          
                    "STOCKS":{},        # Other Stocks's price & trade
                    "EXCH":{},          # Exchange rate
                    "TAIEX":{},         # The Weighted Price Index of the Taiwan Stock Exchange                     
                    "TA":{},            # TA features
                    "PATTERN":{},       # Pattern Recognition
                    
                    # Overlap Studies
                    "MA":{},            # Moving Average
                    "HT_TRENDLINE":{},  # Hilbert Transform - Instantaneous Trendline
                    "MIDPOINT":{},      # MidPoint over period
                    "MIDPRICE":{},      # Midpoint Price over period
                    
                    # Momentum Indicators
                    "CCI":{},           # Commodity Channel Index
                    "MACD":{},          # Moving Average Convergence/Divergence
                    "RSI":{},           # Relative Strength Index
                    "KDJ":{},           # Stochastic (STOCH) KDJ
                    
                    # Volume Indicators
                    "AD":{},            # Chaikin A/D Line  
                    "ADOSC":{},         # Chaikin A/D Oscillator
                    "OBV":{},           # Chaikin A/D Line                   
                    
                    # Cycle Indicators
                    "HT_DCPERIOD":{},   # Hilbert Transform - Dominant Cycle Period
                    "HT_DCPHASE":{},    # Hilbert Transform - Dominant Cycle Phase
                    
                    # Volatility Indicators
                    "ATR":{},           # Average True Range
                    "NATR":{},          # Normalized Average True Range
						}
        self.get_config()


    def get_config(self):

        try:
            conf = getattr(self, self.configuration)
            conf()

        except: 
            print("Can not find configuration")
            raise
            
    def feature_conf(self):

        # Normalization
        # type: 0=before ta_preprocess, 1=after ta_preprocess
        Nm_conf = self.config['Nm']   
        Nm_conf["enable"] = True
        Nm_conf["ratio_enable"] = False
        Nm_conf["type"] = [1]
        Nm_conf["method"] = "Standard"
        
        # Up down
        UD_conf = self.config['UD']   
        UD_conf["enable"] = True

        # Long term features                          
        LT_conf = self.config['LT']   
        LT_conf["enable"] = True

        # Other Stocks's price & trade
        STOCKS_conf = self.config['STOCKS']   
        STOCKS_conf["enable"] = False
        STOCKS_conf["stocks"] = ["2330", "2317"]

        # Exchange rate
        EXCH_conf = self.config['EXCH']   
        EXCH_conf["enable"] = True
        EXCH_conf["Nm"] = True
        if EXCH_conf["Nm"] is True:
            EXCH_conf["file_path"] = "./Data/exchange_rate_data_Nm.pkl"
        else:
            EXCH_conf["file_path"] = "./Data/exchange_rate_data_woNm.pkl"
            
        # The Weighted Price Index of the Taiwan Stock Exchange    
        TAIEX_conf = self.config['TAIEX']   
        TAIEX_conf["enable"] = True
        TAIEX_conf["Nm"] = True
        if TAIEX_conf["Nm"] is True:
            TAIEX_conf["file_path"] = "./Data/taiex_data_Nm.pkl"
        else:
            TAIEX_conf["file_path"] = "./Data/taiex_data_woNm.pkl"
            
        ### TA
        # If TA_conf["enable"] is False, none of the TA features adds to the list.
        TA_conf = self.config['TA']   
        TA_conf["enable"] = True
        TA_conf["Nm"] = True

        ### Pattern Recognition
        # If PATTERN_conf["enable"] is False, none of the Pattern features adds to the list.
        PATTERN_conf = self.config['PATTERN']   
        PATTERN_conf["enable"] = True
        PATTERN_conf["Nm"] = False

        #######################################################################
        ########################### Overlap Studies ###########################
        #######################################################################
        
        # Moving Average        
        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 
        MA_conf = self.config['MA']   
        MA_conf["enable"] = True
        MA_conf["MA_Type"] = [0, 1, 2, 3, 4, 5, 6, 7, 8]       
        MA_conf["timeperiod"] = [3, 5, 13, 26, 52]
        
        # Hilbert Transform - Instantaneous Trendline
        HT_TRENDLINE_conf = self.config['HT_TRENDLINE']   
        HT_TRENDLINE_conf["enable"] = True                 

        # MidPoint over period
        MIDPOINT_conf = self.config['MIDPOINT']   
        MIDPOINT_conf["enable"] = True
        MIDPOINT_conf["period"] = [14]             
        
        # Midpoint Price over period
        MIDPRICE_conf = self.config['MIDPRICE']   
        MIDPRICE_conf["enable"] = True
        MIDPRICE_conf["period"] = [14]    

        #######################################################################
        ######################### Momentum Indicators #########################
        #######################################################################

        # Commodity Channel Index
        CCI_conf = self.config['CCI']   
        CCI_conf["enable"] = True
        CCI_conf["period"] = [14]              

        # Moving Average Convergence/Divergence    
        # period: [fastperiod, slowperiod, signalperiod]
        MACD_conf = self.config['MACD']   
        MACD_conf["enable"] = True
        MACD_conf["period"] = [[12, 26, 9], [5, 30, 3], [8, 13, 9]]              

        # Relative Strength Index
        RSI_conf = self.config['RSI']   
        RSI_conf["enable"] = True
        RSI_conf["period"] = [14, 28, 42]              

        # Stochastic (STOCH) KDJ
        # period: [fastk_period, slowk_period, slowd_period]
        KDJ_conf = self.config['KDJ']   
        KDJ_conf["enable"] = True
        KDJ_conf["period"] = [[9, 9, 3], [3, 2, 2]]              
       
        #######################################################################
        ########################## Volume Indicators ##########################
        #######################################################################

        # Chaikin A/D Line
        AD_conf = self.config['AD']   
        AD_conf["enable"] = True 

        # Chaikin A/D Oscillator
        # period: [fastperiod, slowperiod]
        ADOSC_conf = self.config['ADOSC']   
        ADOSC_conf["period"] = [[3, 10]]              
        ADOSC_conf["enable"] = True 
        
        # On Balance Volume
        OBV_conf = self.config['OBV']   
        OBV_conf["enable"] = True         

        #######################################################################
        ########################### Cycle Indicators ##########################
        #######################################################################
        
        # Hilbert Transform - Dominant Cycle Period
        HT_DCPERIOD_conf = self.config['HT_DCPERIOD']   
        HT_DCPERIOD_conf["enable"] = True                 

        # Hilbert Transform - Dominant Cycle Phase
        HT_DCPHASE_conf = self.config['HT_DCPHASE']   
        HT_DCPHASE_conf["enable"] = True                 
        
        #######################################################################
        ######################## Volatility Indicators ########################
        #######################################################################        
        
        # Average True Range
        ATR_conf = self.config['ATR']   
        ATR_conf["period"] = [14, 28, 42]              
        ATR_conf["enable"] = True         
        
        # Normalized Average True Range
        NATR_conf = self.config['NATR']   
        NATR_conf["period"] = [14, 28, 42]              
        NATR_conf["enable"] = True                 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        