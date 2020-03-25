# SolarWinds Mute and Unmanage script

This script helps with the process of muting or unmanaging large numbers of nodes in SolarWinds. For any questions, don't hesitate to reach out to David, or submit an issue/pull request.

This package utilizes the orionsdk-python package that SolarWinds publishes here: https://github.com/solarwinds/orionsdk-python. See that package for initial setup of the SDK and other problems with the SDK.

## Install

``` shell
ssh SERVER
mkdir ~/gitrepos && cd ~/gitrepos
git clone git@github.com:jdthiele/orionsdk_python_scripts.git
cd orionsdk_python_scripts
python -m venv venv
. venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

``` shell
ssh SERVER  
cd ~/gitrepos/orionsdk_python_scripts
. venv/bin/activate
python -m sw_mute_unmanage -h
```

### Timing Variation Examples

The below examples assume a user of "dthiele" and node of "server1"

- Specify a start and stop date/time  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -m mute -n server1 -s 2019-05-14-00-00 -S 2019-05-15-00-00`
- Specify a start and duration  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -m mute -n server1 -s 2019-05-14-00-00 -d 12h`
- Specify a duration (assumes immediate start) given in days or hours  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -m mute -n server1 -d 30d`
- Specify a stop (assumes immediate start)  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -m mute -n server1 -S 2019-05-15-00-00`
- Specify a start (assumes 1 day duration)  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -m mute -n server1 -s 2019-05-14-00-00`

### Mode Variation Examples

- Mute a server  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -d 4h -m mute -n server1`
- Unmanage a server  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -d 365d -m unmanage -n server1`

### Batch Mode

- pass a comma delimited list of hosts without spaces to mute or unmanaged many nodes at once  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -d 24h -m mute -n server1,server2,server3`
- read the list of hosts from a file/template  
``python -m sw_mute_unmanage -w solarwinds -u dthiele -d 90d -m mute -n `cat serverlist.txt` ``

### Resume Mode

- Unmute and/or remanage a server or set of servers  
`python -m sw_mute_unmanage -w solarwinds -u dthiele -m resume -n server1,server2,server3`
