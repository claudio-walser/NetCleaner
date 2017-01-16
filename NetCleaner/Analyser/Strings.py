import subprocess
import os

class Strings (object):

    filename  = None
    isScanned = False
    isVirus = False
    virusDefinition = None

    def __init__(self, filename:str):
        if not os.path.isfile(filename):
            raise Exception("File %s not found, therefore not able to get strings" % (filename))
        self.filename = filename

    def get(self):
        command = "strings %s" % (self.filename)

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
        return lines