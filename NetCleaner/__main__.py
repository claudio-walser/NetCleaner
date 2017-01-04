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

    sys.exit(0)
