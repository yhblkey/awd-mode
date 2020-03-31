#!/usr/bin/env python

import requests
import hashlib
import sys
import time
if len(sys.argv) == 2:
	time_span = int(sys.argv[1])
record_path = '/tmp/teams_flag'  # /tmp/teams_flag


hosts = open('/tmp/host_list.txt').readlines()

host_list = {}


for host in hosts:
	teamno,teamname,host_ip = host.strip().split(':')
	host_list[teamno] = host_ip

i = 1
while True:
	open(record_path,'w').write('')
	for teamno in host_list:
		flag = hashlib.md5('cust_awd@2019' +  host_list[teamno] +  str(int(time.time())/time_span)).hexdigest()
		open(record_path,'a').write(host_list[teamno] + ':' + flag + "\n" )
		print '[*] flag for %s update to %s!' % (host_list[teamno],flag)
	open('/tmp/gametime.txt','w').write(str(i) + '|' + str(int(time.time())))
	i = i+1
	time.sleep(time_span)
