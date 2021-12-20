# Databricks notebook source


# COMMAND ----------

# MAGIC %md
# MAGIC # COVID Assignment 1
# MAGIC ## Data Analysis with `pandas`
# MAGIC 
# MAGIC ## ![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) In this lesson you:<br>
# MAGIC  - Import the COVID-19 dataset
# MAGIC    * `pd.read_csv()`
# MAGIC  - Summarize the data
# MAGIC    * `head`, `tail`, `shape`
# MAGIC    * `sum`, `min`, `count`, `mean`, `std`
# MAGIC    * `describe`
# MAGIC  - Slice and munge data
# MAGIC    * Slicing, `loc`, `iloc`
# MAGIC    * `value_counts`
# MAGIC    * `drop`
# MAGIC    * `sort_values`
# MAGIC    * Filtering
# MAGIC  - Group data and perform aggregate functions
# MAGIC    * `groupby`
# MAGIC  - Work with missing data and duplicates
# MAGIC    * `isnull`
# MAGIC    * `unique`, `drop_duplicates`
# MAGIC    * `fillna`
# MAGIC  - Visualization
# MAGIC    * Histograms
# MAGIC    * Scatterplots
# MAGIC    * Lineplots
# MAGIC  
# MAGIC  Check out [this cheetsheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) for help.  Also see [the `pandas` docs.](https://pandas.pydata.org/docs/)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Import the COVID-19 dataset

# COMMAND ----------

# MAGIC %md
# MAGIC Use `%sh ls` to search the folder structure

# COMMAND ----------

# MAGIC %sh ls /dbfs/databricks-datasets/COVID/

# COMMAND ----------

# MAGIC %sh ls /dbfs/databricks-datasets/COVID/CSSEGISandData/csse_covid_19_data/csse_covid_19_daily_reports

# COMMAND ----------

# MAGIC %md
# MAGIC Use `%sh head` to see the first few lines of CSV file

# COMMAND ----------

# MAGIC %sh head /dbfs/databricks-datasets/COVID/CSSEGISandData/csse_covid_19_data/csse_covid_19_daily_reports/04-11-2020.csv

# COMMAND ----------

# MAGIC %md
# MAGIC Import `pandas`.  Alias it as `pd`

# COMMAND ----------

import pandas as pd

# COMMAND ----------

# MAGIC %md
# MAGIC Read the csv file.  This creates a `DataFrame`

# COMMAND ----------

pd.read_csv("/dbfs/databricks-datasets/COVID/CSSEGISandData/csse_covid_19_data/csse_covid_19_daily_reports/04-11-2020.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC Now let's combine the lines of code and save the `DataFrame` to a variable so we can reuse it

# COMMAND ----------

import pandas as pd

df = pd.read_csv("/dbfs/databricks-datasets/COVID/CSSEGISandData/csse_covid_19_data/csse_covid_19_daily_reports/04-11-2020.csv")

df

# COMMAND ----------

# MAGIC %md
# MAGIC ### Summarize the data

# COMMAND ----------

# MAGIC %md
# MAGIC Take a peak at the first 10 and last 10 rows of the data

# COMMAND ----------

df.head(10)

# COMMAND ----------

df.tail(10)

# COMMAND ----------

# MAGIC %md
# MAGIC How many records are in the dataset?

# COMMAND ----------

len(df)#2966

# COMMAND ----------

# MAGIC %md
# MAGIC Summarize the data using using six different summary statistics

# COMMAND ----------

df.describe()

# COMMAND ----------

# MAGIC %md
# MAGIC Create a summary of the stats that are aggregated for you...

# COMMAND ----------

aggregate = pd.DataFrame([{'sum': df.Active.sum(),'min' : df.Active.min(), 'max': df.Active.max(), 'count' : df.Active.count(), 'mean': df.Active.mean(), 'std': df.Active.std()}])
print(aggregate)
data = df.describe()
print(data)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Slice and munge data

# COMMAND ----------

# MAGIC %md
# MAGIC Grab the death cases

# COMMAND ----------

deathcase = df.Deaths
print(deathcase.head)

# COMMAND ----------

# MAGIC %md
# MAGIC Grab the country and recovered cases.

# COMMAND ----------

countryrecovered = df[['Country_Region','Recovered']]
print(countryrecovered.head)

# COMMAND ----------

# MAGIC %md
# MAGIC Create a new column `Date`

# COMMAND ----------

df['date'] = pd.to_datetime(df['Last_Update'], format='%Y-%m-%d %H:%M:%S')
print(df.head)

# COMMAND ----------

# MAGIC %md
# MAGIC Slice the DataFrame to get the last 10 rows

# COMMAND ----------

df.iloc[2957:2967]

# COMMAND ----------

# MAGIC %md
# MAGIC Return just the last column from the last row

# COMMAND ----------

df.iloc[2966:2967,12:13]

# COMMAND ----------

# MAGIC %md
# MAGIC How many province/state do we have per country?

# COMMAND ----------

df.groupby(['Country_Region']).Province_State.nunique()

# COMMAND ----------

# MAGIC %md
# MAGIC What's Combined Key?

# COMMAND ----------

# Combination of Admin2,Province_State,Country_Region

# COMMAND ----------

# MAGIC %md
# MAGIC Sort by active cases

# COMMAND ----------

df.sort_values(by=['Active'], ascending=False)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's just look at what's going on in a non-US compared to a US company

# COMMAND ----------

nonUS = df.Country_Region != "US"
US = df.Country_Region == "US"
dfnonUS = df[nonUS]
dfUS = df[US]
# confirmed, death, recovered, active
dfnonUSsum = pd.DataFrame([{'Confirmed': dfnonUS.Confirmed.sum(),'Death': dfnonUS.Deaths.sum(), 'Recovered': dfnonUS.Recovered.sum(), 'Active':dfnonUS.Active.sum()}])
dfUSsum = pd.DataFrame([{'Confirmed': dfUS.Confirmed.sum(),'Death': dfUS.Deaths.sum(), 'Recovered': dfUS.Recovered.sum(), 'Active':dfUS.Active.sum()}])

dfCombined = [dfnonUSsum,dfUSsum]
dfCombined = pd.concat(dfCombined)
dfCombined.index =['Non-US','US']
print(dfCombined)

# COMMAND ----------

# MAGIC %md
# MAGIC Now let's look at what's going on in your county (if your county does not exist use San Francisco)

# COMMAND ----------

SF = df.Admin2 == "San Francisco"
dfSF = df[SF]
# confirmed, death, recovered, active
dfSFsum = pd.DataFrame([{'Confirmed': dfSF.Confirmed.sum(),'Deaths': dfSF.Deaths.sum(), 'Recovered': dfSF.Recovered.sum(), 'Active':dfSF.Active.sum()}])
print(dfSFsum)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Group data and perform aggregate functions

# COMMAND ----------

# MAGIC %md
# MAGIC What country has the greatest number of deaths cases?

# COMMAND ----------

dfDeath = df.groupby(['Country_Region'], as_index=False).Deaths.sum()
max = dfDeath.Deaths.idxmax()
print(dfDeath.loc[[max]])

# COMMAND ----------

# MAGIC %md
# MAGIC Group and sum the data above. **Note that an aggregate function return a scalar (single) value.**

# COMMAND ----------

dfCountry = df.groupby(['Country_Region'], as_index=False).agg({'Confirmed':['sum'],'Deaths': ['sum'], 'Recovered': ['sum'], 'Active': ['sum']})
dfState = df.groupby(['Province_State','Country_Region'], as_index=False).agg({'Confirmed':['sum'],'Deaths': ['sum'], 'Recovered': ['sum'], 'Active': ['sum']})
dfCounty = df.groupby(['Admin2','Province_State','Country_Region'], as_index=False).agg({'Confirmed':['sum'],'Deaths': ['sum'], 'Recovered': ['sum'], 'Active': ['sum']})

# COMMAND ----------

# MAGIC %md
# MAGIC Which non-US states have the most cases?

# COMMAND ----------

nonUS = dfState.Country_Region != "US"
dfNonUS= dfState[nonUS]

dfNonUS.columns =['Province','Country','Confirmed','Deaths','Recovered','Active']

dfNonUS = dfNonUS.sort_values(by = ['Active'], ascending = False)
dfNonUS

# New South Wales, Hong Kong, and Queensland

# COMMAND ----------

# MAGIC %md
# MAGIC ### Work with missing data and duplicates

# COMMAND ----------

# MAGIC %md
# MAGIC Do we have null values in the dataframe if so how many?

# COMMAND ----------

df.isna()
  
#yes 

# COMMAND ----------

df.isna().sum()
# 281 in FIPS, 181 in Province_State, 58 in Lat and Long

# COMMAND ----------

# MAGIC %md
# MAGIC How many unique states?

# COMMAND ----------

df.Province_State.nunique()
#139

# COMMAND ----------

# MAGIC %md
# MAGIC Create another way to do the same thing.

# COMMAND ----------

len(df.Province_State.dropna().unique())
#139

# COMMAND ----------

state = list(df.Province_State.value_counts())

len(state)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualization
# MAGIC    * Histograms
# MAGIC    * Scatterplots
# MAGIC    * Lineplots

# COMMAND ----------

# MAGIC %md
# MAGIC What is the _distribution_ of confirmed by US country region?

# COMMAND ----------

US = dfState.Country_Region == "US"
dfUS= dfState[US]

dfUS.columns =['State','Country','Confirmed','Deaths','Recovered','Active']

# COMMAND ----------

# MAGIC %matplotlib inline
# MAGIC import matplotlib.pyplot as plt
# MAGIC dfUS = dfUS[["State","Confirmed"]]
# MAGIC display(dfUS.plot.hist(by = "State", bins = 10))

# COMMAND ----------

# MAGIC %md
# MAGIC How do recovered cases compare to active?

# COMMAND ----------

dfState.columns =['State','Country','Confirmed','Deaths','Recovered','Active']
col_to_drop = ['Country','Confirmed','Deaths']
RvA = dfState.drop(col_to_drop,axis=1)
RvA

# COMMAND ----------

# MAGIC %matplotlib inline
# MAGIC import matplotlib.pyplot as plt
# MAGIC f = plt.scatter(RvA['Active'], RvA['Recovered'], color='red')
# MAGIC display(f)

# COMMAND ----------

# MAGIC %md
# MAGIC Import the data for all available days.

# COMMAND ----------

import glob
import datetime

path = "/dbfs/databricks-datasets/COVID/CSSEGISandData/csse_covid_19_data/csse_covid_19_daily_reports"
all_files = glob.glob(path + "/*.csv")

dfs = []

for filename in all_files:
  temp_df = pd.read_csv(filename)
  temp_df.columns = [c.replace("/", "_") for c in temp_df.columns]
  temp_df.columns = [c.replace(" ", "_") for c in temp_df.columns]
  
  month, day, year = filename.split("/")[-1].replace(".csv", "").split("-")
  d = datetime.date(int(year), int(month), int(day))
  temp_df["Date"] = d

  dfs.append(temp_df)
  
all_days_df = pd.concat(dfs, axis=0, ignore_index=True, sort=False)
all_days_df = all_days_df.drop(["Latitude", "Longitude", "Lat", "Long_", "FIPS", "Combined_Key", "Last_Update"], axis=1)

# COMMAND ----------

all_days_df.head(10)

# COMMAND ----------

# MAGIC %md
# MAGIC How has the disease spread over time by state?

# COMMAND ----------

# MAGIC %matplotlib inline
# MAGIC import matplotlib.pyplot as plt
# MAGIC state_days_df.groupby(["Date"])["Confirmed"].sum().plot()

# COMMAND ----------

# MAGIC %md
# MAGIC Break this down by types of cases by region.

# COMMAND ----------

all_days_df.groupby("Date")["Confirmed", "Deaths", "Recovered"].sum().plot()

# COMMAND ----------

# MAGIC %md
# MAGIC What is the growth in your county?

# COMMAND ----------

(all_days_df[(all_days_df["Country_Region"] == "US") & (all_days_df["Province_State"] == "California") & (all_days_df["Admin2"] == "San Francisco")]
  .groupby("Date")["Confirmed", "Deaths", "Recovered"].sum().plot(title = "San Francisco"))

# COMMAND ----------

# MAGIC %md
# MAGIC Wrap this up in a function and run it yourself!

# COMMAND ----------

def county_charts (Country,Province,County):
  (all_days_df[(all_days_df["Country_Region"] == Country) & (all_days_df["Province_State"] == Province) & (all_days_df["Admin2"] == County)]
  .groupby("Date")["Confirmed", "Deaths", "Recovered"].sum().plot(title = County))
  


# COMMAND ----------

county_charts("US","Florida","Miami-Dade")
