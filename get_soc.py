import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from datetime import date, timedelta, datetime
from pathlib import Path
from settings import datapath, basepath, threshold_on, threshold_off
import seaborn as sns


def load_latest_file():
    datadir = Path(datapath)
    today = date.today()
    year = today.strftime("%Y")
    datestr = today.strftime("%Y%m%d")
    filename = "BatteryInverter-Battery-{}.csv".format(datestr)
    file = datadir / year / filename

    return pd.read_csv(file, skiprows=4)


def get_weekly_data():
    df = pd.DataFrame()
    try:
        datadir = Path(datapath)
        for i in range(7):
            day = date.today() - timedelta(6 - i)
            year = day.strftime("%Y")
            datestr = day.strftime("%Y%m%d")
            filename = "BatteryInverter-Battery-{}.csv".format(datestr)
            file = datadir / year / filename
            data = pd.read_csv(file, skiprows=4)
            df = df.append(data[["dd/MM/yyyy HH:mm:ss", "SOC"]], ignore_index=True)
        df["dd/MM/yyyy HH:mm:ss"] =pd.to_datetime(df["dd/MM/yyyy HH:mm:ss"], 
                                                  format="%d/%m/%Y %H:%M:%S")
    except:
        pass
    return df



def get_current_soc():
    current_data = load_latest_file()
    date_time, soc = current_data[["dd/MM/yyyy HH:mm:ss", "SOC"]].iloc[-1]
    return date_time, soc


def update_plot():
    data = load_latest_file()
    data = data[["dd/MM/yyyy HH:mm:ss", "SOC"]]
    data.columns = ["datetime", "SOC"]
    data["datetime"] = pd.to_datetime(data["datetime"], 
                                      format="%d/%m/%Y %H:%M:%S")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.datetime, data.SOC, lw=2.5)
    xmin = datetime(data.datetime.dt.year[0], 
                    data.datetime.dt.month[0], 
                    data.datetime.dt.day[0], hour=0)
    xmax = xmin + timedelta(days=1)
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((0, 102))
    h_fmt = mdates.DateFormatter("%H:%M")
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
    ax.xaxis.set_minor_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(h_fmt)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.grid(which="both")
    ax.set_ylabel("SOC")
    title = data.datetime.dt.date[0].strftime('%d.%m.%Y')
    ax.set_title(title)
    ax.axhline(threshold_on, ls=":", color="black", label="threshold", lw=2)
    ax.axhline(threshold_off, ls=":", color="black", lw=2)
    ax.legend()
    plot_dir = Path(basepath)
    plt.savefig(plot_dir / 'www/soc_over_time.png', transparent=True)


def update_weekly_plot():
    weekly_data = get_weekly_data()
    if not weekly_data.empty:
        data = weekly_data[["dd/MM/yyyy HH:mm:ss", "SOC"]]
        data.columns = ["datetime", "SOC"]
        fig, ax = plt.subplots(figsize=(8,2))
        #sns.lineplot(data=data, x="datetime", y="SOC", ax=ax)
        ax.plot(data.datetime, data.SOC, lw=2.5)
        
        xmin = datetime(data.datetime.dt.year[0], 
                    data.datetime.dt.month[0], 
                    data.datetime.dt.day[0], hour=0)
        xmax = xmin + timedelta(days=7)
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((0, 105))
        
        ax.set_ylabel("SOC")
        ax.set_title("SOC over last 7 days")
        ax.axhline(threshold_on, ls=":", color="black", label="threshold", lw=2)
        ax.axhline(threshold_off, ls=":", color="black", lw=2)
        d_fmt = mdates.DateFormatter("%d.%m.")
        ax.xaxis.set_major_formatter(d_fmt)
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
        #ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
        ax.grid(which="both")
        plot_dir = Path(basepath)
        ax.figure.savefig(plot_dir / 'www/soc_over_time_week.png', transparent=True)
