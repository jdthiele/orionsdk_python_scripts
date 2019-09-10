# imports
import requests
import orionsdk
import argparse
import getpass
import sys
import urllib3
import pandas as pd
from datetime import datetime

# disable insecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# define some help menu strings

help_header = """This script will help automate the process of updating custom property values in SolarWinds.

Refer to https://github.com/jdthiele/orionsdk-python_scripts for detailed help."""

# handle some arguments
parser = argparse.ArgumentParser(description=help_header)
parser.add_argument("-s", "--npm_server", help="Provide the name of the SolarWinds server", required=True)
parser.add_argument("-u", "--user", help="Provide the user to connect to the OrionSDK as", required=True)
parser.add_argument("-p", "--password", help="Provide the password for the given user, or omit to be prompted")
parser.add_argument("-n", "--nodes", help="Provide the node (or comma separated nodes) you want to update the property on", required=False)
parser.add_argument("-c", "--customproperty", help="Provide the property to update, where \"all\" will read csvfile for all properties", required=False)
parser.add_argument("-v", "--value", help="Provide the value to set for the given property", required=False)
parser.add_argument("-f", "--file", help="Provide the csv file to lookup property and values from for a set of hosts", required=False)
args = parser.parse_args()
npm_server = args.npm_server
user = args.user
nodes = args.nodes
if nodes:
  nodes = nodes.split(",")
custom_property = args.customproperty
desired_val = args.value
csvfile = args.file

if not csvfile and not custom_property:
  if not nodes and not custom_property and not desired_val:
    print("Please provide either the file and property args or the node, property and value args")
    sys.exit(3)

# ask for a password if not provided in args
if args.password:
    password = args.password
else:
    password = getpass.getpass()

# load the swis client and login to the NPM server
swis = orionsdk.SwisClient(npm_server, user, password, verify=False)

### Define some functions

# get the hosts
def get_nodes_from_csv(csv_data):
  up_rows = csv_data[csv_data.Status == "Up"]
  hosts = up_rows[['Physical','LDOM-VM','Zones']]
  print(hosts)
  sys.exit()
  return


# validate the property is in the dataframe


# run the query to get the node URI and save the output
def get_node_uri (node, swis):
  uri_query = 'SELECT Uri from Orion.Nodes where Caption=\'' + node + '\''
  results = swis.query(uri_query)
  if results['results'] == []:
      print('Did not find a host with this name. Exitting.')
      sys.exit(1)
  nodeuri = results['results'][0]['Uri']
  uri = nodeuri + '/CustomProperties'
  return nodeuri, uri


# check of the custom property exists and what the current value is
def check_current_prop_value(uri, swis, custom_property):
  obj = swis.read(uri)
  current_val = ""
  if custom_property in obj:
    current_val = obj[custom_property]
  else:
    print("The custom property " + custom_property + " does not exist. Exitting.")
    sys.exit(2)
  return current_val


# check if the value is valid
def check_desired_prop_value(custom_property, swis, desired_val):
  query = 'select Value from Orion.CustomPropertyValues where Field=\'' + custom_property + '\''
  results = swis.query(query)
  avail_values = []
  for dict in results["results"]:
    v = dict["Value"]
    avail_values.append(v)
  
  if desired_val not in avail_values:
    print("The value you provided is not in the list of existing values. Please use one of: ")
    print(avail_values)
    sys.exit(4)
  return


# if the given value is different than current, update it
def change_prop_val(current_val, desired_val, custom_property, swis, uri, node):
  if current_val == desired_val:
    print("The value " + desired_val + " is already set")
  else:
    props = {custom_property: desired_val}
    swis.update(uri, **props)
    # print the new value if changed
    obj = swis.read(uri)
    print("Changed " + custom_property + " to \"" + desired_val + "\" on " + node)

### Main
if csvfile:
  # load the csv file into a dict or dataframe??
  csv_data = pd.read_csv(csvfile)
  # parse the 3 hosts columns to get the actual host (rightmost)
  get_nodes_from_csv(csv_data)
  # get the property to load into SW
  # loop through each host
  for node in nodes:
    # get the uri for the node
    nodeuri, uri = get_node_uri(node, swis)
    # loop through each property
    for custom_property in custom_properties:
      # get the current value if any
      current_val = check_current_prop_value(uri, swis, custom_property)
      # check if the proposed value is valid
      check_desired_prop_value(custom_property, swis, desired_val)
      # if current is different from desired, change it
      change_prop_val(current_val, desired_val, custom_property, swis, uri, node)
else:
  # loop through all hosts provided
  for node in nodes:
    # get the uri for the node
    nodeuri, uri = get_node_uri(node, swis)
    # get the current value for the provided property
    current_val = check_current_prop_value(uri, swis, custom_property)
    # check if the proposed value is valid
    check_desired_prop_value(custom_property, swis, desired_val)
    # if current is different from desired, change it
    change_prop_val(current_val, desired_val, custom_property, swis, uri, node)

# Exit with a code of 0 indicating all went well
sys.exit(0)