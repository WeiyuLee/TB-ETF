# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 10:57:13 2018

@author: Weiyu_Lee
"""

import numpy as np
import pandas as pd
import pickle

f = open('./Data/all_data.pkl', 'rb')  
all_data_dict = pickle.load(f)
tasharep_ID = pickle.load(f)
Date = pickle.load(f)

