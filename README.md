# wallbox-controler

Controlling a wallbox (for charging a car) depending on state of charge of battery (battery storage for solar not battery of car). To get the SOC of the battery [
SBFspot](https://github.com/SBFspot/SBFspot) which get the SOC from the SMA battery inverter, is used. It should be
configured to store the data in CSV files for individual days. Make sure that the *-finq* flag is used to ensure that the data is also aquired during the night. 
The project consists of a shell script that can send commands to an AVM FRITZ!DECT smart plug controlling the wallbox. On top of that python in combination with 
pandas is used to load the battery SOC and decide if the state of the plug should be changed. Additionally a simple web interface is provided to see the battery SOC
and to manually change the state and mode (auto or manual) of the wallbox. In manual mode the wallbox stays on/off independent of the battery SOC.

Both SBFspot and the python script should be executed periodically. This can be done for example via crontab under Unix. /etc/crontab should look like this for
a 5 minute update interval:
```
*/5 * * * * /home/pi/wallbox_controller/wallbox_control.py auto
## SBFspot
*/5 * * * * /usr/local/bin/sbfspot.3/daydata
