import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.precision", 2)

# for Jupyter-book, we copy data from GitHub. Locally, to save Internet traffic,
# you can specify the data/ folder from the root of your cloned
# https://github.com/Yorko/mlcourse.ai repo
DATA_URL = "https://raw.githubusercontent.com/Yorko/mlcourse.ai/main/data/"

df = pd.read_csv(DATA_URL + "telecom_churn.csv")
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())

df["Churn"] = df["Churn"].astype("int64")
print(df.describe())
print(df.describe(include=["object", "bool"]))

print(df["Churn"].value_counts())
print(df["Churn"].value_counts(normalize=True))

print(df.sort_values(by="Total day charge", ascending=False).head())
print(df.sort_values(by=["Churn", "Total day charge"], ascending=[True, False]).head())

print(df["Churn"].mean())
print(df.select_dtypes(include=np.number)[df["Churn"] == 1].mean())
print(df[df["Churn"] == 1]["Total day minutes"].mean())
print(df[(df["Churn"] == 0) & (df["International plan"] == "No")]["Total intl minutes"].max())

print(df.loc[0:5, "State":"Area code"])
print(df.iloc[0:5, 0:3])

print(df.apply(np.max))
print(df[df["State"].apply(lambda state: state[0] == "W")].head())

d = {"No": False, "Yes": True}
df["International plan"] = df["International plan"].map(d)
print(df.head())

a_series = pd.Series(['a', 'b', 'c'])
print(a_series.replace({'a':1, 'b':1}))
print(a_series.map({'a':1, 'b':2}))

df = df.replace({"Voice mail plan": d})
print(df.head())

columns_to_show = ["Total day minutes", "Total eve minutes", "Total night minutes"]
print(df.groupby(["Churn"])[columns_to_show].describe(percentiles=[]))
print(df.groupby(["Churn"])[columns_to_show].agg(["mean", "std", "min", "max"]))

print(pd.crosstab(df["Churn"], df["International plan"]))
print(pd.crosstab(df["Churn"], df["Voice mail plan"], normalize=True))

print(df.pivot_table(
    ["Total day calls", "Total eve calls", "Total night calls"],
     ["Area code"],
           aggfunc = "mean",
      ))

total_calls = (
    df["Total day calls"]
    + df["Total eve calls"]
    + df["Total night calls"]
    + df["Total intl calls"]
)
df.insert(loc=len(df.columns), column="Total calls", value=total_calls)
print(df.head())

df["Total charge"] = (
    df["Total day charge"]
    + df["Total eve charge"]
    + df["Total night charge"]
    + df["Total intl charge"]
)
print(df.head())

df.drop(["Total charge", "Total calls"], axis=1, inplace=True)
print(df.drop([1, 2]).head())

print(pd.crosstab(df["Churn"], df["International plan"], margins=True))

sns.set()
#sns.countplot(x="International plan", hue="Churn", data=df)
#plt.show()

print(pd.crosstab(df["Churn"], df["Customer service calls"], margins=True))
#sns.countplot(x="Customer service calls", hue="Churn", data=df)
#plt.show()

df["Many_service_calls"] = (df["Customer service calls"] > 3).astype("int")
print(pd.crosstab(df["Many_service_calls"], df["Churn"], margins=True))
sns.countplot(x="Many_service_calls", hue="Churn", data=df)
plt.show()

print(pd.crosstab(df["Many_service_calls"] & df["International plan"], df["Churn"], margins=True))
