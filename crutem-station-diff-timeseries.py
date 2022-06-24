#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# PROGRAM: crutem-station-diff-timeseries.py
#------------------------------------------------------------------------------
# Version 0.1
# 20 June, 2022
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
from datetime import datetime
# Plotting libraries:
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

fontsize = 16
ncol = 12
nheader = 1
nsmooth = 12

use_nearest = False # ( default = False )
#stationcode_nearest = '124000' # Zielona Gora
#stationcode_nearest = '104960' # Cottbus

#stationcode = '010020'
#stationcode = '010060'
#stationcode = '010080'
#stationcode = '010090'
#stationcode = '200460'
#stationcode = '200260'
#stationcode = '200340'
#stationcode = '200490'
stationcode = 'zagan'

station_file = 'DATA/' + stationcode + '.csv'
crutem_pkl = 'DATA/df_temp.pkl'

#------------------------------------------------------------------------------
# LOAD: station archive into Pandas dataframe
#------------------------------------------------------------------------------

df_temp = pd.read_pickle( crutem_pkl, compression='bz2' )    
stationcodelist = df_temp.stationcode.unique()

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
# EXTRACT: station from CRUTEM pkl archive --> df_2
#------------------------------------------------------------------------------

stationcode = header.split()[0]
stationname = header.split()[4]

if use_nearest == True: stationcode = stationcode_nearest					
station_metadata = df_temp[df_temp['stationcode']==stationcode]

if len(station_metadata.index) > 0:

    df_2 = df_temp[ df_temp.stationcode == stationcode ].iloc[:,0:13].reset_index(drop=True)
    
    # ALIGN: time axes
        
    yearmin = np.min( [ df_1.year.min(), df_2.year.min() ] )
    yearmax = np.max( [ df_1.year.max(), df_2.year.max() ] )
    t_full = np.arange( yearmin, yearmax + 1 )
    df_full = pd.DataFrame( {'year':t_full} )
    da = df_full.merge( df_1, how='left', on='year' ) # station
    db = df_full.merge( df_2, how='left', on='year' ) # CRUTEM station
       
    # EXTRACT: timeseries

    t = pd.date_range( start=str(da.year.iloc[0]), end=str(da.year.iloc[-1]+1), freq='MS')[0:-1]                                                                                                                                          
    ts_1 = []    
    ts_2 = []    
    for i in range(len(da)):            
        monthly_1 = da.iloc[i,1:13]
        monthly_2 = db.iloc[i,1:13]
        ts_1 = ts_1 + monthly_1.to_list()    
        ts_2 = ts_2 + monthly_2.to_list()    
    ts_1 = np.array( ts_1 )   
    ts_2 = np.array( ts_2 )   
                
    # COMPUTE: difference series
    
    ts_diff = ts_2 - ts_1 # CRUTEM - ingest
    
    # COMPUTE: monthly differences
    
    station_diff = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
    station_diff['year'] = da.year
    for j in range(1,13): station_diff[str(j)] = da[str(j)].values - db[str(j)].values
    
else:

    print('station not in archive')
    
    # SET: time axis

    yearmin = np.min( [ df_1.year.min() ] )
    yearmax = np.max( [ df_1.year.max() ] )
    t_full = np.arange( yearmin, yearmax + 1 )
    df_full = pd.DataFrame( {'year':t_full} )
    da = df_full.merge( df_1, how='left', on='year' ) # station
       
    # EXTRACT: timeseries

    t = pd.date_range( start=str(da.year.iloc[0]), end=str(da.year.iloc[-1]+1), freq='MS')[0:-1]                                                                                                                                          
    ts_1 = []    
    for i in range(len(da)):            
        monthly_1 = da.iloc[i,1:13]
        ts_1 = ts_1 + monthly_1.to_list()    
    ts_1 = np.array( ts_1 )   

    # SET: difference series = np.nan

    ts_2 = ts_1 * np.nan
    ts_diff = ts_1 * np.nan
    
    station_diff = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
    station_diff['year'] = da.year
    for j in range(1,13): station_diff[str(j)] = da[str(j)].values * np.nan
    
#------------------------------------------------------------------------------
# PLOT: timeseries
#------------------------------------------------------------------------------
    
figstr = stationcode + '_' + 'station_diff_timeseries.png'
titlestr = stationcode + ': ' + stationname
xstr = 'Year'
ystr1 = '2m Temperature, °C'
ystr2 = 'Difference, °C'     
ystr3 = 'Difference, °C'     

fig = plt.figure( figsize=(15,10) )          

ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2, sharex = ax1)
ax3 = fig.add_subplot(3, 1, 3, sharey = ax2)

ax1.plot( t, pd.Series( ts_2 ).rolling(nsmooth).mean(), 'o-', alpha=0.5, label='station (CRUTEM): ' + str(nsmooth) + 'm MA' )
ax1.plot( t, pd.Series( ts_1 ).rolling(nsmooth).mean(), '.-', alpha=0.5, label='station (candidate): ' + str(nsmooth) + 'm MA' )
ax1.tick_params(labelsize=fontsize)    
ax1.legend(loc='upper left', fontsize=12)
ax1.set_ylabel(ystr1, fontsize=fontsize)
ax1.set_title(titlestr, fontsize=fontsize)

ax2.plot( t, pd.Series( ts_diff ).rolling(12).mean(), '.-', color='teal', alpha=0.5)
ax2.tick_params(labelsize=fontsize)    
ax2.set_ylabel(ystr2, fontsize=fontsize)

for i in range(1,13): ax3.plot(station_diff['year'], station_diff[str(i)], 'o', alpha=0.5, label=str(i).zfill(2) )
ax3.tick_params(labelsize=fontsize)    
ax3.set_xlabel(xstr, fontsize=fontsize)
ax3.set_ylabel(ystr3, fontsize=fontsize)
ax3.legend(loc='upper left', ncol=ncol, fontsize=12)

plt.savefig(figstr, dpi=300, bbox_inches='tight')
plt.close(fig)
    
#------------------------------------------------------------------------------
print('** END')
            
