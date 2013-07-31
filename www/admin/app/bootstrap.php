<?php

require_once "../app/NDOP.php";
NDOP::init('../ndop.conf.ini');
if(isset(NDOP::$app['db'])){
	Atomik::set('database', NDOP::$app['db']);
}
