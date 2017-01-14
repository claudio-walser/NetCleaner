#!/usr/bin/env python3
from NetCleaner.Model.Server import Server
from NetCleaner.Model.Scan import Scan
from NetCleaner.Model.File import File
from NetCleaner.Model.Virus import Virus
from NetCleaner.Model.String import String
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
