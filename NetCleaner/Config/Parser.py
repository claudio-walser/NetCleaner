import yaml
import os

class Parser:

    filename = None
    yaml = {}

    def load(self):
        # raise exception if no .gitcd in current working dir
        if not os.path.isfile(self.filename):
            raise Exception("Config File %s not found" % self.filename)

        # open and load .gitcd
        with open(self.filename, 'r') as stream:
            self.yaml = yaml.safe_load(stream)
