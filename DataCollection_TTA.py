# Imports
from pytrends.request import TrendReq
import calendar
from datetime import date, timedelta, datetime
from isoweek import Week
import pandas as pd
import time

# Settings for searchs
pytrends = TrendReq(hl='en-US')
kw_list = ['bitcoin']

# Step 1: requesting a monthly time series, normalized using all data points
timeframe = 'all'
pytrends.build_payload(kw_list = kw_list,                       
                       timeframe = timeframe,
                       cat = '0', geo = '', gprop ='' )

monthly_data = pytrends.interest_over_time()
monthly_data.reset_index(drop=False, inplace=True)
monthly_data['year'] = monthly_data['date'].apply(lambda x: x.year)
monthly_data['month'] = monthly_data['date'].apply(lambda x: x.month)

monthly_data.rename(columns={'bitcoin':'n_m_y'},inplace=True)

# Step 2: requesting a dayly time series, normalized by month
def get_data():    
    pytrends.build_payload(kw_list = kw_list,                       
                    timeframe = timeframe,
                    cat = '0', geo = '', gprop ='' )
    time.sleep(0.5)    
    return pytrends.interest_over_time()

print('Downloadind data for:')      
today_year = date.today().year    
today_month = date.today().month  
for year in range(2015,today_year+1):
    for month in range(1,13):
        print(str(year)+'-'+str(month))
        number_days = calendar.monthrange(year, month)[1]
        timeframe = f'{year}-{month}-01 {year}-{month}-{number_days}'
                        
        if year==2015 and month==1:
            daily_data = get_data()
        else:
            if year<today_year:
                daily_data = vertical_concat = pd.concat([daily_data, get_data()], axis=0)
            else:
                if month<(today_month):
                    daily_data = vertical_concat = pd.concat([daily_data, get_data()], axis=0)
            
                    
daily_data.reset_index(drop=False, inplace=True)
daily_data.rename(columns={'bitcoin':'n_d_m_y'}, inplace=True)

# Step 3: Re-normalizing dayly data, using all data points
daily_data['year'] = daily_data['date'].apply(lambda x: x.year)
daily_data['month'] = daily_data['date'].apply(lambda x: x.month)

# using equation 1 in secction 2
db_aux = daily_data.groupby(['year','month'])[['n_d_m_y']].sum().reset_index(drop=False)
db_aux.rename(columns={'n_d_m_y':'sum_n_d_m_y'}, inplace=True)
db_aux = db_aux.merge(monthly_data, how='left', left_on=['year','month'], right_on=['year','month'])

# using equation 2 in secction 2
db_aux['weight'] = 1/db_aux['sum_n_d_m_y']*db_aux['n_m_y']
db_aux = db_aux[['year','month','weight']]

# using equation 3 in secction 2
daily_data = daily_data.merge(db_aux, how='left', left_on=['year','month'], right_on=['year','month'])
daily_data['n_d_m_y_normalized'] = daily_data['n_d_m_y']*daily_data['weight']

# using equation 4 in secction 2
daily_data['n_d_m_y_normalized'] = 100*daily_data['n_d_m_y_normalized']/daily_data['n_d_m_y_normalized'].max()
daily_data = daily_data[['date','n_d_m_y_normalized']]


# Step 4: calculating weekly data, 
daily_data['iso_year'] = daily_data['date'].apply(lambda x: x.isocalendar()[0])
daily_data['iso_week'] = daily_data['date'].apply(lambda x: x.isocalendar()[1])

weekly_data = daily_data.groupby(['iso_year','iso_week']).agg({'n_d_m_y_normalized':'sum','date':lambda x: x.iloc[0]})
weekly_data.rename(columns={'n_d_m_y_normalized':'n_w_y_normalized'}, inplace=True)
weekly_data.reset_index(drop=False, inplace=True)
# Normalizing all data points
weekly_data['n_w_y_normalized'] = 100*weekly_data['n_w_y_normalized']/weekly_data['n_w_y_normalized'].max()

# selecting main variables
weekly_data = weekly_data[['date','n_w_y_normalized']]
daily_data = daily_data[['date','n_d_m_y_normalized']]

# saving required datasets
daily_data.to_csv('DataCollection_Solution_daily_data.csv', index=False)
weekly_data.to_csv('DataCollection_Solution_weekly_data.csv', index=False)
print('Requested files have been saved.')