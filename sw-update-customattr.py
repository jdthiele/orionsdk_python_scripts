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

help_header = """This script will help automate the process of getting a hosts listing from SolarWinds

Refer to https://github.com/jdthiele/orionsdk-python_scripts for detailed help."""

# handle some arguments
parser = argparse.ArgumentParser(description=help_header)
parser.add_argument("-s", "--npm_server", help="Provide the name of the SolarWinds server", required=True)
parser.add_argument("-u", "--user", help="Provide the user to connect to the OrionSDK as", required=True)
parser.add_argument("-p", "--password", help="Provide the password for the given user, or omit to be prompted")
parser.add_argument("-a", "--attribute", help="Provide the attribute to update", required=True)
parser.add_argument("-v", "--value", help="Provide the value to set for the given attribute", required=True)
args = parser.parse_args()
npm_server = args.npm_server
user = args.user
custom_attr = args.attribute
custom_val = args.value

# ask for a password if not provided in args
if args.password:
    password = args.password
else:
    password = getpass.getpass()

# load the swis client and login to the NPM server
swis = orionsdk.SwisClient(npm_server, user, password, verify=False)

# define the query to run via the client
query1 = """
select n.Caption
from
  Orion.Nodes n
JOIN
  Orion.NodesCustomProperties c
  ON n.nodeid = c.nodeid
WHERE c.ManagingTeam = 'UNIX'
ORDER BY n.caption;"
"""

# run the query and save the output
queryresults = swis.query(query1)

# print the output in a human readable format
for row in queryresults['results']:
    print ("{Caption}".format(**row))

# Exit with a code of 0 indicating all went well
sys.exit(0)
