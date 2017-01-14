from peewee import *
from NetCleaner.Model.Scan import Scan
from NetCleaner.DatabaseConnection import database

class Virus(Model):
  id = PrimaryKeyField()
  file = ForeignKeyField(Scan)
  definition = CharField()

  class Meta:
    database = database