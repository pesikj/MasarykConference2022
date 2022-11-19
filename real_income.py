import seaborn as sns
import statsmodels.api as sm
from matplotlib import pyplot as plt

from data_loader import real_income

data = real_income.get_real_income()

X = data["ln Y0"]
y = data["ln Yt/Y0"]
X = sm.add_constant(X)
mod = sm.OLS(y, X)
res = mod.fit()
print(res.summary())

sns.lmplot(data=data[["ln Yt/Y0", "ln Y0"]], x="ln Y0", y="ln Yt/Y0", scatter_kws={"s": 10})

for line in range(0, data.shape[0]):
    plt.annotate(data["code"].iloc[line], (data["ln Y0"].iloc[line], data["ln Yt/Y0"].iloc[line]), fontsize=8)

plt.show()
