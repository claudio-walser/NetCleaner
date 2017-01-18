import ftplib
import sys
from NetCleaner.Analyser.Clamscan import Clamscan
from NetCleaner.Analyser.Strings import Strings
from NetCleaner.Model.Scan import Scan
from NetCleaner.Model.File import File
from NetCleaner.Model.Virus import Virus
from NetCleaner.Model.String import String
from pprint import pprint
import os
import shutil
import datetime
import socket


class Ftp(object):

  ftp = None
  serverUrl = None
  tmpPath = '/tmp/ftp-file-to-check'

  server = None
  scan = None

  suspicousFiles = []
  suspiciousFileExtensions = []
  downloadToCheck = False

  currentFileList = []
  fileList = []
  infectedFileList = []

  def __init__(self, server:str):
    self.server  = server
    self.ftp = ftplib.FTP(server.ip)
    if not self.ftp.login():
      raise Exception("Not able to connect to given FTP Server %s" % server.ip)

    self.ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
    self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
    #self.ftp.set_debuglevel(2)
    self.serverUrl = 'ftp://%s/' % server.ip

  def setSuspiciousFiles(self, suspicousFiles:dict = []):
    self.suspicousFiles = suspicousFiles

  def setSuspiciousFileExtensions(self, suspiciousFileExtensions:dict = []):
    self.suspiciousFileExtensions = suspiciousFileExtensions

  def setDownloadToCheck(self, downloadToCheck:bool = False):
    self.downloadToCheck = downloadToCheck

  def crawl(self):
    self.scan = Scan(
      server = self.server,
      time = datetime.datetime.now()
    )
    # time = DateTimeField()
    # completed = BooleanField()
    self.scan.save()
    self.createList()

  def createList(self, path:str = "/"):
    self.currentFileList = []
    try:
      print("Switch to directory %s" % path)
      self.ftp.dir(path, self.checkDirectory)
    except (ftplib.error_temp, EOFError) as e:
      print("error switching to %s" % path)
      print(str(e))
    nextDirectories = []
    for currentFile in self.currentFileList:
      if currentFile['type'] is 'directory':
        nextDirectories.append("%s%s/" % (path, currentFile['name']))
      else:
        filePath = "%s%s" % (path, currentFile['name'])
        self.fileList.append(filePath)
        
        fileModel = File(
          scan = self.scan,
          remotePath = filePath,
          time = datetime.datetime.now()
        ) 
        fileModel.save()



        if self.downloadToCheck is True:
          print("Downloading file %s  to /tmp/ftp-file-to-check" % filePath)
          try:
            self.ftp.retrbinary('RETR %s' % filePath, open(self.tmpPath, 'wb').write)
            scanner = Clamscan('/tmp/ftp-file-to-check')
            scanner.scan()
            if scanner.getIsVirus():
              destinationPath = "downloadedFiles/ftp-%s%s" % (self.server.ip, path)
              if not os.path.exists(destinationPath):
                os.makedirs(destinationPath)
              
              shutil.move('/tmp/ftp-file-to-check', "%s%s" % (destinationPath, currentFile['name']))
              fileModel.localPath = "%s%s" % (destinationPath, currentFile['name'])
              fileModel.save()

              virus = Virus(
                file = fileModel,
                definition = scanner.getVirusDefinition()
              )
              virus.save()

              #strings = Strings("%s%s" % (destinationPath, currentFile['name']))
              #for line in strings.get():
              #  string = String(
              #    virus = virus,
              #    content = line
              #  )
              #  string.save()
                
              self.infectedFileList.append({
                'path': filePath,
                'url': '%s%s' % (self.serverUrl, filePath)
              })

          except ftplib.error_perm:
            print("no permission to read %s" % filePath)
          
    
    for nextDirectory in nextDirectories:
      self.createList(nextDirectory)

    # reset nextDirectories
    self.currentFileList = []
    nextDirectories = []

  def getFileList(self):
    return self.fileList

  def getInfectedFiles(self):
    return self.infectedFileList

  def checkDirectory(self, ftpDir):
    lines = ftpDir.split("\n")
    for line in lines:
      lineParts = line.split()
      fileObject = {
        'name': lineParts.pop(),
        'type': None
      }
      if line.startswith("d"):
        fileObject['type'] = 'directory'
      else:
        fileObject['type'] = 'file'

      self.currentFileList.append(fileObject)

  def close(self):
    self.currentFileList = []
    self.ftp.quit()
    self.ftp.close()
