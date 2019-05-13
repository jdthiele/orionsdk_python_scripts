# imports
import requests
import orionsdk
import argparse
import getpass
import sys
import validations

# define the variables needed for automating the process
npm_server = 'SolarWinds-Orion'
cert='server.pem'

# handle some arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="Provide the user to connect to the OrionSDK as", required=True)
parser.add_argument("-p", "--password", help="Provide the password for the given user")
parser.add_argument("-n", "--node", help="Provide the node you want to blackout", required=True)
parser.add_argument("-m", "--method", help="Provide the blackout method you want to use in SolarWinds - Mute / Unmanage", required=True)
parser.add_argument("-s", "--start", help="Provide the start time")
parser.add_argument("-S", "--stop", help="Provide the stop time")
parser.add_argument("-d", "--duration", help="Provide the duration")
args = parser.parse_args()
user = args.user
node = args.node
method = args.method
start = args.start
stop = args.stop
duration = args.duration

# check for proper timing type arguments
if start or stop or duration:
    if stop and duration:
        print("I cannot take a stop time with duration")
        sys.exit(2)
else:
    print("please provide a start stop or duration argument")
    sys.exit(1)

# set the plan timing type and validate/calculate values
if start and stop:
    timetype = "startandStop"
    # validate start
    startdate = val_start(start)
    # validate stop
elif start and duration:
    timetype = "startandDuration"
    # validate start
    # validate duration
    # calculate stop
elif start:
    timetype = "start"
    duration = "1d"
    # validate start
    # calculate stop as "duration" from start
elif stop:
    timetype = "stop"
    # validate stop
    # calculate start as now
elif duration:
    timetype = "duration"
    # validate duration
else:
    print("how did you get here??")

# ask for a password if not provided in args
if args.password:
    password = args.password
else:
    password = getpass.getpass()

# load the swis client and login to the NPM server
swis = orionsdk.SwisClient(npm_server, user, password, verify=False)

# check if the node(s) is/are already muted/unmanaged

# run the query and save the output
uri_query = 'SELECT Uri from Orion.Nodes where Caption=\'' + node + '\''
results = swis.query(uri_query)
uri = results['results'][0]['Uri']

# update the property
obj = swis.read(uri)
print('Before - MachineType: ' + obj['MachineType'])
print('         SysObjectID: ' + obj['SysObjectID'])
swis.update(uri, MachineType=machinetype, SysObjectID=machinetype)
obj = swis.read(uri)
print('After -  MachineType: ' + obj['MachineType'])
print('         SysObjectID: ' + obj['SysObjectID'])

# get the Technology Polling Assignment URI
uri_query = 'SELECT N.NodeID, T.Uri FROM Orion.TechnologyPollingAssignments T JOIN Orion.Nodes N ON N.NodeID = T.InstanceID WHERE N.Caption = \'' + node + '\' AND T.TechnologyPollingID = \'Core.Node.NodeDetails\' AND T.TargetEntity = \'Orion.Nodes\''
results = swis.query(uri_query)
uri = results['results'][0]['Uri']
netObjId = results['results'][0]['NodeID']
netObjIdList = [netObjId]

# update the property
obj = swis.read(uri)
print('Before - NodeDetails Polling Enabled: ' + str(obj["Enabled"]))
#swis.update(uri, Enabled=False)
swis.invoke('Orion.TechnologyPollingAssignments', 'DisableAssignmentsOnNetObjects', 'Core.Node.NodeDetails', netObjIdList)
obj = swis.read(uri)
print('After  - NodeDetails Polling Enabled: ' + str(obj['Enabled']))

# Exit with a code of 0 indicating all went well
sys.exit(0)