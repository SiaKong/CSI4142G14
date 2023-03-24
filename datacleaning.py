#Import statement
import pandas as pd
import numpy as np


# Read csv into dataframe
mh = pd.read_csv('mh.csv') # Mental Health
sr = pd.read_csv('sr.csv') # Suicide Rate
ur = pd.read_csv('ur.csv') # Unemployment Rate


# Drop unneeded columns
mh = mh.drop(columns=['index','Code'])
sr = sr.drop(columns=['country-year','HDI for year', 'generation'])
ur = ur.drop(columns=['Country Code'])


# Turn years of ur into a single ‘Year’ column and order the dataframe by country and year.
ur = ur.melt(id_vars=["Country Name"], var_name='Year', value_name='Unemployment Rate')
ur = ur.sort_values(by=['Country Name','Year'])


#Create list of countries in each dataframe.
mh_country = mh['Entity']
mh_country = mh_country.drop_duplicates()

ur_country = ur['Country Name']
ur_country = ur_country.drop_duplicates()

sr_country = sr['country']
sr_country = sr_country.drop_duplicates()


#Create list of all countries that exists in all three data frames.
in_country = pd.Series(list(set(mh_country).intersection(set(ur_country))))
in_country = pd.Series(list(set(in_country).intersection(set(sr_country))))


#Create list of all countries that exists in atleast one data frame.
out_country = pd.Series(list(set(mh_country).union(set(ur_country))))
out_country = pd.Series(list(set(out_country).union(set(sr_country))))


# Union of the series 
union = pd.Series(np.union1d(out_country, in_country))
  

# intersection of the series
intersect = pd.Series(np.intersect1d(out_country, in_country))
  

# uncommon elements in both the series 
uc = union[~union.isin(intersect)]
uc.to_csv('uc.csv')


# Manually analyzed uc.csv to find all instances
# of countries with more than one name. Then rename so all countries
# are named correctly.
ur.loc[ur["Country Name"] == "Bahamas, The", "Country Name"] = 'Bahamas'
ur.loc[ur["Country Name"] == "Congo, Rep.", "Country Name"] = 'Congo'
ur.loc[ur["Country Name"] == "Congo, Dem. Rep.", "Country Name"] = 'Democratic Republic of Congo'
ur.loc[ur["Country Name"] == "Egypt, Arab Rep.", "Country Name"] = "Egypt"
ur.loc[ur["Country Name"] == "Gambia, The", "Country Name"] = "Gambia"
ur.loc[ur["Country Name"] == "Hong Kong, SAR, China", "Country Name"] = "Hong Kong"
ur.loc[ur["Country Name"] == "Iran, Islamic Rep.", "Country Name"] = "Iran"
ur.loc[ur["Country Name"] == "Kyrgyz Republic", "Country Name"] = "Kyrgyzstan"
ur.loc[ur["Country Name"] == "Lao PDR", "Country Name"] = "Laos"
ur.loc[ur["Country Name"] == "Korea, Dem. People's Rep.", "Country Name"] = "North Korea"
ur.loc[ur["Country Name"] == "Macedonia", "Country Name"] = "North Macedonia"
ur.loc[ur["Country Name"] == "Russian Federation", "Country Name"] = "Russia"
ur.loc[ur["Country Name"] == "Slovak Republic", "Country Name"] = "Slovakia"
ur.loc[ur["Country Name"] == "Korean Republic", "Country Name"] = "South Korea"
ur.loc[ur["Country Name"] == "Syrian Arab Republic", "Country Name"] = "Syria"
ur.loc[ur["Country Name"] == "Timor", "Country Name"] = "Timor-Leste"
ur.loc[ur["Country Name"] == "Turkiye", "Country Name"] = "Turkey"
ur.loc[ur["Country Name"] == "Venezuela, RB", "Country Name"] = "Venezuela"
ur.loc[ur["Country Name"] == "Yemen, Rep.", "Country Name"] = "Yemen"


sr.loc[sr["country"] == "Bahamas, The", "country"] = 'Bahamas'
sr.loc[sr["country"] == "Congo, Rep.", "country"] = 'Congo'
sr.loc[sr["country"] == "Congo, Dem. Rep.", "country"] = 'Democratic Republic of Congo'
sr.loc[sr["country"] == "Egypt, Arab Rep.", "country"] = "Egypt"
sr.loc[sr["country"] == "Gambia, The", "country"] = "Gambia"
sr.loc[sr["country"] == "Hong Kong, SAR, China", "country"] = "Hong Kong"
sr.loc[sr["country"] == "Iran, Islamic Rep.", "country"] = "Iran"
sr.loc[sr["country"] == "Kyrgyz Republic", "country"] = "Kyrgyzstan"
sr.loc[sr["country"] == "Lao PDR", "country"] = "Laos"
sr.loc[sr["country"] == "Korea, Dem. People's Rep.", "country"] = "North Korea"
sr.loc[sr["country"] == "Macedonia", "country"] = "North Macedonia"
sr.loc[sr["country"] == "Russian Federation", "country"] = "Russia"
sr.loc[sr["country"] == "Slovak Republic", "country"] = "Slovakia"
sr.loc[sr["country"] == "Korean Republic", "country"] = "South Korea"
sr.loc[sr["country"] == "Syrian Arab Republic", "country"] = "Syria"
sr.loc[sr["country"] == "Timor", "country"] = "Timor-Leste"
sr.loc[sr["country"] == "Turkiye", "country"] = "Turkey"
sr.loc[sr["country"] == "Venezuela, RB", "country"] = "Venezuela"
sr.loc[sr["country"] == "Yemen, Rep.", "country"] = "Yemen"


mh.loc[mh["Entity"] == "Bahamas, The", "Entity"] = 'Bahamas'
mh.loc[mh["Entity"] == "Congo, Rep.", "Entity"] = 'Congo'
mh.loc[mh["Entity"] == "Congo, Dem. Rep.", "Entity"] = 'Democratic Republic of Congo'
mh.loc[mh["Entity"] == "Egypt, Arab Rep.", "Entity"] = "Egypt"
mh.loc[mh["Entity"] == "Gambia, The", "Entity"] = "Gambia"
mh.loc[mh["Entity"] == "Hong Kong, SAR, China", "Entity"] = "Hong Kong"
mh.loc[mh["Entity"] == "Iran, Islamic Rep.", "Entity"] = "Iran"
mh.loc[mh["Entity"] == "Kyrgyz Republic", "Entity"] = "Kyrgyzstan"
mh.loc[mh["Entity"] == "Lao PDR", "Entity"] = "Laos"
mh.loc[mh["Entity"] == "Korea, Dem. People's Rep.", "Entity"] = "North Korea"
mh.loc[mh["Entity"] == "Macedonia", "Entity"] = "North Macedonia"
mh.loc[mh["Entity"] == "Russian Federation", "Entity"] = "Russia"
mh.loc[mh["Entity"] == "Slovak Republic", "Entity"] = "Slovakia"
mh.loc[mh["Entity"] == "Korean Republic", "Entity"] = "South Korea"
mh.loc[mh["Entity"] == "Syrian Arab Republic", "Entity"] = "Syria"
mh.loc[mh["Entity"] == "Timor", "Entity"] = "Timor-Leste"
mh.loc[mh["Entity"] == "Turkiye", "Entity"] = "Turkey"
mh.loc[mh["Entity"] == "Venezuela, RB", "Entity"] = "Venezuela"
mh.loc[mh["Entity"] == "Yemen, Rep.", "Entity"] = "Yemen"


# Must repeat this step to account for renamed countries
mh_country = mh['Entity']
mh_country = mh_country.drop_duplicates()

ur_country = ur['Country Name']
ur_country = ur_country.drop_duplicates()

sr_country = sr['country']
sr_country = sr_country.drop_duplicates()

in_country = pd.Series(list(set(mh_country).intersection(set(ur_country))))
in_country = pd.Series(list(set(in_country).intersection(set(sr_country))))

out_country = pd.Series(list(set(mh_country).union(set(ur_country))))
out_country = pd.Series(list(set(out_country).union(set(sr_country))))

union = pd.Series(np.union1d(out_country, in_country))
  

# intersection of the series
intersect = pd.Series(np.intersect1d(out_country, in_country))
  
  
# uncommon elements in both the series 
uc = union[~union.isin(intersect)]








# Remove countries that do not exist in all 3 data sets.
mh = mh.loc[~mh['Entity'].isin(uc)]
sr = sr.loc[~sr['country'].isin(uc)]
ur = ur.loc[~ur['Country Name'].isin(uc)]








# Manually modified column names as follows
#sr: Country -> Country, year -> Year, sex -> Sex
#mh: Entity -> Country
#ur: Country Name -> Country










