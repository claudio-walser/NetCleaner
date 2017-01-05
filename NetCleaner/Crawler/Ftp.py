from ftplib import FTP
import sys

class Ftp(object):

  ftp = None
  serverUrl = None
  tmpPath = '/tmp/ftp-file-to-check'

  suspicousFiles = []
  suspiciousFileExtensions = []
  downloadToCheck = False

  currentFileList = []
  fileList = []
  infectedFileList = []

  def __init__(self, ip:str):
    self.ftp = FTP(ip)
    if not self.ftp.login():
      raise Exception("Not able to connect to given FTP Server %s" % ip)

    self.serverUrl = 'ftp://%s/' % ip

  def setSuspiciousFiles(self, suspicousFiles:dict = []):
    self.suspicousFiles = suspicousFiles

  def setSuspiciousFileExtensions(self, suspiciousFileExtensions:dict = []):
    self.suspiciousFileExtensions = suspiciousFileExtensions

  def setDownloadToCheck(self, downloadToCheck:bool = False):
    self.downloadToCheck = downloadToCheck

  def crawl(self):
    self.createList()

  def createList(self, path:str = "/"):
    self.currentFileList = []
    self.ftp.dir(path, self.checkDirectory)

    nextDirectories = []
    for currentFile in self.currentFileList:
      if currentFile['type'] is 'directory':
        nextDirectories.append("%s%s/" % (path, currentFile['name']))
      else:
        filePath = "%s%s" % (path, currentFile['name'])
        self.fileList.append(filePath)
        
        if self.downloadToCheck is True:
          fileParts = currentFile['name'].split('.')
          fileExtension = fileParts.pop()
          if fileExtension in self.suspiciousFileExtensions:
            print("Downloading file %s  to /tmp/ftp-file-to-check" % filePath)
            self.ftp.retrbinary('RETR %s' % filePath, open(self.tmpPath, 'wb').write)
            # check for viruses with clamav and if positive, store filename into suspiciousFileList for simpler checks
            sys.exit(0)
        else:
          if currentFile['name'] in self.suspicousFiles:
            self.infectedFileList.append({
              'path': filePath,
              'url': '%s%s' % (self.serverUrl, filePath)
            })
    
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
