from ftplib import FTP
import socket
import hashlib
import datetime

from pprint import pprint

class Ftp(object):

  ftp = None
  ip = None
  reachable = False
  anonymousLogin = False
  paths = {}
  currentFileList = []

  def __init__(self, ip:str):
    self.paths = {}
    self.reachable = False
    self.anonymousLogin = False
    self.ip = ip

  def connect(self):
    self.ftp = FTP(self.ip)
    self.reachable = True
    self.ftp.encoding='utf-8'
    self.ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
    #self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)

  def reconnect(self):
    pass

  def login(self):
    if self.ftp is None:
      raise Exception("You need to connect first")
    if not self.ftp.login():
      raise Exception("Not able to connect to given FTP Server %s" % self.ip)
    self.anonymousLogin = True

  def isReachable(self):
    return self.reachable

  def hasAnonymousLogin(self):
    return self.anonymousLogin

  def fingerprint(self):
    fingerprint = ""
    fingerprint += self.ftp.getwelcome()
    fingerprint += self.ftp.sendcmd("HELP")
    fingerprint += self.ftp.sendcmd("SYST")
    fingerprint += self.ftp.sendcmd("FEAT")
    fingerprint += self.getStat()
    fingerprintHash = hashlib.sha224(bytes(fingerprint, 'utf-8')).hexdigest()
    #print(fingerprint)
    return fingerprintHash

  def getStat(self):
    stat = ""
    statOutput = self.ftp.sendcmd("STAT")
    statLines = statOutput.split("\n")
    for statLine in statLines:
      if not statLine.startswith("     Connected to") and not statLine.startswith("     At session startup, client count was"):
        stat += "%s\n" % (statLine)
    return stat

  def deleteFile(self, filename):
    self.ftp.delete(filename)

  def getModifyDate(self, filename):
    output = self.ftp.sendcmd('MDTM %s' % filename)
    if output.startswith("213"):
      output = output.split(" ")
      datestring = output[1]
      year = datestring[:4]
      month = datestring[4:6]
      day = datestring[6:8]
      hour = datestring[8:10]
      minute = datestring[10:12]
      second = datestring[12:14]
      date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
      return date

    return None

  def downloadFile(self, sourceFile, targetFile):
    print("Downloading %s to %s" % (sourceFile, targetFile))
    self.ftp.retrbinary('RETR %s' % sourceFile, open(targetFile, 'wb').write)

  def readPath(self, path):
    self.currentFileList = []
    try:
      self.ftp.dir(path, self.checkDirOutput)
    except:
      self.paths[path] = {
        'files': [],
        'directories': []
      }

    files = []
    directories = []
    for currentFile in self.currentFileList:
      if currentFile['type'] is 'file':
        files.append({
            'name': currentFile['name'],
            'url': "%s/%s" % (path, currentFile['name'])
        })
      else:
        directories.append({
            'name': currentFile['name'],
            'url': "%s/%s" % (path, currentFile['name'])
        })
    self.paths[path] = {
      'files': files,
      'directories': directories
    }
    # todo read modify date by MDTM

  def getFiles(self, path:str):
    if not path in self.paths:
      self.readPath(path)
    return self.paths[path]['files']

  def getDirectories(self, path:str):
    if not path in self.paths:
      self.readPath(path)
    return self.paths[path]['directories']

  def checkDirOutput(self, output):
    lines = output.split("\n")
    for line in lines:
      lineParts = line.split()
      lineParts.pop(0)
      lineParts.pop(0)
      lineParts.pop(0)
      lineParts.pop(0)
      lineParts.pop(0)
      lineParts.pop(0)
      lineParts.pop(0)
      lineParts.pop(0)
      filename = " ".join(lineParts)
      fileObject = {
        'name': filename,
        'type': None
      }
      if line.startswith("d"):
        fileObject['type'] = 'directory'
      else:
        fileObject['type'] = 'file'

      self.currentFileList.append(fileObject)

  def close(self):
    self.paths = {}
    self.reachable = False
    self.anonymousLogin = False
    if self.ftp is None:
      return
    self.ftp.quit()
    self.ftp.close()
