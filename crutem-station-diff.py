#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# PROGRAM: crutem-station-diff.py
#------------------------------------------------------------------------------
# Version 0.1
# 17 June, 2022
# Michael Taylor
# https://patternizer.github.io
# patternizer AT gmail DOT com
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------
# Dataframe libraries:
import numpy as np
import pandas as pd
import pickle
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

fontsize = 16
ncol = 4
nheader = 1

#stationcode = '010020'
#stationcode = '010060'
stationcode = '010080'
#stationcode = '010090'
#stationcode = '200460'
#stationcode = '200260'
#stationcode = '200340'
#stationcode = '200490'
#stationcode = 'zagan'

station_file = 'DATA/' + stationcode + '.csv'
crutem_pkl = 'DATA/df_temp.pkl'

#------------------------------------------------------------------------------
# LOAD: station archive into Pandas dataframe
#------------------------------------------------------------------------------

df_temp = pd.read_pickle( crutem_pkl, compression='bz2' )    

#------------------------------------------------------------------------------
# LOAD: station file into Pandas dataframe --> df_1
#------------------------------------------------------------------------------

f = open(station_file)
lines = f.readlines()   
dates = []
vals = []
for i in range(nheader,len(lines)):    
    header = lines[0]
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
    df_1[ df_1.columns[j] ] = [ vals[i][j-1] for i in range(len(df_1)) ]

# CONVERT: to INT (x10) temperatures to float and rescale to degC

for j in range(1,13): df_1[ str(j) ] = df_1[ str(j) ].astype(float) / 10.

# REPLACE: fill value = -99.9 with np.nan

df_1 = df_1.replace( -99.9, np.nan )
    
#------------------------------------------------------------------------------
# EXTRACT: station from CRUTEM pkl archive file --> df_2
#------------------------------------------------------------------------------

stationcode = header.split()[0]
station_metadata = df_temp[df_temp['stationcode']==stationcode]
stationname = station_metadata.stationname.unique()

if len(station_metadata.index) > 0:

    df_2 = df_temp[ df_temp.stationcode == stationcode ].iloc[:,0:13].reset_index(drop=True)
    
    # ALIGN: time axes
        
    yearmin = np.min( [ df_1.year.min(), df_2.year.min() ] )
    yearmax = np.max( [ df_1.year.max(), df_2.year.max() ] )
    t_full = np.arange( yearmin, yearmax + 1 )
    df_full = pd.DataFrame( {'year':t_full} )
    da = df_full.merge( df_1, how='left', on='year' )
    db = df_full.merge( df_2, how='left', on='year' )
       
    # CALCULATE: differences
    
    station_diff = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
    station_diff['year'] = da.year
    for j in range(1,13): station_diff[str(j)] = da[str(j)].values - db[str(j)].values
            
    # CONVERT: to CRUTEM scaled integers

    for j in range(1,13): station_diff[str(j)] = station_diff[str(j)].values * 10.
    
    # FILL VALUE: = -999
    
    station_diff = station_diff.replace( np.nan, -999 )

    # CONVERT: to INT
    
    station_diff = station_diff.astype(int)

    # SAVE: difference file in CRUTEM format
    
    stationfile = stationcode + '-diff.csv'
    station_data = station_diff.iloc[:,range(0,13)]

    with open(stationfile,'w') as f:        
        f.write( header )
        for i in range(len(station_data)):          
            year = str( station_data.iloc[i,:][0] )        
            rowstr = year        
            for j in range(1,13): 
                monthstr = str( station_data.iloc[i,:][j] )                
                rowstr += f"{monthstr:>5}"          
            f.write(rowstr+'\n')
            
else:
	
	print(stationcode + ' not in archive')            
                            
#------------------------------------------------------------------------------
print('** END')
            
