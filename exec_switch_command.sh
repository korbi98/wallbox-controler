#!/bin/bash

Help()
{
   # Display Help
   echo "Command line script for executing commands on AVM smarthome switch."
   echo "IP and login data of switch is configured in script"
   echo
   echo "Syntax: exec_switch_command [-h|v|c]"
   echo "options:"
   echo "h     Print this Help."
   echo "v     Verbose mode."
   echo "c     Specify command to be executed (required)."
   echo
   echo "for possible commands see 'https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf'"
}


VERBOSE=false

while getopts :hvc: flag
do
    case "${flag}" in
	h) Help && exit;;
        c) COMMAND=${OPTARG};;
        v) VERBOSE=true;;
        \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
    esac
done

[ "$COMMAND" == "" ] && echo "No command provided see 'https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf' for possible commands" && exit

# -----------
# definitions
# -----------
FBF="http://192.168.188.1" # Your FritzBox IP
USER="YourUserName"
PASS="YourPassword"
AIN="YourAIN" # 11 digit number identifing the switch
# ---------------
# fetch challenge
# ---------------
CHALLENGE=$(curl -s "${FBF}/login_sid.lua" | grep -Po '(?<=<Challenge>).*(?=</Challenge>)')	
( $VERBOSE ) && echo "Challenge: "$CHALLENGE

# -----
# login
# -----
MD5=$(echo -n ${CHALLENGE}"-"${PASS} | iconv -f ISO8859-1 -t UTF-16LE | md5sum -b | awk '{print substr($0,1,32)}')
RESPONSE="${CHALLENGE}-${MD5}"
SID=$(curl -i -s -k -d "response=${RESPONSE}&username=${USER}" "${FBF}" | awk -F '"sid":' '{print $2}' | awk -F '"' '{print $2}' | awk NF)
( $VERBOSE ) && echo "Login-Response: "$RESPONSE && echo "SID: "$SID

# -----------------
# execute and echo response of command
# -----------------
COMMAND_URL=${FBF}'/webservices/homeautoswitch.lua?ain='${AIN}'&switchcmd='${COMMAND}'&sid='${SID} 
( $VERBOSE ) && echo "Command-URL: "$COMMAND_URL && RESULT_STR="Result: " || RESULT_STR=""
echo $RESULT_STR$(curl -s $COMMAND_URL)
