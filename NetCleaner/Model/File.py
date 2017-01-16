from peewee import *
from NetCleaner.Model.Scan import Scan
from NetCleaner.DatabaseConnection import database

class File(Model):
  id = PrimaryKeyField()
  scan = ForeignKeyField(Scan)
  remotePath = CharField()
  localPath = CharField(null = True)
  time = DateTimeField()


  class Meta:
    database = database