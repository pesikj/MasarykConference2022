import pandas


def get_real_gdp_per_capita():
    data = pandas.read_csv("data/RealGDP.csv", skiprows=3)
    data = data[data["GeoName"] != "United States"]
    data = data.melt(id_vars=["GeoName"], value_vars=[str(i) for i in range(1998, 2021)], var_name="Year",
                         value_name="RealGDP")
    # print(data.head())

    data_2 = pandas.read_excel("data/population.xlsx", skiprows=range(0, 5), nrows=59)
    data_2["GeoName"] = data_2["GeoName"].replace("Alaska *", "Alaska").replace("Hawaii *", "Hawaii")
    data_2 = data_2.melt(id_vars=["GeoName"], value_vars=[str(i) for i in range(1998, 2021)], var_name="Year",
                         value_name="Population")

    data = pandas.merge(data, data_2, on=["GeoName", "Year"])
    data["Year"] = data["Year"].astype("int")
    data["RealGDPPerCapita"] = data["RealGDP"] / data["Population"]
    return data
