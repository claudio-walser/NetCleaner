# NetCleaner
try to clean up open devices

# Installation
sudo python3 setup.py install

# Usage
Create the database 
```
nc-create-database 
```

Index some servers 
```
nc-memorize --type ftp --from shodan --file exports/shodan-export.json 
```

Try to fingerprint (as far as possible)
```
nc-server --fingerprint 
```

Run the scanner and store infected files
```
nc-scanner --check-by-download 
```

If you want to delete infected file on the remote host, run the same command with --cleanup
Take care of your local law, delete files on devices dont belong to you could be illegal. Even if you doing it for good. 
```
nc-scanner --check-by-download --cleanup
```