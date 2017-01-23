import subprocess

class File (object):

    filename  = None
    isScanned = False
    definition = None

    def __init__(self, filename:str):
        if not os.path.isfile(filename):
            raise Exception("File %s not found, therefore not able to get header" % (filename))
        self.filename = filename

    def scan(self):
        command = "file %s" % (self.filename)

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
        parts = output.split(": ")
        self.definition = parts[1]

    def getDefinition(self):
        if not self.isScanned:
            raise Exception("Scan the file first")
        return self.definition