#!/bin/sh
cd /var/www/html
pip install requests
service apache2 stop
service apache2 start
chmod -R 777 CTFd_files
python /tmp/new.py 3 100000
chmod 777 /tmp/time.txt
chmod 777 /tmp/score.txt
chmod 777 /tmp/result.txt
python /tmp/gen_flag.py 300 &
/bin/bash
