import os
from NetCleaner.Config.Parser import Parser

class Input(Parser):

  filename = 'input.yaml'

  def __init__(self):
    self.load()


  def get(self, sourceType = None):
    if self.yaml['sources'] and self.yaml['sources'][sourceType]:
      return self.yaml['sources'][sourceType]

    return None
