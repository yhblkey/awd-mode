# coding=utf-8
'''
AWD config

container_dir    web应用源码目录       web_container
min_time_span    每一轮的时间周期       300（单位 秒）
score_init       初试分数              10000
score_every      每次攻击（得/失）分    100
port             web应用容器内部运行端口 80
image            基础镜像名称           web_14.04
teamsfile        队伍信息csv文件
'''

class Config(object):
    container_dir = 'web_container'
    min_time_span = 300
    score_init = 100000
    score_every = 100
    port = 80
    challenge_image = 'yhbl/awd_v3'
    flagserver_image = 'yhbl/awd_v3'
    network = 'mynetwork'
    serverport_start = 8800
    sshport_strat = 2200
    teamsfile = './test.csv'





