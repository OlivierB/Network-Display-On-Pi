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
   'modules/:folder' => array(
       'action' => 'modules',
   )
));