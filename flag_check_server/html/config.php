<?php
$team_number = 3;
$user_list = [];
$token_list = array();
$ip_list = array();
$score_every = 100;

$contents = explode("
", file_get_contents('/tmp/host_list.txt'));
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

$min_time_span = 300;
$record = '/tmp/score.txt';

$gameinfo = explode('|', file_get_contents('/tmp/gametime.txt'));
$game_rounds = $gameinfo[0];
$game_time = $gameinfo[1];
    