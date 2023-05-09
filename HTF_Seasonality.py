import pandas as pd
from datetime import datetime
import datetime as dt
import time
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter("ignore")


guWk = pd.read_csv("../GUWeekly.csv")

ten_year = "2013-01-01"
five_year = "2018-01-01"
two_year = "2020-01-01"


def structureMT4Data(df):  # df cleaning and formatting
    df.columns = ["date", "time", "open", "high", "low", "close", "volume"]

    df["date"] = pd.to_datetime(df["date"])
    df["date"] = pd.to_datetime(df["date"], format="%Y%m/%d")
    df["time"] = pd.to_datetime(df["time"], format="%H:%M").dt.time
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    # df.set_index("date", inplace=True)

    df = df[df["high"] != df["low"]]

    df.dropna(inplace=True)
    return df


df = structureMT4Data(guWk)


def sortMonth(df):
    jan = df[df["month"] == 1]
    feb = df[df["month"] == 2]
    mar = df[df["month"] == 3]
    apr = df[df["month"] == 4]
    may = df[df["month"] == 5]
    jun = df[df["month"] == 6]
    jul = df[df["month"] == 7]
    aug = df[df["month"] == 8]
    sep = df[df["month"] == 9]
    oct = df[df["month"] == 10]
    nov = df[df["month"] == 11]
    dec = df[df["month"] == 12]
    return jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec


def averageClose(df, date=ten_year):
    date_range = df["date"] >= date
    df = df[date_range]
    jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec = sortMonth(df)

    year = pd.Series(
        [
            jan.close.mean(),
            feb.close.mean(),
            mar.close.mean(),
            apr.close.mean(),
            may.close.mean(),
            jun.close.mean(),
            jul.close.mean(),
            aug.close.mean(),
            sep.close.mean(),
            oct.close.mean(),
            nov.close.mean(),
            dec.close.mean(),
        ]
    )
    year_col = pd.Series(
        [
            "Janurary",
            "Feburary",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
    )
    year = pd.concat([year_col, year], axis=1)
    year.columns = ["Months", "Avg_price"]
    year.set_index("Months", inplace=True)
    return year


year_10 = averageClose(df, ten_year)
year_5 = averageClose(df, five_year)
year_2 = averageClose(df, two_year)

# q1_open = sortMonth(df)[0]
# q1_open.reset_index(inplace=True)
# q1_open = q1_open[q1_open.month == 1.0]


# q1_close = sortMonth(df)[2]
# q1_close.reset_index(inplace=True)
# q1_close = q1_close[q1_close.month == 3.0]
# q1 = pd.concat([q1_open.open, q1_close.close, q1_open.year, q1_close.year], axis=1)
# print(q1)

# fig, ax = plt.subplots(figsize=(15, 8))
# year_10.plot(
#     kind="line",
#     ax=ax,
# )
# year_5.plot(
#     kind="line",
#     ax=ax,
# )
# year_2.plot(kind="line", ax=ax, title="10, 5, 2 Years", grid=True)
# ax.set_xlabel("Month")
# ax.set_ylabel("Avg. price")
# plt.show()
