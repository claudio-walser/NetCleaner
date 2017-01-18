#!/usr/bin/env python3
import sys
import argcomplete
import argparse
from NetCleaner.Crawler.Ftp import Ftp
from NetCleaner.Model import *
from pprint import pprint

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

def crawl(crawler, path):
  files = crawler.getFiles(path)
  directories = crawler.getDirectories(path)

  pprint(files)
  pprint(directories)
  pass


def main():
  print("starting scanner")
  arguments = parser.parse_args()
  servers = Server.select()
  for server in servers:
    print("Scanning %s" % server.ip)
    crawler = Ftp(server)
    if server.type == 'ftp':
      crawler = Ftp(server.ip)
      crawler.connect()
      crawler.login()
    else:
      raise Exception("No crawler for server type: %s" % server.type)

    crawl(crawler, '/')

    crawler.close()

    # crawler.setSuspiciousFiles(config.get('suspicousFiles'))
    # crawler.setDownloadToCheck(config.get('downloadToCheck'))
    # crawler.setSuspiciousFileExtensions(config.get('suspiciousFileExtensions'))
    # crawler.crawl()
    # crawler.close()

    # print("Get infected file list on server %s" % server.ip)
    # pprint(crawler.getInfectedFiles())


  #pprint(arguments)


