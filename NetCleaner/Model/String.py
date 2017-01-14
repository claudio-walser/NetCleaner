from peewee import *
from NetCleaner.Model.Virus import Virus
from NetCleaner.DatabaseConnection import database

class String(Model):
  id = PrimaryKeyField()
  virus = ForeignKeyField(Virus)
  content = CharField()

  class Meta:
    database = database