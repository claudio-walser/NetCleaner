#!/usr/bin/env python3
import sys
import argcomplete
import argparse
from NetCleaner.Crawler.Ftp import Ftp
from NetCleaner.Model.Server import Server
from pprint import pprint
from NetCleaner.Config.Config import Config

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

#nc-scanner scan --rescan --check-by-download --cleanup
parser.add_argument(
    '-r', "--rescan",
    help="Rescan servers which are already scanned",
    action='store_true'
)

parser.add_argument(
    '-cbd', "--check-by-download",
    help="Check any file by download it to /tmp first",
    action='store_true'
)

parser.add_argument(
    '-c', "--cleanup",
    help="Cleanup the files on remote if infected",
    action='store_true'
)

argcomplete.autocomplete(parser)


def main():
  print("starting scanner")
  arguments = parser.parse_args()
  config = Config()
  servers = Server.select()
  for server in servers:
    print("Scanning %s" % server.ip)
    crawler = Ftp(server)
    # if str(server.type) is 'ftp':
    #   crawler = Ftp(server)
    # else:
    #   raise Exception("No crawler found for type %s" % server.type)

    crawler.setSuspiciousFiles(config.get('suspicousFiles'))
    crawler.setDownloadToCheck(config.get('downloadToCheck'))
    crawler.setSuspiciousFileExtensions(config.get('suspiciousFileExtensions'))
    crawler.crawl()
    crawler.close()

    print("Get infected file list on server %s" % server.ip)
    pprint(crawler.getInfectedFiles())


  #pprint(arguments)


