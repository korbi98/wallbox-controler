#!/usr/bin/env python3

from settings import threshold_on, threshold_off, basepath
from logger import log_event, log_error, log_dev
from get_soc import get_current_soc, update_plot
from pathlib import Path
import subprocess
import sys

ACTIVATION_MSG = "Wallbox was activated"
DEACTIVATION_MSG = "Wallbox was deactivated"
ENABLE_AUTO_MSG = "Auto mode enabled"
MANUAL_REASON = "Manual command"
AUTO_REASON = "Threshold reached"

def activate_wallbox(reason="unspecified"):
    result = exec_switch_command("setswitchon")
    if result[0] == "1":
        log_event(ACTIVATION_MSG, reason)
    else:
        log_error("activation failed")


def deactivate_wallbox(reason="unspecified"):
    result = exec_switch_command("setswitchoff")
    if result[0] == "0":
        log_event(DEACTIVATION_MSG, reason)
    else:
        log_error("deactivation failed")


def get_wallbox_status():
    result = exec_switch_command("getswitchstate")
    if "invalid" in result:
        return 100
    else:
        return int(result[0])


def exec_switch_command(command, verbose=False):
    result = subprocess.run(["/home/pi/wallbox_controller/exec_switch_command.sh",
                             "-c", command, "-v" * verbose],
                            stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def set_operation_mode(mode):
    dir = Path(basepath)
    with open(dir / "settings.py", "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if "operation_mode" in line:
                lines[index] = "operation_mode = {}".format(mode)
        with open(dir / "settings.py", "w") as f:
            f.writelines(lines)


def get_operation_mode():
    dir = Path(basepath)
    with open(dir / "settings.py", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "operation_mode" in line:
                return int(line.replace("operation_mode = ", ""))
    return 0


def update_wallbox(soc):
    update_plot()
    if get_operation_mode():
        if soc > threshold_on and not get_wallbox_status():
            activate_wallbox(AUTO_REASON)
        if soc < threshold_off and get_wallbox_status():
            deactivate_wallbox(AUTO_REASON)
        log_dev("updated wallbox status; soc {}, status {}".format(soc, get_wallbox_status()))
    else:
        log_dev("wallbox not updated because manual mode")


def get_status_str():
    timestamp, soc = get_current_soc()
    operation_mode = "auto" if get_operation_mode() else "manual"
    status = get_wallbox_status()
    if status == 0:
        status_str = "off"
    elif status == 1:
        status_str = "on"
    else:
        status_str = "error"

    status_str = "{}:  SOC: {}; Mode: {}; Status: {}".format(timestamp, soc, operation_mode, status_str)
    print(status_str)
    return status_str


def main():
    args = sys.argv[1:]
    if args[0] == "activate" and not get_wallbox_status():
        activate_wallbox(MANUAL_REASON)
        set_operation_mode(0)
    elif args[0] == "deactivate" and get_wallbox_status():
        deactivate_wallbox(MANUAL_REASON)
        set_operation_mode(0)
    elif args[0] == "auto":
        _, soc = get_current_soc()
        update_wallbox(soc)
    elif args[0] == "enable_auto":
        set_operation_mode(1)
        log_event(ENABLE_AUTO_MSG, MANUAL_REASON)
        _, soc = get_current_soc()
        update_wallbox(soc)
    elif args[0] == "status":
        get_status_str()
    elif (args[0] != "activate" and args[0] != "deactivate" and args[0] != "auto" and
          args[0] != "enable_auto" and args[0] != "status"):
        print("invalid command ({}) specifed to wallbox_control".format(args[0]))
        log_error("invalid command ({}) specifed to wallbox_control".format(args[0]))


if __name__ == "__main__":
    main()
