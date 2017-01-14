from peewee import *
from NetCleaner.DatabaseConnection import database

class Server(Model):
  id = PrimaryKeyField()
  ip = CharField()
  fingerprint = CharField(null = True)
  type = CharField()
  time = DateTimeField()
  reachable = BooleanField(null = True)
  anonymous = BooleanField(null = True)


  class Meta:
    database = database