from peewee import *
from NetCleaner.Model.Server import Server
from NetCleaner.DatabaseConnection import database

class Scan(Model):
  id = PrimaryKeyField()
  server = ForeignKeyField(Server)
  time = DateTimeField()
  completed = BooleanField()


  class Meta:
    database = database