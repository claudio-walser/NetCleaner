import subprocess
import os

from pprint import pprint

class Clamscan (object):

    filename  = None
    isScanned = False
    isVirus = False
    virusDefinition = None

    def __init__(self, filename:str):
        if not os.path.isfile(filename):
            raise Exception("File %s not found, therefore not able to scan" % (filename))
        self.filename = filename

    def scan(self):
        command = "clamscan %s" % (self.filename)

        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output, err = process.communicate()
        self.isScanned = True            

        output = output.decode("utf-8").strip()
        lines = output.split("\n")
        firstLine = lines[0]
        definition = firstLine.split()
        pprint(definition)
        if definition.pop() == 'FOUND':
            self.isVirus = True
            self.virusDefinition = definition.pop()

    def getIsVirus(self):
        if not self.isScanned:
            raise Exception("Scan the file first")
        return self.isVirus

    def getVirusDefinition(self):
        if not self.isScanned:
            raise Exception("Scan the file first")
        return self.virusDefinition