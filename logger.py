from settings import logpath
from pathlib import Path
from datetime import datetime

def log_event(event, reason):
    now = now = datetime.now()
    time_str = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(Path(logpath) / "event.log", "a") as f:
        f.write("{}:  {};    Reason: {}\n".format(time_str, event, reason))


def log_error(error):
    now = now = datetime.now()
    time_str = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(Path(logpath) / "error.log", "a") as f:
        f.write("{}:  {}\n".format(time_str, error))


# only for developement
def log_dev(msg):
    now = now = datetime.now()
    time_str = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(Path(logpath) / "debug.log", "a") as f:
        f.write("{}:  {}\n".format(time_str, msg))
