# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:00:04 2018

@author: Weiyu_Lee
"""

class config:

    def __init__(self, configuration):
		
        self.configuration = configuration
        self.config = {
        				  "Nm":{},  # Normalization
        				  "UD":{},  # Up, down features
                    "TA":{},  # TA features

                    "MA":{},  # Moving Average
                    "MACD":{},  # Moving Average Convergence/Divergence
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

        ### Normalization
        Nm_conf = self.config['Nm']   
        Nm_conf["enable"] = True        
        
        ### Up down
        UD_conf = self.config['UD']   
        UD_conf["enable"] = True
        
        ### TA
        # If TA_conf["enable"] is False, none of the TA features adds to the list.
        TA_conf = self.config['TA']   
        TA_conf["enable"] = True
        
        # Moving Average        
        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 
        MA_conf = self.config['MA']   
        MA_conf["enable"] = True
        MA_conf["MA_Type"] = [0, 1, 2, 3, 4, 5, 6, 7, 8]       
        MA_conf["timeperiod"] = [5, 13, 26, 52]
        
        # Moving Average Convergence/Divergence    
        # period: [fastperiod, slowperiod, signalperiod]
        MACD_conf = self.config['MACD']   
        MACD_conf["enable"] = True
        MACD_conf["period"] = [[12, 26, 9]]              
        