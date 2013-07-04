<?php
require_once '../ndop.conf.php';


NDOP::$app = parse_ini_file('../ndop.conf.ini');

if( isset(NDOP::$app['database_address']) && 
    isset(NDOP::$app['database_login']) && 
    isset(NDOP::$app['database_password']) )
{
    try {
        $dbh = new PDO("mysql:host=".NDOP::$app['database_address'].";dbname=NDOP_GUI", NDOP::$app['database_login'], NDOP::$app['database_password']);
        Atomik::set('database', $dbh);
    }
    catch(PDOException $e)
    {
        // echo $e->getMessage();
    }
}