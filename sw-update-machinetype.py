# imports
import requests
import orionsdk
import argparse
import getpass
import sys

# disable some annoying warning about SSL i think it was
requests.packages.urllib3.disable_warnings()

# define the variables needed for automating the process
npm_server = 'SolarWinds-Orion'
#cert='server.pem'

# handle some arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="Provide the user to connect to the OrionSDK as", required=True)
parser.add_argument("-p", "--password", help="Provide the password for the given user")
parser.add_argument("-n", "--node", help="Provide the node you want to update the machinetype property on", required=True)
parser.add_argument("-m", "--machinetype", help="Provide the name of the MachineType to set", required=True)
args = parser.parse_args()
user = args.user
node = args.node
machinetype = args.machinetype

# ask for a password if not provided in args
if args.password:
    password = args.password
else:
    password = getpass.getpass()

# load the swis client and login to the NPM server
swis = orionsdk.SwisClient(npm_server, user, password, verify=False)

# run the query and save the output
uri_query = 'SELECT Uri from Orion.Nodes where Caption=\'' + node + '\''
results = swis.query(uri_query)
if results['results'] == []:
    print('Did not find a host with this name. Exitting.')
    sys.exit(1)
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
