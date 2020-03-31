<?php
require 'config.php';

$now_time = time();

$remaining_time = $min_time_span - ($now_time - $game_time);

$data = [
    'game_rounds' => $game_rounds,
    'remaining_time' => $remaining_time
];
header('Content-type:application/json;charset=utf-8');
echo json_encode($data);