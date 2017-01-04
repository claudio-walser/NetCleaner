# NetCleaner
try to clean up open devices


# Class Structure
Config Parser
Input Parser
Suspicious Files / FileTypes

Crawler (able to download files and overwrite files with same bytesize)
FTP
Iomega

Downloader (maybe done in crawler)

Analyser (classifies each file and stores information about it)
Clamscan
strings
file




# DB Scheme

File
- id
- name
- header (comes from Analyser/File)
- remotePath
- localPath
- timestamp
- virusDetected (comes from Analyser/Clamscan

String (information comes from Analyser/Strings
-id
-fileId
-string