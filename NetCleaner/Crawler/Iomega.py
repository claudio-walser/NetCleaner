from ftplib import FTP
import socket
import hashlib
import datetime
import requests
from pprint import pprint



# from pprint import pprint

# url = 'https://79.139.89.73/cp/FolderContents?v=2.3'


# # get root nodes
# url = 'https://79.139.89.73/manage/foldercontent.html'
# r = requests.get(url, verify=False)
# print(r.text)

# # get folder contents

# # path:forum%2F.Thumbnails
# # sortby:name
# # max:20
# # start:0
# # contenttype:all
# payload = {
#   'path': 'Foty',
#   'sortby': 'name',
#   'max': 10000,
#   'start': 0,
#   'contenttype': 'all'
# }
# r = requests.post(url, data=payload, verify=False)



class Iomega(object):

  ip = None
  address = None
  serverVersion = '2.3'
  reachable = False
  paths = {}
  
  def __init__(self, ip:str):
    self.paths = {}
    self.reachable = False
    self.ip = ip
    self.address = 'https://%s/manage/foldercontent.html?v=%s' % (self.serverVersion, self.ip)

  def connect(self):
    url = 'https://%s/cp/FolderContents' % self.ip
    r = requests.get(url, verify=False)
    if r.status_code is 200:
      self.reachable = True
      print("Server reachable")
    else:
      print(r.status_code)

  def reconnect(self):
    pass

  def isReachable(self):
    return self.reachable

  def hasAnonymousLogin(self):
    return True

  def fingerprint(self):
    return 'iomega'

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
