import pandas as pd
import numpy
from scipy.stats.mstats import gmean
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn

import requests

state_list = [
  "Alabama",
  "Alaska",
  "Arizona",
  "Arkansas",
  "California",
  "Colorado",
  "Connecticut",
  "Delaware",
  "District of Columbia",
  "Florida",
  "Georgia",
  "Hawaii",
  "Idaho",
  "Illinois",
  "Indiana",
  "Iowa",
  "Kansas",
  "Kentucky",
  "Louisiana",
  "Maine",
  "Maryland",
  "Massachusetts",
  "Michigan",
  "Minnesota",
  "Mississippi",
  "Missouri",
  "Montana",
  "Nebraska",
  "Nevada",
  "New Hampshire",
  "New Jersey",
  "New Mexico",
  "New York",
  "North Carolina",
  "North Dakota",
  "Ohio",
  "Oklahoma",
  "Oregon",
  "Pennsylvania",
  "Rhode Island",
  "South Carolina",
  "South Dakota",
  "Tennessee",
  "Texas",
  "Utah",
  "Vermont",
  "Virginia",
  "Washington",
  "West Virginia",
  "Wisconsin",
  "Wyoming",
]

# for year in range(2020, 2000, -1):
#   year = str(year)
#   filename = f"data/usa_edu_data/tabn104.80_{year}.xls"
#   with requests.get(f"https://nces.ed.gov/programs/digest/d{year[-2:]}/tables/xls/tabn104.88.xls", stream=True) as r:
#     if r.status_code == 200:
#       with open(filename, "wb") as f:
#         f.write(r.content)
#
# for year in range(2012, 2011, -1):
#   year = str(year)
#   filename = f"data/usa_edu_data/tabn015_{year}.xls"
#   with requests.get(f"https://nces.ed.gov/programs/digest/d{year[-2:]}/tables/xls/tabn015.xls", stream=True) as r:
#     if r.status_code == 200:
#       with open(filename, "wb") as f:
#         f.write(r.content)
#
# for year in range(2011, 2000, -1):
#   year = str(year)
#   filename = f"data/usa_edu_data/tabn012_{year}.xls"
#   with requests.get(f"https://nces.ed.gov/programs/digest/d{year[-2:]}/tables/xls/tabn012.xls", stream=True) as r:
#     if r.status_code == 200:
#       with open(filename, "wb") as f:
#         f.write(r.content)

data = None

for year in range(2020, 2012, -1):
  data_current_year = pd.read_excel(f"data/usa_edu_data/tabn104.80_{year}.xls", skiprows=[0, 1, 2, 3, 4, 5, 6], header=None)
  if year > 2016:
    data_current_year = data_current_year.iloc[:, [0, 10, 19]]
  else:
    data_current_year = data_current_year.iloc[:, [0, 1, 13]]
  data_current_year.columns = ["GeoName", "high_school_percentage", "degree_percentage"]
  data_current_year["GeoName"] = data_current_year["GeoName"].str.replace(".", "").str.strip()
  data_current_year["year"] = year
  data_current_year = data_current_year.dropna()
  if data is not None:
    data = pd.concat([data, data_current_year])
  else:
    data = data_current_year
data = data.reset_index()
data.tail()

data_current_year = pd.read_excel(f"data/usa_edu_data/tabn015_2012.xls", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], header=None)
data_current_year = data_current_year.iloc[:, [0, 1, 17]]
data_current_year.head()
data_current_year.columns = ["GeoName", "high_school_percentage", "degree_percentage"]
data_current_year["GeoName"] = data_current_year["GeoName"].str.replace(".", "").str.strip()
data_current_year["year"] = 2012
data_current_year = data_current_year.dropna()
data_current_year.head()
data = pd.concat([data, data_current_year])
data = data.reset_index()
data.tail()

for year in range(2011, 2007, -1):
  data_current_year = pd.read_excel(f"data/usa_edu_data/tabn012_{year}.xls", skiprows=[0, 1, 2, 3, 4, 5, 6, 7], header=None)
  data_current_year = data_current_year.iloc[:, [0, 1, 17]]
  data_current_year.columns = ["GeoName", "high_school_percentage", "degree_percentage"]
  data_current_year["GeoName"] = data_current_year["GeoName"].str.replace(".", "").str.strip()
  data_current_year["year"] = year
  data_current_year = data_current_year.dropna()
  data = pd.concat([data, data_current_year])
data_current_year.head()

data_edu_raw = data

data_edu = data_edu_raw[["GeoName", "high_school_percentage", "degree_percentage", "year"]]
data_edu = data_edu.rename(columns={"GeoName": "state"})
data_edu = data_edu.sort_values(by=["state", "year"])
data_edu["degree_percentage"] = data_edu["degree_percentage"]/100 + 1
data_edu["degree_percentage_t-1"] = data_edu.groupby("state")["degree_percentage"].shift(1)
data_edu["degree_percentage_growth"] = data_edu["degree_percentage"] / data_edu["degree_percentage_t-1"]

data_edu["high_school_percentage"] = data_edu["high_school_percentage"]/100 + 1
data_edu["high_school_percentage_t-1"] = data_edu.groupby("state")["high_school_percentage"].shift(1)
data_edu["high_school_percentage_growth"] = data_edu["high_school_percentage"] / data_edu["high_school_percentage_t-1"]

data_edu_Y0 = data_edu[data_edu["year"] == 2008][["state", "degree_percentage", "high_school_percentage"]]
data_edu = data_edu.merge(data_edu_Y0, on=["state"])

data_edu = data_edu.dropna()

data_edu_agg = data_edu.groupby(by="state").agg({"high_school_percentage_growth": [gmean], "degree_percentage_growth": [gmean]}) - 1
data_edu_agg.columns = ["high_school_percentage_growth", "degree_percentage_growth"]

data_edu_agg.head()


data_1 = pd.read_csv("CAGDP1__ALL_AREAS_2001_2020.csv", encoding="ISO-8859-1")
data_1 = data_1[data_1["Description"] == "Real GDP (thousands of chained 2012 dollars)"]
data_1 = data_1[data_1["GeoName"].isin(state_list)]
data_1 = data_1.melt(id_vars=["GeoName"], value_vars=[str(i) for i in range(2001, 2020)], var_name="year",
                     value_name="gdp")
data_1 = data_1.dropna()
data_1 = data_1[data_1["gdp"] != "(NA)"]
data_1["gdp"] = data_1["gdp"].astype("int64")
data_1["year"] = data_1["year"].astype("int")
data_1.head()

data_2 = pd.read_excel("download.xls", skiprows=range(0, 5), nrows=59)
data_2["GeoName"] = data_2["GeoName"].replace("Alaska *", "Alaska")
data_2 = data_2.melt(id_vars=["GeoName"], value_vars=[str(i) for i in range(2008, 2020)], var_name="year",
                     value_name="population")
data_2["year"] = data_2["year"].astype("int")
data_2.head()

data_3 = pd.read_csv("SAIRPDImplicitRegionalPriceDeflatorsbystate.csv")
data_3 = data_3.melt(id_vars=["GeoName"], value_vars=[str(i) for i in range(2008, 2020)], var_name="year",
                     value_name="regional_deflator")
data_3["year"] = data_3["year"].astype("int")
data_3.head()

data = pd.merge(data_1, data_2, on=["GeoName", "year"])
data = pd.merge(data, data_3, on=["GeoName", "year"])
data = data.rename({"GeoName": "state"}, axis=1)
data["gdp_per_capita"] = data["gdp"] / data["population"]
data["gdp_per_capita"] = data["gdp_per_capita"] / (data["regional_deflator"] / 100)
# data["gdp_per_capita"] = numpy.log(data["gdp_per_capita"])
data_Y0 = data[data["year"] == 2008][["state", "gdp_per_capita"]]
data_Y0 = data_Y0.rename(columns={"gdp_per_capita": "Y0"})
data = data.sort_values(["state", "year"])
data["gdp_per_capita_t-1"] = data.groupby("state")["gdp_per_capita"].shift(1)
data["gdp_per_capita_growth"] = data["gdp_per_capita"] / data["gdp_per_capita_t-1"]
data = data.dropna()
data.head()

data = data.merge(data_Y0, on=["state"])

data_agg = data.groupby(by="state").agg({"gdp_per_capita_growth": [gmean]}) - 1
data_agg.columns = data_agg.columns.droplevel()
data_agg.head()

data_agg = data_agg.merge(data_Y0, on=["state"])
data_Y0["Y0"] = numpy.log(data_Y0["Y0"])

data_final = data_agg.merge(data_edu_agg, on=["state"])

data_final["state"] = data_final["state"].str.strip()
data_final = data_final[~data_final["state"].isin(["District of Columbia", "Wyoming", "Alaska", "New York", "North Dakota"])]
data_final = data_final.reset_index()

data_final.head(20)

X = sm.add_constant(data_final)
mod = smf.ols(formula="gmean ~ Y0 + high_school_percentage_growth + degree_percentage_growth", data=X)
res = mod.fit()
print(res.summary())

