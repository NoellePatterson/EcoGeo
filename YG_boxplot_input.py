import glob
import numpy as np
import csv
import math
import pandas as pd

start_year = 1992 # choose start year for metrics compilation, and collect all data until present
files = glob.glob("metric-data/*")
station_dict = {}
for file in files:
    currentFile = pd.read_csv(file, sep=',', header=None, index_col=0)
    if file == 'metric-data/Green_greendale_metrics.csv':
        station_dict['Greendale'] = currentFile
    elif file == 'metric-data/Green_jensen_metrics.csv':
        station_dict['Jensen'] = currentFile
    elif file == 'metric-data/Yampa_dlp_metrics.csv':
        station_dict['Yampa'] = currentFile

SP_Tim_Water = []
SP_Mag = []
SP_Dur = []
SP_ROC = [] 
DS_Dur_WS = []
gage_label = []

for currentFile in station_dict:
    currentData = station_dict[currentFile]
    for index, subyear in enumerate(currentData):
        if currentData.loc['Year'][index+1] < float(start_year):
            continue
        SP_Tim_Water.append(currentData.loc['SP_Tim_Water'][index+1])
        SP_Dur.append(currentData.loc['SP_Dur'][index+1])
        SP_ROC.append(currentData.loc['SP_ROC'][index+1])
        SP_Mag.append(currentData.loc['SP_Mag'][index+1])
        DS_Dur_WS.append(currentData.loc['DS_Dur_WS'][index+1])
        gage_label.append(currentFile)
    # import pdb; pdb.set_trace() 

"""Use tukey categories as first list element; either class names (new_array) or water year type (class_label)"""        
csv_outputs = [gage_label, SP_Tim_Water, SP_Dur, SP_ROC, SP_Mag, DS_Dur_WS]
csv_outputs_transpose = list(map(list, zip(*csv_outputs)))
header = ['groups', 'SP_Tim_Water', 'SP_Dur', 'SP_ROC', 'SP_Mag', 'DS_Dur_WS']
with open('boxplot_input.csv', 'w') as csvfile:
    resultsWriter = csv.writer(csvfile, dialect='excel')
    resultsWriter.writerows(csv_outputs_transpose)

from pandas import read_csv
df = read_csv('boxplot_input.csv')
df.columns = header
df.to_csv('boxplot_input.csv', index=False)