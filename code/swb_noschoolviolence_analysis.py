import pandas as pd
import numpy as np
#import plotnine as ggplot
import sys

import pandas as pd

from geopy
#from geopy.geocoders import Nominatim

import requests
import urllib
import time

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

analysis_dir = "../"
sys.path.append(analysis_dir)

# Load NoSchoolViolence Data
df = pd.read_csv(analysis_dir + 'data/K-12 SSDB (Public).csv')
df.head()

"""# Part 1: Supplement School Violence Data

### Socioeconomic data from Census

1. Look up the latitude, longitude for each school within the school datasets.
2. Finds the county FIPS code for each lat, long
3. Joins census data on FIPS

***Limitations:*** Lookup is current and may not find school which have changed locations since the violance incident was logged in the NoSchoolViolence DB.


"""

def add_coordinates(x):
  """
  Add longitude and latitude to NoSchoolViolence DB

  x: row in pandas.Dataframe containing columsn for School, City, State
  """

  try:
    location = geolocator.geocode("{} {}, {}".format(x['School'], x['City'], x['State']))
  except:
    location = None
  if location is None:
    x['latitude'] = np.nan
    x['longitude'] = np.nan
  else:
    x['latitude'] = location.latitude
    x['longitude'] = location.longitude
  time.sleep(1)
  print(str(x.idx) + ': ' + str(x['latitude']))
  return x

def get_FIPS(lat, lon, fips):

  """
  Looks up Census FIPS given a lat, long


  lat: latitude (float)
  lon: longitude (float)
  fips: np.nan if not run before (int)


  """

  if not pd.isnull(fips):
    return fips

  #Sample latitude and longitudes
  if pd.isnull(lat):
    return np.nan

  #Encode parameters
  params = urllib.parse.urlencode({'latitude': lat, 'longitude':lon, 'format':'json'})
  #Contruct request URL
  url = 'https://geo.fcc.gov/api/census/block/find?' + params

  #Get response from API

  response = requests.get(url)
  print(response)
  print(url)
  #Parse json in response
  try:
    data = response.json()
  except:
    return np.nan

  #Print FIPS code
  time.sleep(1)

  return data['County']['FIPS']

# Initialize Nominatim API - we use this api to run the search
geolocator = geopy.geocoders.Nominatim(user_agent="MyApp")

add_lat_long = False # change to True if running this code for the first time. Takes ~2 hours to complete for. ~1,500 schools

if add_lat_long:
  # add lat, long
  df['idx'] = df.index
  df = df.apply(add_coordinates, axis=1)
  df.to_csv(analysis_dir + 'data/K-12 SSDB (Public)_with_coordinates.csv')

  # add FIPS
  df['FIPS'] = np.nan
  df['FIPS'] = df.apply(lambda x : get_FIPS(x['latitude'], x['longitude'], x['FIPS']), axis=1)
  df.to_csv(analysis_dir + 'K-12 SSDB (Public)_with_FIPS.csv')
else:
  df = pd.read_csv(analysis_dir + 'data/K-12 SSDB (Public)_with_FIPS.csv')

"""### Add Census Data

Census data can be retrieved using the `censusdata` package. However it is much easier and faster to access census data from https://www.nhgis.org/


I also calculate the diversity of the community using the Shannon Diversity index:
https://www.statology.org/shannon-diversity-index/

"""

key = '0a5a2fa2a4794c69a13e1bc8f6c57c60af6a4315' # You don't need the census key for the data when pulling data from https://www.nhgis.org/

supplemental_census = pd.read_csv(analysis_dir + 'data/nhgis0001_ds254_20215_county.csv', encoding = "ISO-8859-1")

# create single FIPS code3 for supplemental data
supplemental_census['COUNTYA'] = supplemental_census['COUNTYA'].astype(str)
supplemental_census['STATEA'] = supplemental_census['STATEA'].astype(str)
supplemental_census['COUNTYA'] = supplemental_census['COUNTYA'].apply(lambda x : '00' + x if len(x)==1 else x)
supplemental_census['COUNTYA'] = supplemental_census['COUNTYA'].apply(lambda x : '0' + x if len(x)==2 else x)
supplemental_census['FIPS'] = supplemental_census['STATEA'] + supplemental_census['COUNTYA']
supplemental_census['FIPS'] = supplemental_census['FIPS'].astype(int)

# Calculate Shannon Diversity Index
supplemental_census['HighSchool_grad_rate'] = (supplemental_census['AOP8E017'] + supplemental_census['AOP8E018'])/supplemental_census['AOP8E001']
supplemental_census['below_poverty_rate'] = (supplemental_census['AOXWE002'] + supplemental_census['AOXWE003'])/supplemental_census['AOXWE001']
supplemental_census['food_assistance'] = supplemental_census['AOQ3E002']/supplemental_census['AOQ3E001']
supplemental_census['unemployment'] = 1 - supplemental_census['AOSJE004']/supplemental_census['AOSJE003']
supplemental_census['Two or more'] = supplemental_census[['AON5M008', 'AON5M009', 'AON5M010']].sum(axis=1)

col_rename = {'AOQIE001': 'median_household_income',
              'AON5M002': 'White',
              'AON5M003': 'Black',
              'AON5M004': 'American Indian',
              'AON5M005': 'Asian',
              'AON5M006': 'Pacific Islander',
              'AON5M007': 'Other',
              }
supplemental_census.rename(columns=col_rename, inplace=True)

# First Diversity Index: Shannon Index
races = ['White', 'Black', 'American Indian', 'Asian', 'Pacific Islander', 'Other']

supplemental_census['Total'] = supplemental_census[races].sum(axis=1)
supplemental_census[races] = supplemental_census[races].div(supplemental_census['Total'], axis=0)
supplemental_census['Shannon_index'] = (supplemental_census[races]*np.log(supplemental_census[races])).sum(axis=1) # Entropy -- lower means more diverse

# Final Variables
final_cols = ['Shannon_index', 'HighSchool_grad_rate', 'below_poverty_rate',
              'median_household_income', 'unemployment', 'food_assistance', 'FIPS', 'Total', 'COUNTY', 'STATE']
supplemental_census = supplemental_census[final_cols]

"""## Add Crime Data

Crime data at the county level is very difficult to acquire. The closest thing is the FBI UCR database: https://cde.ucr.cjis.gov/LATEST/webapp/#. But you have to download a 4GB master file and the data is very messy. Someone has already [aggregated some crime data in 2001.](https://www.icpsr.umich.edu/web/NACJD/studies/3451/variables?start=0&STUDYQ=3451&EXTERNAL_FLAG=1&ARCHIVE=NACJD&sort=STUDYID%20asc%2CDATASETID%20asc%2CSTARTPOS%20asc&rows=50&q=ds1) For simplicity I use this analysis.
"""

supplemental_crime = pd.read_csv(analysis_dir + 'data/UCI_crimedata_2001.csv')

supplemental_crime.columns

supplemental_crime.head()

cols = ['FIPS_ST', 'FIPS_CTY', # FIPS identifiers
        'GRNDTOT', # total crimes resolving in an arrest
        'DRUGTOT', # total drug related crimes
        'WEAPONS'] # total crimes involving weapons possession
supplemental_crime = supplemental_crime[cols]

supplemental_crime['FIPS_CTY'] = supplemental_crime['FIPS_CTY'].astype(int).astype(str)
supplemental_crime['FIPS_ST'] = supplemental_crime['FIPS_ST'].astype(int).astype(str)
supplemental_crime['FIPS_CTY'] = supplemental_crime['FIPS_CTY'].apply(lambda x : '00' + x if len(x)==1 else x)
supplemental_crime['FIPS_CTY'] = supplemental_crime['FIPS_CTY'].apply(lambda x : '0' + x if len(x)==2 else x)
supplemental_crime['FIPS'] = supplemental_crime['FIPS_ST'] + supplemental_crime['FIPS_CTY']
supplemental_crime['FIPS'] = supplemental_crime['FIPS'].astype(int)

supplemental_data = pd.merge(supplemental_crime, supplemental_census, how='inner', on='FIPS')

crime_cols = ['GRNDTOT', 'DRUGTOT', 'WEAPONS']

#convert to percentiles
supplemental_data[crime_cols] = supplemental_data[crime_cols].div(supplemental_data['Total'], axis=0).rank(pct=True)

supplemental_data.to_csv(analysis_dir + 'data/K-12 SSDB (Public)_w_supplemental_data.csv')

"""# Analysis

## Approach
- I avoid use a probabilistic model since we do not have data on schools without incidents of violence. Though there is the [SSOCS survey ](https://www.census.gov/programs-surveys/ssocs.html) from the census which might have this data.
- Instead I use an empirical approach which measures correlation between variables and incidents of violance.
- The statement I intent to make is

Step 1: Split the variables into quantiles.


```
Graduation Rate --> [0-25%, 26-50%, 51-75%, 76-100%] percentiles
```

Step 2: Calculate the percent of violance incidents from the School Violence Database occure within each decile.


```
Graduation Rate:
0-25%: 74% occurance rate
26-50%: 16%
51-75%: 7%
76-100%: 3%
```

Step 3: Categorize the risk level from ranking the quantiles by occurace rate

```
Graduation Rate:
0-25%: 74% [High Risk]
26-50%: 16% [Medium Risk
51-75%: 7% [Low Risk]
76-100%: 3%  [Very Low Risk]
```

Step 4: User inputes their school's location. The algorithm looks up the demographics (quantiles) for their county, and returns which variables are "High Risk"

```
Graduation Rate:
0-25%: 74% [High Risk]
26-50%: 16% [Medium Risk
51-75%: 7% [Low Risk]
76-100%: 3%  [Very Low Risk]
```


<hr>

##Limitations


**Variables I am missing that are in the POC questionnaire**
- Number of staff
- gendar ratio
- Total enrollment
- % dientifying differently
- Percent ethnicity
"""

analysis_df = supplemental_data.copy() #pd.read_csv(data_dir + 'supplemental_data.csv')

# convert data columns to percentiles and high, med, low
vars = ['GRNDTOT', # strong correlation
             'Shannon_index', # revisit
             'median_household_income', #inverse correlation
             'food_assistance', # ??
             'unemployment', # strong correlation
             'HighSchool_grad_rate', # strong correlation
             'School Type', # strong correlation
             'During School Day (Y/N)', # not useful
             'Bullied (Y/N/ N/A)',  # not useful
             'Day of week (formula)', # strong correlation
             'During a Sporting Event (Y/N)', # not useful
             'Victims Race', # not useful
              'HoD'] # strong correlation

# calculate quantiles for these variables
quantiles = ['GRNDTOT',
             'Shannon_index',
             'median_household_income',
             'unemployment',
             'HighSchool_grad_rate',
             'food_assistance']

# Calculate quantiles
for col in quantiles:
  analysis_df[col] = pd.cut(analysis_df[col].rank(pct=True), [0, .25, .5, .75, 1.0 ]) # higher percentile means for diverse

# join to NoSchoolViolence
df.FIPS = df.FIPS.fillna(-1)
df.FIPS = df.FIPS.astype(int)

NoSchoolViolence = pd.merge(df, analysis_df, how='left', on='FIPS')

NoSchoolViolence['HoD'] = pd.to_datetime(df['Time of Occurrence (12 hour AM/PM)']).dt.hour

# incidents per school
NoSchoolViolence.groupby('School')['School'].count().sort_values().hist()

# incidents per county
NoSchoolViolence.groupby('FIPS')['FIPS'].count().sort_values().hist(bins=100)

for col in vars:
  NoSchoolViolence[col].value_counts().sort_index().plot(kind='bar', title=col)
  plt.show()

"""## Run Inference"""

se_factors = ['GRNDTOT', # strong correlation
             'Shannon_index', # revisit
             'median_household_income', #inverse correlation
             'unemployment', # strong correlation
             'HighSchool_grad_rate'] # strong correlation


other_factors = ['School Type', # strong correlation
             'During School Day (Y/N)', # weak correlation
             'Bullied (Y/N/ N/A)',  # weak correlation
             'Day of week (formula)', # strong correlation
             'During a Sporting Event (Y/N)', # weak correlation
             'Victims Race', # weak correlation
              'HoD'] # strong correlation

# Step 3 - calculate violence occurance rate in violence database
se_lookup = NoSchoolViolence[se_factors].apply(lambda x : x.value_counts('perc')) #
col_map = { 'GRNDTOT':'Crime Rate', 'Shannon_index':'Community Diversity',
           'median_household_income':'Median Income', 'unemployment': 'Unemployment Rate',
            'HighSchool_grad_rate':'High School Graduation Rate'}
se_lookup.rename(columns = col_map, inplace=True)

# Melt data into a lookup table we can merge with later
se_lookup = pd.melt(se_lookup.reset_index(), value_vars=se_lookup.columns, var_name='factor', value_name='perc', id_vars='index')

# Step 4 - Rank by occurance level
se_lookup['rk'] = se_lookup.groupby('factor')['perc'].rank(ascending=False)
mapping = pd.DataFrame({'rk':[1,2,3,4], 'risk_level':['high', 'medium', 'low', 'very low']})
se_lookup = pd.merge(se_lookup, mapping, on='rk', how='inner')
se_lookup.head()



"""## Save Everything we need for the Demo"""

analysis_df.rename(columns=col_map, inplace=True)
analysis_df.to_csv(analysis_dir + 'data/geo_lookup.csv')

se_lookup.to_csv(analysis_dir + 'data/risk_factor_lookup.csv')

def geo_risk_lookup(county, state, geo_lookup, risk_factor_lookup, print_high_risk=True):
  """
  Function to lookup high risk county level demographics

  county: str
    county name, must be contained in the geo_lookup_table
  state: str
    state name, must be contained in the geo_lookup_table
  geo_lookup_table: pandas.DataFrame
    dataframe matching the geo_lookup_table.csv file
  risk_factor_lookup: pandas.DataFrame
    dataframe matching the risk_factor_lookup.csv file


  """

  # identify demogrpahics quantiles for county, state

  geo_res = geo_lookup.loc[(geo_lookup.COUNTY==county) & (geo_lookup.STATE==state), risk_factor_lookup.factor.unique()]
  if geo_res.shape[0]==0:
    raise ValueError('{}, {} - Not In geo_lookup table'.format(state, county))
  geo_res.rename(columns=col_map, inplace=True)
  geo_res = pd.melt(geo_res, value_vars=geo_res.columns, var_name='factor', value_name='index')

  # identify which quantiles are high risk
  risk_levels = pd.merge(geo_res, risk_factor_lookup, how='inner', on=['factor', 'index'])

  if print_high_risk:
    high_risk = risk_levels[risk_levels.risk_level=='high']

    # Output risk factors
    print('Your school has {} high risk factors:'.format(high_risk.shape[0]))
    for idx, r in high_risk.iterrows():
      l, h = [float(x) for x in r['index'].replace('(', '').replace(']','').split(',')]
      print("""- Your school's county is in a high risk category for {} {:.0%}-{:.0%} percentile -
      which account for {:.0%} of violence incident""".format(r['factor'], l, h, r['perc']))

  risk_levels = risk_levels[['factor', 'index',  'perc', 'risk_level', ]]
  risk_levels.columns = ['factor', 'percentile',  'violance occurance rate', 'risk_level']
  return risk_levels

"""# Demo"""
print("Lets see....")
geo_lookup = pd.read_csv(analysis_dir + 'data/geo_lookup.csv')
risk_factor_lookup = pd.read_csv(analysis_dir + 'data/risk_factor_lookup.csv')

analysis_df.tail(30)

print("....Where are we")
risk_levels = geo_risk_lookup(county='Big Horn County',
                state='Wyoming',
                geo_lookup=geo_lookup,
                risk_factor_lookup=risk_factor_lookup)

print(risk_levels)

