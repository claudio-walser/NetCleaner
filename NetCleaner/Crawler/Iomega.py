from ftplib import FTP
import socket
import hashlib
import datetime

from pprint import pprint

class Iomega(object):

  ip = None
  reachable = False
  paths = {}
  
  def __init__(self, ip:str):
    self.paths = {}
    self.reachable = False
    self.ip = ip

  def connect(self):
    pass

  def reconnect(self):
    pass

  def isReachable(self):
    return self.reachable

  def hasAnonymousLogin(self):
    return True

  def fingerprint(self):
    pass

  def deleteFile(self, filename):
    pass

  def getModifyDate(self, filename):
    return None

  def downloadFile(self, sourceFile, targetFile):
    pass

  def getFiles(self, path:str):
    return []

  def getDirectories(self, path:str):
    return []

  def close(self):
    pass
