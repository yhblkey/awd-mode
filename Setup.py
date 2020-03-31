# coding=utf-8
import time
import os
import hashlib
import csv
from Config import Config

#修改添加config类，集中配置ß

def copy_dir(src, dst):
    os.system('cp -r %s %s' % (src, dst))


def generate_passwd(teamnum):
    salt = 'yhblsqt'
    passwd = hashlib.md5(salt + str(time.time()) + str(teamnum)).hexdigest()
    open('passwd.txt', 'a').write('team' + str(teamnum) + ':ctf:' + passwd + "\n")
    return passwd


def generate_container_setup_sh(passwd):
    content = '''#!/bin/sh
cd /var/www/html
service ssh start
a2enmod rewrite
service apache2 restart
service mysql start
useradd ctf
echo ctf:%s | chpasswd
sleep 2
chmod +x extra.sh
if [ -x "extra.sh" ]; then 
./extra.sh
fi
/bin/bash
''' % passwd
    return content

def generate_container_docker_sh(teamnum, port, image, network, serverport_start, sshport_strat):
    content = '''#!/bin/sh
docker run -p %d:%d  -p %d:22 -v `pwd`:/var/www/html -d  --network %s --ip 172.60.0.%d  --name team%d -ti %s /var/www/html/setup.sh 
''' % (serverport_start + teamnum, port, sshport_strat + teamnum, network,1+teamnum, teamnum, image)
    return content


def generate_host_list(teamsfile):
    fp = open('./flag_check_server/tmp/host_list.txt', 'w')
    team_list = csv.reader(open(teamsfile, 'r'))
    next(team_list)
    sum = 0
    for row in team_list:
        # print row
        sum = sum + 1
        fp.write('team%d:%s:172.60.0.%d\n' % (int(row[0]), row[1], int(row[0]) + 1))
    fp.close()
    return sum

def generate_flag_setup_sh(teamsum, score_init, min_time_span):
    content = '''#!/bin/sh
cd /var/www/html
pip install requests
service apache2 stop
service apache2 start
chmod -R 777 CTFd_files
python /tmp/new.py %d %d
chmod 777 /tmp/time.txt
chmod 777 /tmp/score.txt
chmod 777 /tmp/result.txt
python /tmp/gen_flag.py %d &
/bin/bash
''' % (teamsum, score_init, min_time_span)
    return  content

def generate_flag_docker_sh(network, teamsum, image):
    content = '''#!/bin/sh
docker run -v `cd ./html;pwd`:/var/www/html -v `cd ./tmp;pwd`:/tmp -p 8080:80 -d  --net %s --ip 172.60.0.%d --name flag_check_server -ti %s /tmp/setup.sh
''' % (network, teamsum+2, image)
    return content

def generate_flag_config(teamsum, min_time_span, score_every):
    content = '''<?php
$team_number = %d;
$user_list = [];
$token_list = array();
$ip_list = array();
$score_every = %d;

$contents = explode("\n", file_get_contents('/tmp/host_list.txt'));
$i = 0;
foreach ($contents as $content){
    $tmp = explode(':', $content);
    array_push($user_list, $tmp[1]);
    $token_list[$tmp[0]] = $i;
    $ip_list[$tmp[2]] = $i;
    $i = $i + 1;
}

$key = '7eba1d9399712ded28028d8e20462437';       //md5('AWD_CUST_2019_yanzhiqiang')
$time_file = '/tmp/time.txt';

$min_time_span = %d;
$record = '/tmp/score.txt';

$gameinfo = explode('|', file_get_contents('/tmp/gametime.txt'));
$game_rounds = $gameinfo[0];
$game_time = $gameinfo[1];
    ''' % (teamsum, score_every, min_time_span)
    return content


# python setup.py web_container/ 60*5
def setup():

    container_dir = Config.container_dir         #WebContainterName
    min_time_span = Config.min_time_span    #MinTimeSpen
    score_init = Config.score_init       #
    score_every = Config.score_every
    teamsum = generate_host_list(Config.teamsfile)
    port = Config.port
    challenge_image = Config.challenge_image
    flagserver_image = Config.flagserver_image
    network = Config.network
    serverport_start = Config.serverport_start
    sshport_strat = Config.sshport_strat

    open('./flag_check_server/tmp/setup.sh', 'w').write(generate_flag_setup_sh(teamsum, score_init, min_time_span))
    open('./flag_check_server/docker.sh', 'w').write(generate_flag_docker_sh(network, teamsum, flagserver_image))
    open('./flag_check_server/html/config.php', 'w').write(generate_flag_config(teamsum, min_time_span, score_every))

    for i in range(teamsum):
        password = generate_passwd(i + 1)
        team_dir = 'team' + str(i + 1)
        copy_dir(container_dir, team_dir)
        print '[*] copy %s' % team_dir

        os.system('chmod -R 777 %s' % team_dir)
        print '[*] chmod all '

        open(team_dir + '/setup.sh', 'w').write(generate_container_setup_sh(password))
        print '[*] write setup.sh %s' % team_dir

        open(team_dir + '/docker.sh', 'w').write(generate_container_docker_sh(i + 1, port, challenge_image, network, serverport_start, sshport_strat))
        print '[*] write docker.sh %s' % team_dir

        os.system('chmod 700 %s/setup.sh %s/docker.sh ' % (team_dir, team_dir))
        print '[*] chmod setup.sh & docker.sh %s' % team_dir
    return teamsum, container_dir

def start_FlagServer():
    os.system('chmod +x ./flag_check_server/docker.sh')
    os.system('chmod +x ./flag_check_server/tmp/setup.sh')
    os.system('cd ./flag_check_server/ && sh docker.sh')
    print '[*] start docker flag_server'

def start_team(teamno):
    team_dir = 'team' + str(teamno)
    os.system('cd ./%s/ && sh docker.sh' % (team_dir))
    print '[*] start docker %s' % team_dir

def start():
   # os.system('docker network create --subnet 172.60.0.0/24 --gateway 172.60.0.1  --internal mynetwork')
    print 'success generate network!!!'
    teamsum, container_dir = setup()
    for i in range(teamsum):
        start_team(i+1)
    start_FlagServer()



if __name__ == '__main__':
    start()
