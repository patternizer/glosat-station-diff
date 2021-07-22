#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# PROGRAM: glosat-station-diff.py
#------------------------------------------------------------------------------
# Version 0.1
# 22 July, 2021
# Michael Taylor
# https://patternizer.github.io
# patternizer AT gmail DOT com
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------
# Dataframe libraries:
import numpy as np
import pandas as pd
import pickle
from datetime import datetime

# Silence library version notifications
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

nheader = 1

station_1 = 'Paris_new_ex_Daniel.Tg'
station_2 = 'stationfile.txt'

stationcode = '071560'

pkl_archive = 'DATA/df_temp.pkl'
df_temp = pd.read_pickle(pkl_archive, compression='bz2')    
station_metadata = df_temp[df_temp['stationcode']==stationcode].iloc[0,14:23]

#------------------------------------------------------------------------------
# LOAD: station_1
#------------------------------------------------------------------------------

f = open(station_1)
lines = f.readlines()    
dates = []
vals = []
for i in range(nheader,len(lines)):    
    words = lines[i].split()
    if len(words) > 1:                    
        date = int(words[0])
        val = (len(words)-1)*[None]
        for j in range(len(val)):
            try: val[j] = int(words[j+1])
            except: pass
        dates.append(date)
        vals.append(val) 
f.close()    
dates = np.array(dates)
vals = np.array(vals)

df_1 = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
df_1['year'] = dates
for j in range(1,13):   
    df_1[df_1.columns[j]] = [ vals[i][j-1] for i in range(len(df_1)) ]

#------------------------------------------------------------------------------
# LOAD: station_2
#------------------------------------------------------------------------------

f = open(station_2)
lines = f.readlines()    
dates = []
vals = []
for i in range(nheader,len(lines)):    
    words = lines[i].split()
    if len(words) > 1:                    
        date = int(words[0])
        val = (len(words)-1)*[None]
        for j in range(len(val)):
            try: val[j] = int(words[j+1])
            except: pass
        dates.append(date)
        vals.append(val) 
f.close()    
dates = np.array(dates)
vals = np.array(vals)

df_2 = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
df_2['year'] = dates
for j in range(1,13):   
    df_2[df_2.columns[j]] = [ vals[i][j-1] for i in range(len(df_2)) ]

#------------------------------------------------------------------------------
# CALCULATE: differences
#------------------------------------------------------------------------------

station_diff = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
station_diff['year'] = dates
for j in range(1,13):
    station_diff[str(j)] = df_1[str(j)] - df_2[str(j)]
        
stationfile = 'station_diff.csv'
station_data = station_diff.iloc[:,range(0,13)].reset_index(drop=True).astype(int)
stationcode = stationcode
stationlat = "{:<4}".format(str(int(station_metadata[0]*10)))
stationlon = "{:<4}".format(str(int(station_metadata[1]*10)))
stationelevation = "{:<3}".format(str(station_metadata[2]))
stationname = "{:<20}".format(station_metadata[3][:20])
stationcountry = "{:<13}".format(station_metadata[4][:13])
stationfirstlast = str(station_metadata[5]) + str(station_metadata[6])
stationsourcefirst = "{:<8}".format(str(station_metadata[7]) + str(station_metadata[8]))
stationgridcell = "{:<3}".format('NAN')
station_header = ' ' + stationcode[0:] + ' ' + stationlat + ' ' + stationlon + ' ' + stationelevation + ' ' + stationname + ' ' + stationcountry + ' ' + stationfirstlast + '  ' + stationsourcefirst + '   ' + stationgridcell 
with open(stationfile,'w') as f:        
    f.write(station_header+'\n')
    for i in range(len(station_data)):          
        year = str(int(station_data.iloc[i,:][0]))        
        rowstr = year        
        for j in range(1,13):        
            if np.isnan(station_data.iloc[i,:][j]):            
                monthstr = str(-99.9)                
            else:                
                monthstr = str(np.round(station_data.iloc[i,:][j],1))                
            rowstr += f"{monthstr:>5}"          
        f.write(rowstr+'\n')
            
#------------------------------------------------------------------------------
print('** END')
            