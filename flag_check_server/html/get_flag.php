<?php
//获取来源队伍的IP 根据IP发放当前被攻陷主机的flag 测试是flag文件地址为 ./teams_flag  真是环境下为/tmp/teams_flag

require 'config.php';

$victim_ip = $_SERVER['REMOTE_ADDR'];

$flag_list = array();

$contents = explode("\n", file_get_contents('/tmp/teams_flag'));


foreach ($contents as $content){
    $tmp = explode(':', $content);
    if ($tmp[0] === $victim_ip){
        $victim_id = $ip_list[$victim_ip];
        die('success ！！！ '.$user_list[$victim_id].'  :   '.$tmp[1]);
    }
}
die(' The IP you captured is not in the IP range of the match ！！！！');