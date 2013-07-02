<?php

Atomik::set(array(
    'atomik' =>array(
        'url_rewriting' => true
    ),
    'plugins' => array(
        'Errors' => array(
            'catch_errors' => true
        ),
        'Session',
        'Flash',
    ),

    'app.layout' => '_layout',

    
));

Atomik::set('app.routes', array(
   'hello/:year/:month' => array(
       'action' => 'hello',
       'month' => 'all'
   )
));


require_once '../ndop.conf.php';
if( NDOP::$app['database_address'] != null && 
    NDOP::$app['database_login'] != null && 
    NDOP::$app['database_password'] != null)
{
    Atomik::set('plugins.Db', array(
        'dsn' => 'mysql:host='.NDOP::$app['database_address'].';dbname=NDOP',
        'username' => NDOP::$app['database_login'],
        'password' => NDOP::$app['database_password']
        )
    );
}