from storm.locals import *



class Server(object):
  __storm_table__ = "server"
  id = Int(primary=True)
  ip = Unicode()
  fingerprint = Unicode()
  type = Unicode()
