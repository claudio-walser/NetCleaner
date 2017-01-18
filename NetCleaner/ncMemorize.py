#!/usr/bin/env python3

import sys
import argcomplete
import argparse
import json
import datetime
from pprint import pprint

from NetCleaner.Model import *

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

parser.add_argument(
    '-t', "--type",
    help="What type of servers you want to import?",
    type=str,
    choices=['ftp', 'iomega'],
    required=True
)
parser.add_argument(
    "--from",
    help="Whats the source of your data?",
    type=str,
    choices=['shodan'],
    required=True
)


parser.add_argument(
    "--file",
    help="Where is the file you want to import?",
    type=str,
    required=True
)
argcomplete.autocomplete(parser)



def main():
  print("memorize main function")

  arguments = parser.parse_args()
  serverType = arguments.type
  importFile = arguments.file


  servers = []
  for line in open(importFile, 'r'):
    serverIp = json.loads(line)['ip_str']
    print("adding server ip: %s" % serverIp)
    server = Server(
      ip = serverIp,
      type = serverType,
      time = datetime.datetime.now()
    )
    server.save()

  # with open(importFile, 'r') as stream:
  #   servers = json.load(stream)

  pprint(servers)


