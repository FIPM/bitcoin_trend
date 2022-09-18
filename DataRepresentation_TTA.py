# Installs
# pip install pandas

# Imports
import pandas as pd
from datetime import date
import os

# Uploading data
main_folder = os.getcwd()
monthly_data = pd.read_csv(os.path.join(main_folder,'raw_data','monthly_data.csv'))
weekly_data = pd.read_csv(os.path.join(main_folder,'raw_data','weekly_data.csv'))
hourly_data = pd.read_csv(os.path.join(main_folder,'raw_data','hourly_data.csv'))

# Creating key variables to merge datasets
monthly_data['year'] = monthly_data['date'].apply(lambda x: date.fromisoformat(x).year)
monthly_data['month'] = monthly_data['date'].apply(lambda x: date.fromisoformat(x).month)
monthly_data['value_month']=monthly_data['value_month']/100

weekly_data['year'] = weekly_data['date'].apply(lambda x: date.fromisoformat(x).year)
weekly_data['month'] = weekly_data['date'].apply(lambda x: date.fromisoformat(x).month)
weekly_data['iso_year'] = weekly_data['date'].apply(lambda x: date.fromisoformat(x).isocalendar()[0])
weekly_data['iso_week'] = weekly_data['date'].apply(lambda x: date.fromisoformat(x).isocalendar()[1])
weekly_data['value_week']=weekly_data['value_week']/100

hourly_data['year'] = hourly_data['date'].apply(lambda x: date.fromisoformat(x.split(' ')[0]).year)
hourly_data['month'] = hourly_data['date'].apply(lambda x: date.fromisoformat(x.split(' ')[0]).month)
hourly_data['iso_year'] = hourly_data['date'].apply(lambda x: date.fromisoformat(x.split(' ')[0]).isocalendar()[0])
hourly_data['iso_week'] = hourly_data['date'].apply(lambda x: date.fromisoformat(x.split(' ')[0]).isocalendar()[1])
hourly_data['value_hour']=hourly_data['value_hour']/100

# Renaming column in monthly_data
db_n_m_y_monthly = monthly_data[['year','month','value_month']].rename(columns={'value_month':'n_m_y_montly'})

# Calculating Equation 2
db_n_m_y = weekly_data.groupby(['year','month'])[['value_week']].sum().rename(columns={'value_week':'sum_value_week'}).reset_index(drop=False)
db_n_m_y['n_w_m_y'] = db_n_m_y['sum_value_week']
db_n_m_y = db_n_m_y[['year','month','n_w_m_y']]

# Calculating Equation 3
db_n_w_m_y_montly = weekly_data.merge(db_n_m_y.merge(db_n_m_y_monthly, how='left', left_on=['year','month'], right_on=['year','month']),
                  how='left', left_on=['year','month'], right_on=['year','month'])
db_n_w_m_y_montly['n_w_m_y_montly'] = db_n_w_m_y_montly['value_week']/db_n_w_m_y_montly['n_w_m_y']*db_n_w_m_y_montly['n_m_y_montly']
db_n_w_m_y_montly = db_n_w_m_y_montly[['iso_year','iso_week','n_w_m_y_montly']]

# Calculation Equation 1
db_n_w_m_y = hourly_data.groupby(['iso_year','iso_week'])[['value_hour']].sum().rename(columns={'value_hour':'n_w_m_y'}).reset_index(drop=False)
db_n_h_d_w_m_y = hourly_data.merge(db_n_w_m_y.merge(db_n_w_m_y_montly, how='left', left_on=['iso_year','iso_week'], right_on=['iso_year','iso_week']),
                  how='left', left_on=['iso_year','iso_week'], right_on=['iso_year','iso_week'])

# Calculation Equation 4 (calculating the comparable/consistent version of the values in the houly_data file)
db_n_h_d_w_m_y['n_h_d_w_m_y_monthly'] = db_n_h_d_w_m_y['value_hour']/db_n_h_d_w_m_y['n_w_m_y']*db_n_h_d_w_m_y['n_w_m_y_montly']

# Calculation Equation 5 (Normalization)
db_n_h_d_w_m_y['n_h_d_w_m_y'] = 100*db_n_h_d_w_m_y['n_h_d_w_m_y_monthly']/db_n_h_d_w_m_y['n_h_d_w_m_y_monthly'].max()
db_n_h_d_w_m_y = db_n_h_d_w_m_y[['time_hour','date','n_h_d_w_m_y']]

# There are some missing values because the weekly_data and hourly_data do not have the same number of iso weeks. 

print('Maximum value of the consistent version of the values in the houly_data file: '+str(db_n_h_d_w_m_y['n_h_d_w_m_y'].max()))

# saving required datasets
db_n_h_d_w_m_y.to_csv('DataRepresentation_Solution_hourly_data.csv', index=False)
print('Requested files have been saved.')