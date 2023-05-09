import pandas as pd
from datetime import datetime
import datetime as dt
import time
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter("ignore")
# df = pd.read_csv("GBPUSD30.csv")
gu15min = pd.read_csv("../GBPUSD15_dirty.csv")
eu15min = pd.read_csv("../EURUSD15.csv")
au15min = pd.read_csv("../AUDUSD15.csv")
ucad15min = pd.read_csv("../USDCAD15.csv")
uchf15min = pd.read_csv("../USDCHF15.csv")
uj15min = pd.read_csv("../USDJPY15.csv")
gold15min = pd.read_csv("../XAUUSD15.csv")
silver15min = pd.read_csv("../XAGUSD15.csv")


# session times
asian_session_finish = datetime.strptime("07:00:00", "%H:%M:%f").time()
london_session_start = datetime.strptime("08:00:00", "%H:%M:%f").time()
london_session_finish = datetime.strptime("15:00:00", "%H:%M:%f").time()
ny_session_start = datetime.strptime("15:00:00", "%H:%M:%f").time()
ny_session_finish = datetime.strptime("23:00:00", "%H:%M:%f").time()

date = "2018-01-01"


def structureMT4Data(df, date=date):  # df cleaning and formatting
    df.columns = ["date", "time", "open", "high", "low", "close", "volume"]
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])

    df["date"] = pd.to_datetime(df["date"])
    df["date"] = pd.to_datetime(df["date"], format="%Y%m/%d")
    df["time"] = pd.to_datetime(df["time"], format="%H:%M").dt.time

    df.set_index("datetime", inplace=True)
    date_range = df["date"] >= date
    df = df[date_range]
    df = df[df["high"] != df["low"]]

    df.dropna(inplace=True)
    return df


# df["datetime"] = pd.to_datetime(df["datetime"], unit="ms").astype("datetime64[ns]")


def dailyHiLo(df):
    candle_count = 0
    daily_high_times = []
    daily_low_times = []
    day_counter = 0
    for i in range(1, len(df)):
        if df.date.iloc[i] != df.date.iloc[i - 1]:
            day_counter = day_counter + 1
            if candle_count >= 90:
                daily_high = max(df["high"].iloc[i - candle_count : i], default=0)
                daily_low = min(df["low"].iloc[i - candle_count : i], default=0)
                time_window = df["time"].iloc[i - candle_count : i]

                for index_high, value_high in enumerate(
                    df["high"].iloc[i - candle_count : i]
                ):
                    if value_high == daily_high and index_high != 0:
                        daily_high_times.append(time_window[index_high])
                for index_low, value_low in enumerate(
                    df["low"].iloc[i - candle_count : i]
                ):
                    if value_low == daily_low and index_low != 0:
                        daily_low_times.append(time_window[index_low])

            candle_count = 0
        candle_count = candle_count + 1

    high_counts = pd.Series(daily_high_times).value_counts()
    high_counts = high_counts.sort_index()
    low_counts = pd.Series(daily_low_times).value_counts()
    low_counts = low_counts.sort_index()
    combined_counts = pd.concat([high_counts, low_counts], axis=1)
    combined_counts.columns = ["Daily_high", "Daily_low"]
    return combined_counts


def asianHiLo(df):
    asia_high_times = []
    asia_low_times = []
    num_bars = 20
    # find the session highs and lows
    for i in range(1, len(df) - 1):
        # get the session high and low
        if df.iloc[i]["time"] == asian_session_finish:
            asian_high = max(df["high"].iloc[i - (num_bars + 1) : i], default=0)
            asian_low = min(df["low"].iloc[i - (num_bars + 1) : i], default=0)
            subset = df["time"].iloc[i - (num_bars + 1) : i]
            for index_high, value_high in enumerate(
                df["high"].iloc[i - (num_bars + 1) : i]
            ):
                if value_high == asian_high:
                    if index_high != 0:
                        asia_high_times.append(subset[index_high])
            for index_low, value_low in enumerate(
                df["low"].iloc[i - (num_bars + 1) : i]
            ):
                if value_low == asian_low:
                    if index_low != 0:
                        asia_low_times.append(subset[index_low])

    high_counts = pd.Series(asia_high_times).value_counts()
    high_counts = high_counts.sort_index()
    low_counts = pd.Series(asia_low_times).value_counts()
    low_counts = low_counts.sort_index()
    combined_counts = pd.concat([high_counts, low_counts], axis=1)
    combined_counts.columns = ["Asia_high", "Asia_low"]
    combined_counts = combined_counts.loc[combined_counts["Asia_high"] >= 2]
    combined_counts = combined_counts.loc[combined_counts["Asia_low"] >= 2]
    return combined_counts


def londonHiLo(df):
    london_high_times = []
    london_low_times = []
    num_bars = 32
    # find the session highs and lows
    for i in range(1, len(df) - 1):
        # get the session high and low
        if df.iloc[i]["time"] == london_session_finish:
            if df["time"].iloc[i - num_bars] == asian_session_finish:
                london_high = max(df["high"].iloc[i - (num_bars + 1) : i], default=0)
                london_low = min(df["low"].iloc[i - (num_bars + 1) : i], default=0)
                subset = df["time"].iloc[i - (num_bars + 1) : i]
                for index_high, value_high in enumerate(
                    df["high"].iloc[i - (num_bars + 1) : i]
                ):
                    if value_high == london_high:
                        if index_high != 0:
                            london_high_times.append(subset[index_high])
                for index_low, value_low in enumerate(
                    df["low"].iloc[i - (num_bars + 1) : i]
                ):
                    if value_low == london_low:
                        if index_low != 0:
                            london_low_times.append(subset[index_low])

    high_counts = pd.Series(london_high_times).value_counts()
    high_counts = high_counts.sort_index()
    low_counts = pd.Series(london_low_times).value_counts()
    low_counts = low_counts.sort_index()
    combined_counts = pd.concat([high_counts, low_counts], axis=1)
    combined_counts.columns = ["London_high", "London_low"]
    return combined_counts


def newYorkHiLo(df):
    ny_high_times = []
    ny_low_times = []
    num_bars = 32
    # find the session highs and lows
    for i in range(1, len(df) - 1):
        # get the session high and low
        if df.iloc[i]["time"] == ny_session_finish:
            if df["time"].iloc[i - num_bars] == london_session_finish:
                london_high = max(df["high"].iloc[i - (num_bars + 1) : i], default=0)
                london_low = min(df["low"].iloc[i - (num_bars + 1) : i], default=0)
                subset = df["time"].iloc[i - (num_bars + 1) : i]
                for index_high, value_high in enumerate(
                    df["high"].iloc[i - (num_bars + 1) : i]
                ):
                    if value_high == london_high:
                        if index_high != 0:
                            ny_high_times.append(subset[index_high])
                for index_low, value_low in enumerate(
                    df["low"].iloc[i - (num_bars + 1) : i]
                ):
                    if value_low == london_low:
                        if index_low != 0:
                            ny_low_times.append(subset[index_low])

    high_counts = pd.Series(ny_high_times).value_counts()
    high_counts = high_counts.sort_index()
    low_counts = pd.Series(ny_low_times).value_counts()
    low_counts = low_counts.sort_index()
    combined_counts = pd.concat([high_counts, low_counts], axis=1)
    combined_counts.columns = ["NY_high", "NY_low"]
    return combined_counts


dfs = [gu15min, eu15min, au15min, ucad15min, uchf15min, uj15min, gold15min, silver15min]
# dfs = [gu15min, eu15min]
results = pd.DataFrame()
number = 0
for i, df in enumerate(dfs):
    df_cleaned = structureMT4Data(df, date)

    daily_res = dailyHiLo(df_cleaned)
    asia_res = asianHiLo(df_cleaned)
    london_res = londonHiLo(df_cleaned)
    ny_res = newYorkHiLo(df_cleaned)

    results = pd.concat(
        [results, daily_res, asia_res, london_res, ny_res],
        axis=1,
    )
    labels = ["GU", "EU", "AU", "UCAD", "UCHF", "UJ", "Gold", "Silver"]
    label = labels[i]
    print(label)
    fig, ax = plt.subplots(figsize=(15, 8))
    daily_res.plot(kind="bar", ax=ax, stacked=True)
    plt.savefig(f"Daily_{label}_2018.png")

    fig, ax = plt.subplots(figsize=(15, 8))
    asia_res.plot(kind="bar", ax=ax, stacked=True)
    plt.savefig(f"asia_res_{label}_2018.png")

    fig, ax = plt.subplots(figsize=(15, 8))
    london_res.plot(kind="bar", ax=ax, stacked=True)
    plt.savefig(f"london_res_{label}_2018.png")

    fig, ax = plt.subplots(figsize=(15, 8))
    ny_res.plot(kind="bar", ax=ax, stacked=True)
    plt.savefig(f"ny_res_{labels[i]}_2018.png")


results.to_csv("Daily_SessionHiLo.csv", index=False)
