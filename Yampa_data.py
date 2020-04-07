import pandas as pd
from datetime import datetime
from climata.usgs import DailyValueIO
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

'''
15 min to daily project, uncomment here to use
'''
# pull up 15 minute data
# filename = 'yampa_height.csv'
# data = pd.read_csv(filename)

# # create dict of empty ordered daily entries
# data_by_date = {}
# dates, i = np.unique(data['date'], return_index=True)
# dates = dates[np.argsort(i)]
# for date in dates:
#     data_by_date[date] = []

# # populate dict entries with array of height values for each date
# for index, row in data.iterrows():
#     date = row['date']
#     try: # convert height values to float, if possible
#         data_by_date[date].append(np.float(row['height']))
#     except: # if not possible it's probably because the value is "ice"
#         data_by_date[date].append(row['height'])

# ht_min = []
# ht_max = []
# ht_avg = []

# for index, date in enumerate(dates):
#     try:
#         ht_min.append(np.nanmin(data_by_date[date]))
#         ht_max.append(np.nanmax(data_by_date[date]))
#         ht_avg.append(np.nanmean(data_by_date[date]))
#     except: # try removing strings in case it is a partial ice day
#         updated_height = []
#         for height in data_by_date[date]:
#             if type(height) == float:
#                 updated_height.append(height)
#         try: # try taking stats if the day had some numerical values
#             ht_min.append(np.nanmin(updated_height))
#             ht_max.append(np.nanmax(updated_height))
#             ht_avg.append(np.nanmean(updated_height))
#         except: # if no numerical values for a day, assume it's "ice"
#             ht_min.append('Ice')
#             ht_max.append('Ice')
#             ht_avg.append('Ice')

# ht_stats = pd.DataFrame(list(zip(dates,ht_min,ht_max,ht_avg)),columns =['date','min','max','average'])

# ht_stats.to_csv('Yampa_daily_height.csv',index=False)

'''
easy USGS data import code, uncomment here to use
'''
# set parameters, deerlodge
# start_day = pd.to_datetime("1982-10-1")
# end_day = pd.to_datetime("2019-06-01")
# num_days = (end_day-start_day).days
# datelist = pd.date_range(end=pd.datetime.today(), periods=num_days).tolist()
# station_id = "09260050"
# param_id = "00060"

# set parameters, Greendale
start_day = pd.to_datetime("1928-10-01")
end_day = pd.to_datetime("2020-03-25")
num_days = (end_day-start_day).days
station_id = "11046500"
param_id = "00060"
# flow is 00060, temperature is 00010


data = DailyValueIO(
    start_date=start_day,
    end_date=end_day,
    station=station_id,
    parameter=param_id,
)

for series in data:
    dates = [r[0] for r in series.data]
    date_print = [r[0].strftime("%m-%d-%Y") for r in series.data]
    cfs_flow = [r[1] for r in series.data]
    cms_flow = [r[1]*.0283168 for r in series.data]

data = {'date':date_print, 'cms_flow':cms_flow, 'flow':cfs_flow}
flow_csv = pd.DataFrame(data)
flow_csv[['date','flow']].to_csv("data_updates.csv", sep=',', index=False)
plt.plot(dates, cms_flow)
plt.ylabel(r'Flow $(m^3/s)$', fontsize = 18)
# plt.ylim(0,20000*.0283168)
plt.title(series.site_name, fontsize=22)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.margins(0.2)
plt.show()


