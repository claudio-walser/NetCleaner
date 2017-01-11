#!/usr/bin/env python3

import sys
import argcomplete
import argparse
from pprint import pprint

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

parser.add_argument(
    '-f', "--fingerprint",
    help="Fingerprint your servers",
    type=str
)
argcomplete.autocomplete(parser)



def main():
  print("server main function")

  arguments = parser.parse_args()
  pprint(arguments)


