#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argcomplete
import argparse
from NetCleaner.Model import *
from NetCleaner.Crawler.Ftp import Ftp
from NetCleaner.Crawler.Iomega import Iomega

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
      
      try:
        if server.type == 'ftp':
          crawler = Ftp(server.ip)
        elif server.type == 'iomega':
          crawler = Iomega(server.ip)
        else:
          raise Exception("No crawler for server type: %s" % server.type)
        crawler.connect()
        crawler.login()
        server.fingerprint = crawler.fingerprint()

        print("Fingerprinted server %s" % server.ip)
        print(server.fingerprint)
      except:
        print("Failed to fingerprint %s" % server.ip)

      server.reachable = crawler.isReachable()
      server.anonymous = crawler.hasAnonymousLogin()
      server.save()
