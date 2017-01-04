from ftplib import FTP

from pprint import pprint

class Ftp(object):

  ftp = None

  def __init__(self, ip:str):
    self.ftp = FTP(ip)
    if not self.ftp.login():
      raise Exception("Not able to connect to given FTP Server %s" % ip)

    pprint(self.ftp.dir())


