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

## Configuration
Configuration file is in /etc/netCleaner/config.yaml

## Possible usage
nc-memorize --type ftp --shodanFile shodan.json
nc-server fingerprint 
nc-scanner scan --rescan --check-by-download --cleanup