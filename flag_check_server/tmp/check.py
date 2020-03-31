#!/usr/bin/env python
# -*- coding:utf8 -*-
'''

'''
import hashlib
import base64

sleep_time  = 120
debug = True
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

import time
import httplib
import urllib2
import ssl 

my_time = 'AAAA' 
__doc__ = 'http(method,host,port,url,data,headers)'
flag_server = '172.17.0.1'
key = '7eba1d9399712ded28028d8e20462437'
hosts = open('host.lists','r').readlines()
user_id = [host.split(':')[0] for host in hosts]
hosts = [host.split(':')[1] for host in hosts]
port = 80

def http(method,host,port,url,data,headers):
    con=httplib.HTTPConnection(host,port,timeout=2)
    if method=='post' or method=='POST':
        headers['Content-Length']=len(data)
        headers['Content-Type']='application/x-www-form-urlencoded'  
        con.request("POST",url,data,headers=headers)
    else:
        headers['Content-Length'] = 0    
        con.request("GET",url,headers=headers)
    res = con.getresponse()
    if res.getheader('set-cookie'):
        #headers['Cookie'] = res.getheader('set-cookie')
        pass
    if res.getheader('Location'):
        print "Your 302 direct is: "+res.getheader('Location')
    a = res.read()
    con.close()
    return a


def https(method,host,port,url,data,headers):
    url = 'https://' + host + ":" + str(port) + url
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    return response.read()

def get_score():
    res = http('get',flag_server,8080,'/score.php?key=%s'%key,'',headers)
    print res
    user_scores = res.split('|')
    print "******************************************************************"
    res = ''
    i = 0
    for user_score in user_scores:
	res += (user_id[i] + ":" + user_score).ljust(20,'*')
	i += 1
    print res
    print "******************************************************************" 
    return user_scores

def write_score(scores):
    scores = '|'.join(scores)
    res = http('get',flag_server,8080,'/score.php?key=%s&write=1&score=%s'%(key,scores),'',headers)
    if res == "success":
	return True
    else:   
	print res
	raise ValueError

class check():
    def __init__(self):
	print "checking host: "+host

    def index_check(self):
	res = http('get',host,port,'/web/?time=%s'%str(my_time),'',headers)
	if '网校课程' in res:
	    return True
	if debug:
	    print "[fail!] index_fail"
	return False
	

    def test_check(self):
	res = http('get',host,port,'/flag.py','',headers)
	if '403 Forbidden' in res:
	    return True
	if debug:
	    print "[fail!] test_fail"
	return False


    def test_check_2(self):
	headers['Cookie'] = ''
	data = 'key=1'
	res = http('get',host,port,'/web/register?goto=/web/teacher',data,headers)
	if '邮箱地址' in res:
	    return True
	if debug:
	    print "[fail!] test_2_fail"
	return False
	

    def login_check(self):
	headers['Cookie'] = 'PHPSESSID=ujg0tpds1u9d23b969f2duj5c7;'
	headers['X-Requested-With'] = 'XMLHttpRequest'
	res = http('post',host,port,'/admin/login/index.html','username=admin&password=admin&verify=7480',headers)
	if '"status":1' in res:
	    return True
	if debug:
	    print "[fail!] login_fail"
	return False

    def admin_check(self):
	data = 'eval(666)'
	headers['Cookie'] = 'PHPSESSID=ujg0tpds1u9d23b969f2duj5c7;'
    	res = http('get',host,port,'/admin/tools/database?type=export',data,headers)
	tmp = http('get',host,port,'/admin/login/loginout.html','',headers)
	if 'qq3479015851_article_type' in res:
	    return True
	if debug:
	    print "[fail!] admin_fail"
	return False
    

def server_check():
    try:
	a = check()
	# if not a.index_check():
	#     return False
	if not a.test_check():
	    return False
	# if not a.test_check_2():
	#     return False	
	return True
    except Exception,e:
	print e
	return False


game_round = 0
while True:
    
    scores = get_score()
    scores = []
    print "--------------------------- round %d -------------------------------"%game_round
    for host in hosts:
	print "---------------------------------------------------------------"
	host = host[:-1]
	if server_check():
	    print "Host: "+host+" seems ok"
	    scores.append("10")
        else:
	    print "Host: "+host+" seems down"
	    scores.append("-40")
    game_round += 1
    write_score(scores)
    time.sleep(sleep_time)
