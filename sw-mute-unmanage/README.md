# SolarWinds Mute and Unmanage script

This script helps with the process of muting or unmanaging large numbers of nodes in SolarWinds. For any questions, don't hesitate to reach out to David, or submit an issue/pull request.

This package utilizes the orionsdk-python package that SolarWinds publishes here: https://github.com/solarwinds/orionsdk-python. See that package for initial setup of the SDK and other problems with the SDK.

## Install

``` shell
ssh SERVER
mkdir ~/gitrepos && cd ~/gitrepos
git clone git@github.com:jdthiele/orionsdk-python_scripts.git
cd orionsdk-python_scripts/sw-mute-unmanage
pip3 install virtualenv
virtualenv venv
. ../venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

``` shell
ssh SERVER  
cd ~/gitrepos/orionsdk-python_scripts/sw-mute-unmanage  
. ../venv/bin/activate
```

### Timing Variation Examples

The below examples assume a user of "dthiele" and node of "server1"

- Specify a start and stop date/time  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -m mute -n server1 -s 2019-05-14-00-00 -S 2019-05-15-00-00`
- Specify a start and duration  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -m mute -n server1 -s 2019-05-14-00-00 -d 12h`
- Specify a duration (assumes immediate start) given in days or hours  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -m mute -n server1 -d 12h`
- Specify a stop (assumes immediate start)  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -m mute -n server1 -S 2019-05-15-00-00`
- Specify a start (assumes 1 day duration)  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -m mute -n server1 -s 2019-05-14-00-00`

### Mode Variation Examples

- Mute a server  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -d 12h -m mute -n server1`
- Unmanage a server  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -d 12h -m unmanage -n server1`

### Batch Mode

- pass a comma delimited list of hosts without spaces to mute or unmanaged many nodes at once  
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -d 12h -m mute -n server1,server2,server3`
- read the list of hosts from a file/template  
``python3 sw-mute-unmanage.py -w solarwinds -u dthiele -d 12h -m mute -n `cat serverlist.txt` ``

### Resume Mode

- Unmute and/or remanage a server or set of servers
`python3 sw-mute-unmanage.py -w solarwinds -u dthiele -m resume -n server1,server2,server3`
