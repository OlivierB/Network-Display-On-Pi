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



Atomik::add('app.routes', array(
   'modules/editor/:module' => array(
       'action' => 'module_editor',
       'module' => ''
   )
));

Atomik::add('app.routes', array(
   'widget/editor/:widget' => array(
       'action' => 'widget_editor',
       'widget' =>''
   )
));