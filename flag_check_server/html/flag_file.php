<?php


require 'config.php';

$now_time = time();
$flag_file = '/tmp/teams_flag'; // /tmp/team_flag

function check_time($attack_uid, $victim_uid)
{
    global $time_file;
    global $min_time_span;
    global $now_time;
    global $team_number;
    global $game_time;
    $old_times = explode('|', file_get_contents($time_file));
    $id = $attack_uid * $team_number + $victim_uid;

    if ($old_times[$id] == '0'){
        return True;
    }elseif ($old_times[$id] >= $game_time and $old_times[$id] <= $game_time + $min_time_span){
        die("error: submit too quick " . ($game_time + $min_time_span - $now_time) . " seconds left");
    }else{
        return True;
    }

//    if ($now_time - $old_times[$id] < $min_time_span) {
//        die("error: submit too quick " . ($min_time_span + $old_times[$id] - $now_time) . " seconds left");
//    } else {
//        return True;
//    }


}

function update_time($attack_uid, $victim_uid)
{
    global $time_file;
    global $now_time;
    global $team_number;
    $old_times = explode('|', file_get_contents($time_file));
    $id = $attack_uid * $team_number + $victim_uid;
    $old_times[$id] = $now_time;
    file_put_contents($time_file, implode('|', $old_times));
}

function match_flag($flag, $flag_file)
{
    $flags = explode("\n", file_get_contents($flag_file));
    foreach ($flags as $real_flag) {
        $tmp = explode(":", $real_flag);
        $host = $tmp[0];
        $real_flag = $tmp[1];
        if ($flag == $real_flag) {
            return $host;
        }
    }
    return '';

}

if (isset($_REQUEST['token']) && isset($_REQUEST['flag'])) {
    $token = $_REQUEST['token'];  //team1
    $flag = $_REQUEST['flag'];    //32位
    if (!array_key_exists($token, $token_list)) {  //判断是否存在team1
        die('error: no such token ！！');
    }
    $ip = match_flag($flag, $flag_file);          //找到flag文件中对应队伍的IP
    if (!$ip) {
        die('error: no such flag ！！');
    }
    $attack_id = $token_list[$token];            //找到攻击队伍的队伍ID
    $victim_id = $ip_list[$ip];                  //找到被攻击队伍的队伍ID
    if ($attack_id === $victim_id) {             //不能自己攻击自己
        die('error: do not attack yourself ！！');
    }
    for ($i = 0; $i < $team_number; $i++) {
        $scores[$i] = 0;
    }
    $scores[$attack_id] = $score_every;
    $scores[$victim_id] = 0 - $score_every;
    check_time($attack_id, $victim_id);
    $score = implode('|', $scores);
    file_put_contents('/tmp/result.txt', $user_list[$attack_id] . ' => ' . $user_list[$victim_id] . "\n", FILE_APPEND);
    $cmd = 'curl "127.0.0.1/score.php?key=' . $key . '&write=1&score=' . $score . '"';
    system($cmd);
    update_time($attack_id, $victim_id);

} else {
    die("error: empty token or empty target");
}
