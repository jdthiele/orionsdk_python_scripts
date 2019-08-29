# imports
import requests
import orionsdk
import argparse
import getpass
import sys
import urllib3
from datetime import datetime

# disable insecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# define some help menu strings

help_header = """This script will help automate the process of updating custom attribute values in SolarWinds.

Refer to https://github.com/jdthiele/orionsdk-python_scripts for detailed help."""

# handle some arguments
parser = argparse.ArgumentParser(description=help_header)
parser.add_argument("-s", "--npm_server", help="Provide the name of the SolarWinds server", required=True)
parser.add_argument("-u", "--user", help="Provide the user to connect to the OrionSDK as", required=True)
parser.add_argument("-p", "--password", help="Provide the password for the given user, or omit to be prompted")
parser.add_argument("-n", "--node", help="Provide the node you want to update the machinetype property on", required=True)
parser.add_argument("-c", "--customproperty", help="Provide the attribute to update", required=True)
parser.add_argument("-v", "--value", help="Provide the value to set for the given attribute", required=True)
args = parser.parse_args()
npm_server = args.npm_server
user = args.user
node = args.node
custom_property = args.customproperty
custom_val = args.value

# ask for a password if not provided in args
if args.password:
    password = args.password
else:
    password = getpass.getpass()

# load the swis client and login to the NPM server
swis = orionsdk.SwisClient(npm_server, user, password, verify=False)

# run the query to get the node URI and save the output
uri_query = 'SELECT Uri from Orion.Nodes where Caption=\'' + node + '\''
results = swis.query(uri_query)
if results['results'] == []:
    print('Did not find a host with this name. Exitting.')
    sys.exit(1)
nodeuri = results['results'][0]['Uri']
uri = nodeuri + '/CustomProperties'

# check of the custom property exists and what the current value is
obj = swis.read(uri)
current_val = ""
if custom_property in obj:
  current_val = obj[custom_property]
else:
  print("The custom property " + custom_property + " does not exist. Exitting.")
  sys.exit(1)

# check if the value is valid
query = 'select Value from Orion.CustomPropertyValues where Field=\'' + custom_property + '\''
results = swis.query(query)
avail_values = []
for dict in results["results"]:
  v = dict["Value"]
  avail_values.append(v)

if custom_val not in avail_values:
  print("The value you provided is not in the list of existing values. Please use one of: ")
  print(avail_values)
  sys.exit(2)

# if the given value is different than current, update it
if current_val == custom_val:
  print("The value " + custom_val + " is already set")
  sys.exit(0)
else:
  props = {custom_property: custom_val}
  swis.update(uri, **props)

# print the new value if changed
obj = swis.read(uri)
print("Changed " + custom_property + " to: " + custom_val)

# Exit with a code of 0 indicating all went well
sys.exit(0)