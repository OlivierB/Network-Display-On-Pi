<?php

function header_display($title){


	echo '
	<h1>
	<a href="#" class="slidesjs-previous slidesjs-navigation">
	<i class="icon-chevron-left"></i>
	</a>
	'.$title.'
	<a href="#" class="slidesjs-next slidesjs-navigation">
	<i class="icon-chevron-right"></i>
	</a>
	</h1>';
}




function display_module($name, $id) {
	header_display($name);

	$select_widgets = "SELECT `id_widget`, `id_widget_parameter_set`, x, y, width, height FROM `module_composition_widget` WHERE `id_module` = :id_module ORDER BY y, x;";
	$prep_select_widgets = NDOP::$app['db']->prepare($select_widgets);
	$prep_select_widgets->execute(array(
		'id_module' => $id
		));

	$widgets = $prep_select_widgets->fetchAll(PDO::FETCH_ASSOC);

	$current_x = 0;
	$current_y = 0;

	echo "<div class='slide-div'>";
	echo 	"<div class='row-fluid'>";

	foreach ($widgets as $index => $widget) {

		// if the widget is set to be on the second line then every following 
        // widgets willl be on the second line
        if ($widget['y'] == 1 && $current_y == 0) {
            echo "</div><div class='row-fluid'>";
            $current_x = 0;
            $current_y = 1;
        }

        
        // if there is a blank before the widget, we fill it with nothing
        if ($widget['x'] > $current_x) {
            $diff = $widget['x'] - $current_x;
            display_widget(-1, -1, $diff, $widget['height']);
        }
        
		display_widget($widget['id_widget'], $widget['id_widget_parameter_set'], $widget['width'], $widget['height']);
		$current_x += $widget['width'];
	}
	echo 	"</div>";
	echo "</div>";
}

function display_widget($id_widget, $id_widget_parameter_set, $width, $height) {
	$select_widget = "SELECT `folder_name` FROM `widget` WHERE `widget`.`id` = :id_widget;";
	$prep_select_widget = NDOP::$app['db']->prepare($select_widget);

	$prep_select_widget->execute(array(
		'id_widget' => $id_widget
		));

	$widget = $prep_select_widget->fetchAll(PDO::FETCH_ASSOC);

	if($height == 2) {
		$class_height = "height-full";
	}else{
		$class_height = "height-half";
	}
	echo "<div class='span".$width." ".$class_height."' >";
	if($id_widget > 0){
		include "./widgets/".$widget[0]['folder_name']."/content.php";
	}else{

	}
	
	echo "</div>";
}