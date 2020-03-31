<?php
/**
 * Created by PhpStorm.
 * User: yhbl
 * Date: 18-11-12
 * Time: 下午3:47
 */

require 'config.php';

$str = file_get_contents("/tmp/score.txt");
$str_array  = explode('|',$str);
$map = array();
for($i = 1;$i<= count($str_array);$i++){
    $map[$user_list[$i-1]] = $str_array[$i-1];
}
//echo "<tr><th scope=\"row\" class=\"text-center\">1</th><td>Phillip</td><td>152</td></tr>";
arsort($map);
$place = 1;
foreach ($map as $k => $v){
    echo "<tr><th scope=\"row\" class=\"text-center\">{$place}</th><td>{$k}</td><td>{$v}</td></tr>".PHP_EOL;
    $place++;
}

