# PYTHON_ARGCOMPLETE_OK

import sys
from NetCleaner.Config.Config import Config
from NetCleaner.Config.Input import Input
from NetCleaner.Crawler.Ftp import Ftp


from pprint import pprint


def main():
    config = Config()
    inputConfig = Input()

    ftpIps = inputConfig.get('ftp')
    if ftpIps:
      for ftpIp in ftpIps:
        crawler = Ftp(ftpIp)
        crawler.setSuspiciousFiles(config.get('suspicousFiles'))
        crawler.setDownloadToCheck(config.get('downloadToCheck'))
        crawler.setSuspiciousFileExtensions(config.get('suspiciousFileExtensions'))
        crawler.crawl()
        crawler.close()

        print("Get potentially infected file list on server %s" % ftpIp)
        pprint(crawler.getInfectedFiles())

    sys.exit(0)
