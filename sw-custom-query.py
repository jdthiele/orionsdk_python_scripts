# imports
import requests
import orionsdk
import argparse
import getpass
import sys
import pandas
import json

# disable some annoying warning about SSL i think it was
requests.packages.urllib3.disable_warnings()

# define the variables needed for automating the process
npm_server = 'SolarWinds-Orion'
cert='server.pem'
printcsv = False

# handle some arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="Provide the user to connect to the OrionSDK as", required=True)
parser.add_argument("-p", "--password", help="Provide the password for the orionsdk-api user. Look in KeePass")
parser.add_argument("-f", "--queryfile", help="Provide the path to the SWQL query file you want to run against the SW database", required=True)
parser.add_argument("-c", "--csv", help="Print in csv format", action='store_true')
args = parser.parse_args()
user = args.user
queryfile = args.queryfile

# switch the printcsv variable if the csv argument was given
if args.csv:
  printcsv = True

# ask for a password if not provided in args
if args.password:
    password = args.password
else:
    password = getpass.getpass()

# load the swis client and login to the NPM server
swis = orionsdk.SwisClient(npm_server, user, password, verify=cert)

# define the query to run via the client
with open(queryfile) as f:
  query1 = f.read()

# run the query and save the output
results = swis.query(query1)
results_json = json.dumps(results["results"])

# print the output in the needed format
results_df = pandas.read_json(results_json)
if printcsv == False:
  print(results_df.to_string())
else:
  results_csv = results_df.to_csv(index=False)
  print(results_csv)


# Exit with a code of 0 indicating all went well
sys.exit(0)
