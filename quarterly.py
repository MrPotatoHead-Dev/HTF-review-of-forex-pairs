import pandas as pd
from datetime import datetime
import datetime as dt
import time
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter("ignore")

# guMnth = pd.read_csv("../XAUUSD_RAW43200.csv")
guMnth = pd.read_csv("../GBPUSD43200.csv")
# guMnth = pd.read_csv("../CL_raw43200.csv")
ten_year = "2015-01-01"

five_year = "2017-01-01"  # use this one
two_year = "2020-01-01"
year = int(2022)


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


df = structureMT4Data(guMnth)


# seperate data into months
def sortMonth(df, date=ten_year):
    date_range = df["date"] >= date
    df = df[date_range]
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


# determine the quarters return
def quarterlyReturn(df, Q, date=ten_year):
    # If statements corresponding to the quarter chosen
    if Q == 1:
        print("Analyzing Q1")
        index1 = 0
        index2 = 1.0
        index3 = 2
        index4 = 3.0
    elif Q == 2:
        print("Analyzing Q2")
        index1 = 3
        index2 = 4.0
        index3 = 5
        index4 = 6.0
    elif Q == 3:
        print("Analyzing Q3")
        index1 = 6
        index2 = 7.0
        index3 = 8
        index4 = 9.0
    elif Q == 4:
        print("Analyzing Q4")
        index1 = 9
        index2 = 10.0
        index3 = 11
        index4 = 12.0
    # return the months dataframe
    q_open = sortMonth(df, date)[index1]
    q_open.reset_index(inplace=True)
    q_open = q_open[q_open.month == index2]
    q_close = sortMonth(df, date)[index3]
    q_close.reset_index(inplace=True)
    q_close = q_close[q_close.month == index4]
    # combine the dataframes open and close values to determine the return
    q = pd.concat([q_open.open, q_close.close, q_open.year, q_close.year], axis=1)
    q.columns = ["open", "close", "year_open", "year_close"]

    bullish = []
    bearish = []
    roi_sum = []
    for i in range(len(q)):
        if q["year_open"].iloc[i] == q["year_close"].iloc[i]:
            # roi = int((q.close.iloc[i] - q.open.iloc[i]) * 1000)
            roi = 1 if q.close.iloc[i] > q.open.iloc[i] else -1
            if roi > 0:
                bullish.append(1)
            elif roi < 0:
                bearish.append(1)
            roi_sum.append(roi)

    if len(bullish) > len(bearish):
        print(f"Q{Q} is frequently more bullish")
        status = 2
    elif len(bullish) < len(bearish):
        print(f"Q{Q} is frequently more bearish")
        status = 1
    elif len(bullish) == len(bearish):
        print("Inconclusive")
        status = 0
    roi = sum(roi_sum)
    return roi, status


# average with respect to the close
def averageClose(df):
    avg_year = []
    for i in range(12):
        month = sortMonth(df)[i]
        avg_year.append(month.close.mean())
    return avg_year


# average with respect to the high and low of the candle
def avergeHL(df):
    avg_year = []
    for i in range(12):
        month = sortMonth(df)[i]

        h_l = (month.high + month.low) / 2
        avg_year.append(h_l.mean())
    return avg_year


def averageBody(df):
    avg_year = []
    for i in range(12):
        month = sortMonth(df)[i]

        h_l = (month.open + month.close) / 2
        avg_year.append(abs(h_l.mean()))
    return avg_year


# seperate 1 years of Price Action
year_simp = df[df["year"] == 2022]
print(year_simp)

avg_hl = avergeHL(df)
avg_year = averageClose(df)
avg_body = averageBody(df)
print(len(avg_hl))
xvals = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]

x = range(len(avg_hl))

fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(x, avg_hl, label="avg H-L")
ax.plot(x, avg_year, label="avg Close")
ax.plot(x, avg_body, label="avg_Body")
ax2 = ax.twinx()
ax2.plot(x, year_simp.close, "r", linewidth=2, label="2022 PA")
plt.xticks(range(len(xvals)), xvals)
plt.title("Average price over 15years overlayed 2022 PA (GBPUSD)")
plt.grid(axis="x")
ax.legend()
ax2.legend(loc="lower right")
plt.show()

q1 = quarterlyReturn(df, 1, five_year)[0]
q2 = quarterlyReturn(df, 2, five_year)[0]
q3 = quarterlyReturn(df, 3, five_year)[0]
q4 = quarterlyReturn(df, 4, five_year)[0]


quarter_return = pd.Series([q1, q2, q3, q4])
# fig, ax = plt.subplots(figsize=(15, 8))
# quarter_return.plot(kind="bar", ax=ax)
# ax.set_xticklabels(["Q1", "Q2", "Q3", "Q4"], rotation=0)
# for i, v in enumerate(quarter_return):
#     ax.annotate(str(v), xy=(i, v), ha="center", va="bottom")
# plt.show()
