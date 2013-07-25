<?php

require_once "../pages/NDOP.php";
NDOP::init('../ndop.conf.ini');
if(isset(NDOP::$app['db'])){
	Atomik::set('database', NDOP::$app['db']);
}
