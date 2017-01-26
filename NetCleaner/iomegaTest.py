#!/usr/bin/env python3
import requests
from pprint import pprint
from lxml import html
from pprint import pprint
import urllib

url = 'https://178.248.207.118/cp/FolderContents?v=2.3'



# get root nodes
url = 'https://178.248.207.118/cp/Shares?v=2.3&user=&protocol=webaccess'
r = requests.get(url, verify=False)
rootNodes = []
for item in r.json()['items']:
  if item['access'] == 'readwrite':
    rootNodes.append(item['name'])

pprint(rootNodes)

for rootNode in rootNodes:
  testNode = {
    'name': rootNode
  }
  print(rootNode)
  parsed = urllib.parse.urlencode(testNode)
  folderName = parsed.replace('name=', '')
  print("now do the payload")
  payload = {
    'path': folderName,
    'sortby': 'name',
    'max': 10000,
    'start': 0,
    'contenttype': 'all'
  }
  r = requests.post(url, data=payload, verify=False)
  pprint(r.json())

# get folder contents

# path:forum%2F.Thumbnails
# sortby:name
# max:20
# start:0
# contenttype:all
