import pandas as pd
import numpy as np
from datetime import date
from pathlib import Path
from settings import datapath, basepath, threshold_on, threshold_off


def load_latest_file():
    datadir = Path(datapath)
    
    today = date.today()
    year = today.strftime("%Y")
    datestr = today.strftime("%Y%m%d")
    filename = "BatteryInverter-Battery-{}.csv".format(datestr)
    file = datadir / year / filename

    return pd.read_csv(file, skiprows=4)


def get_current_soc():
    current_data = load_latest_file()
    date_time, soc = current_data[["dd/MM/yyyy HH:mm:ss", "SOC"]].iloc[-1]
    return date_time, soc


def update_plot():
    current_data = load_latest_file()
    ax = current_data[["dd/MM/yyyy HH:mm:ss", "SOC"]].plot()
    ax.set_xticks([0, 72, 144, 216, 288])
    ax.set_xticklabels(["00:00", "06:00", "12:00", "18:00", "00:00"])
    ax.set_ylabel("SOC")
    title = current_data[["dd/MM/yyyy HH:mm:ss", "SOC"]].iat[0, 0]
    ax.set_title(title[0:10])
    ax.axhline(threshold_on, ls=":", color="black", label="threshold")
    ax.axhline(threshold_off, ls=":", color="black")
    ax.legend()
    plot_dir = Path(basepath)
    ax.figure.savefig(plot_dir / 'www/soc_over_time.png')
