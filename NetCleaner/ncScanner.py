#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse
from NetCleaner.Crawler.Ftp import Ftp
from NetCleaner.Analyser.Clamscan import Clamscan
from NetCleaner.Model import *
import shutil
import datetime
import os
import ftplib
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
arguments = parser.parse_args()
tmpFile = '/tmp/ftp-file-to-check'

def crawl(crawler, path, scan, server):
  print("crawling %s" % path)
  files = crawler.getFiles(path)
  directories = crawler.getDirectories(path)
  print("files from directory: %s " % path)
  pprint(files)
  print("directories from directory: %s " % path)
  pprint(directories)

  try:
    # todo implement reconnect in case of timeout or EORError
    for file in files:
      filePath = "%s/%s" % (path, file)
      try:
        fileModel = File(
          scan = scan,
          remotePath = filePath,
          time = datetime.datetime.now()
        )
        fileModel.save()

        crawler.downloadFile(filePath, tmpFile)

        scanner = Clamscan(tmpFile)
        scanner.scan()
        if scanner.getIsVirus():
          try:
            crawler.getModifyDate(filePath)
          except Exception as e:
            print(str(e))
          if arguments.cleanup is True:
            try:
              crawler.deleteFile(filePath)
            except ftplib.error_perm:
              print("No permissions to delete file %s" % filePath)
          destinationPath = "downloadedFiles/ftp-%s/%s%s" % (server.ip, scan.time, path)
          if not os.path.exists(destinationPath):
            os.makedirs(destinationPath)

          shutil.move('/tmp/ftp-file-to-check', "%s/%s" % (destinationPath, file))
          fileModel.localPath = "%s%s" % (destinationPath, file)
          fileModel.save()

          virus = Virus(
            file = fileModel,
            definition = scanner.getVirusDefinition()
          )
          virus.save()

      except ftplib.error_perm:
        print("no permissions to download file")

    for directory in directories:
      crawl(crawler, "%s/%s" % (path, directory), scan, server)
  except Exception as e:
    raise e
    print("Exception occured: %s" % str(e))

def main():
  print("starting scanner")
  servers = Server.select()
  for server in servers:
    print("Scanning %s" % server.ip)
    crawler = Ftp(server)
    if server.type == 'ftp':
      try:
        crawler = Ftp(server.ip)
        crawler.connect()
        crawler.login()
      except:
        server.reachable = crawler.isReachable()
        server.anonymous = crawler.hasAnonymousLogin()
        server.save()
    else:
      raise Exception("No crawler for server type: %s" % server.type)

    scan = Scan(
      server = server,
      time = datetime.datetime.now()
    )
    scan.save()
    crawl(crawler, '', scan, server)
    crawler.close()
