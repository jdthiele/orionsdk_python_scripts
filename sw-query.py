#!/usr/bin/python3
#
# Title: sw-query.py
# Author: David Thiele
# Date Created: 2018-01-15
# Date Revised: YYYY-MM-DD
# Revision: 1.0
# Purpose: automate the pull down of a host list from SolarWinds
#   This script can be repurposed to run basically any query.
#
# Prerequisites:
#   - python3 installed
#   - orionsdk python pip package installed
#   - SSL cert downloaded and available for this script to use
#   - local entry in /etc/hosts for SolarWinds-Orion
#   - All of this is done on mon03dp already
#
# Logic;
#
# The output is tee to stdout and the log file
# Calling scripts:
# Called scripts:
# Exit code: 0 indicates all went well.
#            1 indicates an error.
# Constants:

# Variables:
# None to declare here

#############
# Functions
#############
# None

#function one {
#   return 0
#}

#############
# Main
#############

import requests
import orionsdk
import argparse
import getpass
import sys

# disable some annoying warning about SSL i think it was
requests.packages.urllib3.disable_warnings()

# define the variables needed for automating the process
npm_server = 'SolarWinds-Orion'
username = 'orionuser'
cert='server.pem'

# get the password from the -p argument or prompt the user if needed
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--password", help="Provide the password for the orionuser account")
args = parser.parse_args()
if args.password:
    password = args.password
else:
    password = getpass.getpass()

# load the swis client and login to the NPM server
swis = orionsdk.SwisClient(npm_server, username, password, verify=cert)

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
