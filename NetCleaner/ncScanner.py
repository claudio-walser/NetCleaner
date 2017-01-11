#!/usr/bin/env python3

import sys
import argcomplete
import argparse
from pprint import pprint

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

#nc-scanner scan --rescan --check-by-download --cleanup
parser.add_argument(
    '-r', "--rescan",
    help="Rescan servers which are already scanned",
    type=str
)

parser.add_argument(
    '-cbd', "--check-by-download",
    help="Check any file by download it to /tmp first",
    type=str
)

parser.add_argument(
    '-c', "--cleanup",
    help="Cleanup the files on remote if infected",
    type=str
)

argcomplete.autocomplete(parser)



def main():
  print("scanner main function")

  arguments = parser.parse_args()
  pprint(arguments)


