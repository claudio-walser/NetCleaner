from ftplib import FTP
import hashlib


# 214-The following commands are recognized.
#  ABOR ACCT ALLO APPE CDUP CWD  DELE EPRT EPSV FEAT HELP LIST MDTM MKD
#  MODE NLST NOOP OPTS PASS PASV PORT PWD  QUIT REIN REST RETR RMD  RNFR
#  RNTO SITE SIZE SMNT STAT STOR STOU STRU SYST TYPE USER XCUP XCWD XMKD
#  XPWD XRMD

class Ftp(object):

  ftp = None
  ip = None

  def __init__(self, ip:str):
    self.ftp = FTP(ip)
    if not self.ftp.login():
      raise Exception("Not able to connect to given FTP Server %s" % ip)
    self.ip = ip


  def fingerprint(self):
    print(self.ip)
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