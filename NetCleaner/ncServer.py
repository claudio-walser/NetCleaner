#!/usr/bin/env python3

import sys
import argcomplete
import argparse
from pprint import pprint
from NetCleaner.Model.Server import Server
from NetCleaner.Server.Ftp import Ftp
import ftplib

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
      print("Trying to fingerprint %s" % server.ip)
      try:
        ftp = Ftp(server.ip)
        server.fingerprint = ftp.fingerprint()
        server.anonymous = True
        server.reachable = True
        print("Fingerprinted server: %s" % server.ip)
      except (ConnectionRefusedError, TimeoutError, OSError):
        server.reachable = False
        print("Server: %s is not reachable" % server.ip)
      except ftplib.error_perm:
        server.anonymous = False
        print("Server: %s has no anonymous login" % server.ip)
        pass

      server.save()
