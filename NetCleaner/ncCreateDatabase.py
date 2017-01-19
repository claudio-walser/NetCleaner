#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from NetCleaner.Model import *
from peewee import *


def main():
  print("create database")

  try:
    Server.create_table()
    print("Server table created!")
  except OperationalError:
    print("Server table already exists!")

  try:
    Scan.create_table()
    print("Scan table created!")
  except OperationalError:
    print("Scan table already exists!")

  try:
    File.create_table()
    print("File table created!")
  except OperationalError:
    print("File table already exists!")

  try:
    Virus.create_table()
    print("Virus table created!")
  except OperationalError:
    print("Virus table already exists!")

  try:
    String.create_table()
    print("String table created!")
  except OperationalError:
    print("String table already exists!")
