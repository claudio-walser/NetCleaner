#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argcomplete
import argparse
from NetCleaner.Model import *
from NetCleaner.Crawler.Ftp import Ftp

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

parser.add_argument(
    '-f', "--fingerprint",
    help="Fingerprint your servers",
    action='store_true'
)
argcomplete.autocomplete(parser)

def main():
  print("server main function")

  arguments = parser.parse_args()
  if arguments.fingerprint:
    servers = Server.select().where((Server.fingerprint >> None) & (Server.reachable >> None) & (Server.anonymous >> None))
    
    for server in servers:
      print()
      print()
      if server.type == 'ftp':
        try:
          crawler = Ftp(server.ip)
          crawler.connect()
          crawler.login()
          server.fingerprint = crawler.fingerprint()

          print("Fingerprinted server %s" % server.ip)
          print(server.fingerprint)
        except:

          server.reachable = crawler.isReachable()
          server.anonymous = crawler.hasAnonymousLogin()
          print("Failed to fingerprint")
          print("reachable: %s" % server.reachable)
          print("anonymous login: %s" % server.anonymous)
      else:
        raise Exception("No crawler for server type: %s" % server.type)

      server.save()
