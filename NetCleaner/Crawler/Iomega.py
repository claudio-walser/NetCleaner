from ftplib import FTP
import socket
import hashlib
import datetime
import requests
import urllib
from pprint import pprint
import sys
# disable InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
  anonymousLogin = False
  paths = {}

  def __init__(self, ip:str):
    self.paths = {}
    self.reachable = False
    self.anonymousLogin = False
    self.ip = ip
    self.address = 'https://%s/manage/foldercontent.html?v=%s' % (self.serverVersion, self.ip)

  def connect(self):
    url = 'https://%s/cp/FolderContents' % self.ip
    r = requests.get(url, verify=False)
    if r.status_code is 200:
      self.reachable = True
      self.anonymousLogin = True
      print("Server reachable")
    else:
      print(r.status_code)

  def reconnect(self):
    pass

  def isReachable(self):
    return self.reachable

  def hasAnonymousLogin(self):
    return self.anonymousLogin

  def fingerprint(self):
    return 'iomega'

  def deleteFile(self, filename):
    pass

  def getModifyDate(self, filename):
    return None

  def downloadFile(self, sourceFile, targetFile):
    print("Downloading %s to %s" % (sourceFile, targetFile))
    with open(targetFile, 'wb') as handle:
        response = requests.get("https://%s%s" % (self.ip, sourceFile), stream=True, verify=False)
        if not response.ok:
            return False
        for block in response.iter_content(1024):
            handle.write(block)
        return True

  def readPath(self, path:str):
    directories = []
    files = []
    realPath = path

    if path == '':
      directories = self.readRootNodes()
    else:
      parseNode = {
        'name': path
      }
      folderName = urllib.quote_plus(path)

      payload = {
        'path': folderName,
        'sortby': 'name',
        'max': 10000,
        'start': 0,
        'contenttype': 'all'
      }
      url = 'https://%s/cp/FolderContents?v=2.3' % self.ip
      r = requests.post(url, data=payload, verify=False)

      for item in r.json()['items']:
        if item['access'] == 'readwrite' or item['access'] == 'read':
          if 'type' in item and item['type'] == 'folder':
            directories.append({
                'name': item['name'],
                'url': "%s/%s" % (path, item['name'])
            })
          else:
            files.append({
                'name': item['name'],
                'url': item['url']
            })

    self.paths[realPath] = {
      'files': files,
      'directories': directories
    }


  def readRootNodes(self):
    rootNodes = []
    url = 'https://%s/cp/Shares?v=2.3&user=&protocol=webaccess' % self.ip
    r = requests.get(url, verify=False)
    for item in r.json()['items']:
      if item['access'] == 'readwrite' or item['access'] == 'read':
        rootNodes.append({
          'name': item['name'],
          'url': item['name']
        })

    return rootNodes

  def getFiles(self, path:str):
    if not path in self.paths:
      self.readPath(path)
    return self.paths[path]['files']

  def getDirectories(self, path:str):
    if not path in self.paths:
      self.readPath(path)
    return self.paths[path]['directories']

  def close(self):
    self.paths = {}
    pass
