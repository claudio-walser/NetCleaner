from peewee import *

database = SqliteDatabase("net-cleaner.db")
#database = MySQLDatabase('net-cleaner', charset='utf8')
#database.init('net-cleaner', host='localhost', user='root')


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


class Scan(Model):
  id = PrimaryKeyField()
  server = ForeignKeyField(Server)
  time = DateTimeField()
  completed = BooleanField(default = 0)

  class Meta:
    database = database


class File(Model):
  id = PrimaryKeyField()
  scan = ForeignKeyField(Scan)
  remotePath = CharField()
  localPath = CharField(null = True)
  time = DateTimeField()
  remoteTime = DateTimeField(null = True)
  header = CharField(null = True)

  class Meta:
    database = database


class Virus(Model):
  id = PrimaryKeyField()
  file = ForeignKeyField(File)
  definition = CharField()

  class Meta:
    database = database


class String(Model):
  id = PrimaryKeyField()
  virus = ForeignKeyField(Virus)
  content = CharField()

  class Meta:
    database = database
