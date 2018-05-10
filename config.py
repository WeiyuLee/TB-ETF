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
                    "TA":{},            # TA features
                    
                    # Overlap Studies
                    "MA":{},            # Moving Average
                    "HT_TRENDLINE":{},  # Moving Average
                    
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
        Nm_conf["type"] = [0]
        
        # Up down
        UD_conf = self.config['UD']   
        UD_conf["enable"] = True
        
        ### TA
        # If TA_conf["enable"] is False, none of the TA features adds to the list.
        TA_conf = self.config['TA']   
        TA_conf["enable"] = True

        #######################################################################
        ########################### Overlap Studies ###########################
        #######################################################################
        
        # Moving Average        
        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 
        MA_conf = self.config['MA']   
        MA_conf["enable"] = True
        MA_conf["MA_Type"] = [0, 1, 2, 3, 4, 5, 6, 7, 8]       
        MA_conf["timeperiod"] = [5, 13, 26, 52]
        
        # Hilbert Transform - Instantaneous Trendline
        HT_TRENDLINE_conf = self.config['HT_TRENDLINE']   
        HT_TRENDLINE_conf["enable"] = True                 

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
        MACD_conf["period"] = [[12, 26, 9]]              

        # Relative Strength Index
        RSI_conf = self.config['RSI']   
        RSI_conf["enable"] = True
        RSI_conf["period"] = [14]              

        # Stochastic (STOCH) KDJ
        # period: [fastk_period, slowk_period, slowd_period]
        KDJ_conf = self.config['KDJ']   
        KDJ_conf["enable"] = True
        KDJ_conf["period"] = [[9, 9, 3]]              
       
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
        ATR_conf["period"] = [14]              
        ATR_conf["enable"] = True         
        
        # Normalized Average True Range
        NATR_conf = self.config['NATR']   
        NATR_conf["period"] = [14]              
        NATR_conf["enable"] = True                 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        