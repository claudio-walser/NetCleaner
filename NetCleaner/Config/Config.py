from NetCleaner.Config.Parser import Parser
from pprint import pprint

class Config(Parser):

  filename = 'config.yaml'

  def __init__(self):
    self.load()
    pprint(self.yaml)