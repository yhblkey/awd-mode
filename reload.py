# coding=utf-8
import sys
import os
from Config import Config

# 本模块用于重新启动服务   使用原有的用户名 密码 内网IP 外网映射端口 以及源码来重新创建容器环境

def copy_dir(src, dst):
    os.system('cp -r %s %s' % (src, dst))

def container_reboot(teamnum):
    # 删除原容器
    team_name = ('team'+str(teamnum))
    os.system('docker rm -f %s' % team_name)
    os.system('rm -rf %s ' % team_name)
    # 获取原容器的ssh密码
    passwd_old = ''
    password_list = open('passwd.txt', 'r').readlines()
    for passwd in password_list :
        tmp = passwd.replace('\n', '').split(':')
        if tmp[0] == team_name:
            passwd_old = tmp[2]
    if passwd_old == '':
        print 'error：未找到容器ssh连接密码'
        exit()
    # print passwd_old
    # 构建重启容器的初始化脚本 setup.sh
    setup_content = '''#!/bin/sh
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
''' % passwd_old
    # 构建重启容器的docker脚本 docker.sh
    docker_content = '''#!/bin/sh
docker run -p %d:%d  -p %d:22 -v `pwd`:/var/www/html -d  --net mynetwork --ip 172.60.0.%d  --name team%d -ti %s /var/www/html/setup.sh 
''' % (8800 + teamnum, Config.port, 2200 + teamnum, 1 + teamnum, teamnum, Config.challenge_image)
    # 启动容器
    copy_dir(Config.container_dir, team_name)
    print '[*] copy %s' % team_name

    os.system('chmod -R 777  %s/' % team_name)
    print '[*] chmod all '

    open(team_name + '/setup.sh', 'w').write(setup_content)
    print '[*] write setup.sh %s' % team_name

    open(team_name + '/docker.sh', 'w').write(docker_content)
    print '[*] write docker.sh %s' % team_name

    os.system('chmod 700 %s/setup.sh %s/docker.sh ' % (team_name, team_name))
    print '[*] chmod setup.sh & docker.sh %s' % team_name

    os.system('cd ./%s/ && sh docker.sh' % team_name)
    print '[*] start docker %s' % team_name


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if str.isdigit(sys.argv[1]):
            container_reboot(int(sys.argv[1]))
        else:
            print '[*] error: 参数必须为队伍编号数字形式'
            exit()
    else:
        print '[*] error: 必须携带一个参数值'
