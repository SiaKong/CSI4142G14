#Import statement
import pandas as pd


# Read csv into dataframe
sr = pd.read_csv('Suicide Rate.csv')
mh = pd.read_csv('Mental Health.csv')
ur = pd.read_csv('Unemployment Rate.csv')


# Merge the dataframes on Country and Year (shared in all three dataframes)
all = sr.merge(mh, on=['Country', 'Year'], how='inner')
all = all.merge(ur, on=['Country', 'Year'], how='inner')


# Export merged file
all.to_csv('master.csv')

