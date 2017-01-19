from ftplib import FTP
import socket
import hashlib


class Ftp(object):

  ftp = None
  ip = None
  reachable = False
  anonymousLogin = False

  def __init__(self, ip:str):
    self.ip = ip

  def connect(self):
    self.ftp = FTP(self.ip)
    self.reachable = True
    self.ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
    self.ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)

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

  def getFiles(self, path:str):
    return []

  def getDirectories(self, path:str):
    return []

  def checkDirOutput(self, output):
    lines = output.split("\n")
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
    if self.ftp is None:
      return
    self.ftp.quit()
    self.ftp.close()
