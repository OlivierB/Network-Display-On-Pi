<?php

require_once "../pages/NDOP.php";
NDOP::init('../ndop.conf.ini');

Atomik::set('database', NDOP::$app['db']);
