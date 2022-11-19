import pandas
import numpy



def get_real_income():
    data = pandas.read_csv("data/RealIncomePerCapita.csv", skiprows=3)
    data = data[data["GeoName"] != "United States"]
    data = data.dropna()
    data["ln Yt/Y0"] = numpy.log(data["2019"] / data["2008"])
    data["ln Y0"] = numpy.log(data["2008"])
    print(stats.shapiro(data["ln Yt/Y0"]))
    print(stats.shapiro(data["ln Y0"]))

    abbr = pandas.read_csv("data/StateAbbr.csv")
    data = data.merge(abbr, left_on="GeoName", right_on="state")
    return data
