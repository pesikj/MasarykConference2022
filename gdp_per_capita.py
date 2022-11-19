import numpy
import pandas
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from matplotlib import pyplot as plt

from data_loader import real_gdp_per_capita

data = real_gdp_per_capita.get_real_gdp_per_capita()

data_regression_0 = data[data["Year"] == 1998]
data_regression_t = data[data["Year"] == 2020]
data = pandas.merge(data_regression_0, data_regression_t, on="GeoName", suffixes=("_0", "_t"))

# Outliers
data = data[~data["GeoName"].isin(["District of Columbia", "North Dakota"])]

data["ln Yt/Y0"] = numpy.log(data["RealGDPPerCapita_t"] / data["RealGDPPerCapita_0"])
data["ln Y0"] = numpy.log(data["RealGDPPerCapita_0"])
print(stats.shapiro(data["ln Yt/Y0"]))
print(stats.shapiro(data["ln Y0"]))

abbr = pandas.read_csv("data/StateAbbr.csv")
data = data.merge(abbr, left_on="GeoName", right_on="state")

X = data["ln Y0"]
y = data["ln Yt/Y0"]
X = sm.add_constant(X)
mod = sm.OLS(y, X)
res = mod.fit()
print(res.summary())

sns.lmplot(
    data=data[["ln Yt/Y0", "ln Y0"]], x="ln Y0", y="ln Yt/Y0", scatter_kws={"s": 10}
)

for line in range(0, data.shape[0]):
    plt.annotate(data["code"].iloc[line], (data["ln Y0"].iloc[line], data["ln Yt/Y0"].iloc[line]), fontsize=8)

plt.show()
