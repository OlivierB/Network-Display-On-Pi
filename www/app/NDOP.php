<?php
// require "common.php";

Class NDOP {
	public static $app;
	public static $nb_widget;

	public static function init($path_ini_file) {
		NDOP::$nb_widget = 0;
		
		NDOP::$app = @parse_ini_file($path_ini_file);

		if( isset(NDOP::$app['database_address']) && 
			isset(NDOP::$app['database_port']) && 
			isset(NDOP::$app['database_login']) &&
			isset(NDOP::$app['database_password']) && 
			isset(NDOP::$app['database_name']) )
		{
			try {
				NDOP::$app['db'] = new PDO("mysql:host=".NDOP::$app['database_address'].";port=".NDOP::$app['database_port'].";dbname=".NDOP::$app['database_name'], NDOP::$app['database_login'], NDOP::$app['database_password'],array(PDO::ATTR_TIMEOUT => "1"));
				NDOP::$app['db']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

			}
			catch(PDOException $e)
			{
                // echo $e->getMessage();
			}
		}
	}

	public static function display_modules(){
		$module_exist = false;

		if(isset(NDOP::$app['db']) && NDOP::$app['db']){
			
			$sql = "SELECT `module`.`name`, `module`.`id` FROM `layout` JOIN `module` ON `layout`.`id_module` = `module`.`id` GROUP BY `layout`.`page`";
			$results = NDOP::$app['db']->query($sql);
			$pages = $results->fetchAll(PDO::FETCH_ASSOC);

			foreach ($pages as $key => $value) {
				$module_exist = true;
				echo "<div>";
				NDOP::display_module($value['name'], $value['id']);
				echo "</div>";
			}

		}
		if(!$module_exist){
			echo "<div class='slide-div'>";
			echo 	"<div class='row-fluid'>";
			
			include "static/introduction.php";
			echo 	"</div>";
			echo "</div>";

		}
	}

	public static function display_module($name, $id) {
		NDOP::header_display($name);

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
        // widgets will be on the second line
			if ($widget['y'] == 1 && $current_y == 0) {
        	// if ther is no widget on the first line we add a blank one to set a height to the first line
				if($current_x == 0) {
					NDOP::display_widget(-1, -1, 1, 1);
				}


				echo "</div><div class='row-fluid'>";
				$current_x = 0;
				$current_y = 1;
			}


        // if there is a blank before the widget, we fill it with nothing
			if ($widget['x'] > $current_x) {
				$diff = $widget['x'] - $current_x;
				NDOP::display_widget(-1, -1, $diff, $widget['height']);
			}

			NDOP::display_widget($widget['id_widget'], $widget['id_widget_parameter_set'], $widget['width'], $widget['height']);
			$current_x += $widget['width'];
		}
		echo 	"</div>";
		echo "</div>";
	}

	public static function display_widget($id_widget, $id_widget_parameter_set, $width, $height) {
		$select_widget = "SELECT `folder_name` FROM `widget` WHERE `widget`.`id` = :id_widget;";
		$prep_select_widget = NDOP::$app['db']->prepare($select_widget);

		$select_params = "SELECT `name`, `value` FROM `widget_parameter_value` LEFT OUTER JOIN `widget_parameter_design` ON `id_param` = `id` WHERE `id_set` = :id_set;";
		$prep_select_params = NDOP::$app['db']->prepare($select_params);


		$prep_select_widget->execute(array(
			'id_widget' => $id_widget
			));

		$widget = $prep_select_widget->fetch(PDO::FETCH_ASSOC);

		$prep_select_params->execute(array(
			'id_set' => $id_widget_parameter_set
			));

		$params_fetch = $prep_select_params->fetchAll(PDO::FETCH_ASSOC);

		$params = array();
		foreach ($params_fetch as $key => $value) {
			$params[$value['name']] = $value['value'];
		}

		if($height == 2) {
			$class_height = "height-full";
		}else{
			$class_height = "height-half";
		}
		echo "<div class='span".$width." ".$class_height."' >";
		if($id_widget > 0){
			$id = ++NDOP::$nb_widget;
			include "./widgets/".$widget['folder_name']."/content.php";
		}else{

		}

		echo "</div>";
	}

	public static function header_display($title){

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

	public static function load_IP_conf(){
		if(isset(NDOP::$app['db']) && NDOP::$app['db']){
			$obj = array();

			$sql = "SELECT * FROM  `server_information` WHERE name='data_server' ;";
			$results = NDOP::$app['db']->query($sql);
			$address = $results->fetch(PDO::FETCH_ASSOC);

			if(isset($address['ip']) && isset($address['port'])){
				$obj['NDOPAddress'] = 'ws://'.$address['ip'].':'.$address['port'];
			}

			// $sql = "SELECT * FROM  `server_information` WHERE name='freegeoip_server' ;";
			// $results = NDOP::$app['db']->query($sql);
			// $address = $results->fetch(PDO::FETCH_ASSOC);

			// if(isset($address['ip']) && isset($address['port'])){
			// 	$obj['freeGeoIpAdress'] = $address['ip'].':'.$address['port'];
			// }

			$obj['webServerAddress'] = $_SERVER['SERVER_ADDR'];

			$app = array();
			// $app['App'] = $obj;

			return 'var App = '.json_encode($obj).';';
		}
		return '';
	}

	public static function load_slide_conf(){
		if(isset(NDOP::$app['db']) && NDOP::$app['db']){

			$sql = "SELECT * FROM  `slide_configuration` ;";
			$results = NDOP::$app['db']->query($sql);
			$conf = $results->fetch(PDO::FETCH_ASSOC);

			if(isset($conf['interval'])){
				$interval = $conf['interval'];
			}else{
				$interval = 15000;
			}

			if(isset($conf['auto_start'])){
				if($conf['auto_start']){
					$auto_start = 'true';
				}else{
					$auto_start = 'false';
				}
			}else{
				$auto_start = 'false';
			}

			if(isset($conf['pause_on_hover'])){
				if($conf['pause_on_hover']){
					$pause_on_hover = 'true';
				}else{
					$pause_on_hover = 'false';
				}
			}else{
				$pause_on_hover = 'false';
			}

			if(isset($conf['update_id'])){
				$update_id = $conf['update_id'];
			}else{
				$update_id = 0;
			}
			if(isset($conf['update_check_interval'])){
				$update_check_interval = $conf['update_check_interval'];
			}else{
				$update_check_interval = 900000;
			}

			if(isset($conf['update_id'])){
				$update_id = $conf['update_id'];
			}else{
				$update_id = 0;
			}
			if(isset($conf['background_color'])){
				$background_color = $conf['background_color'];
			}else{
				$background_color = '#CCCCCC';
			}


			$js = '
			$(function() {

			    $("#slides").slidesjs({
			        width: window.innerWidth,
			        height: window.innerHeight - 20,
			        start: 1,
			        play: {
			            active: true,
			            // [string] Can be either "slide" or "fade".
			            // effect: "fade"

			            // [number] Time spent on each slide in milliseconds.
			            interval: '.$interval.',

			            // [boolean] Start playing the slideshow on load.
			            auto: '.$auto_start.',

			            // [boolean] show/hide stop and play buttons
			            swap: false,

			            // [boolean] pause a playing slideshow on hover
			            pauseOnHover: '.$pause_on_hover.',

			            // [number] restart delay on inactive slideshow
			            restartDelay: 2500
			        },
			        navigation: false
			    });

			    // handle the navigation with left and right arrows
			    $(window).keyup(function(e) {
			        var key = e.which | e.keyCode;
			        if (key === 37) { // 37 is left arrow
			            $(".slidesjs-previous").click();
			        } else if (key === 39) { // 39 is right arrow
			            $(".slidesjs-next").click();
			        } else if (key === 38) { // 39 is right arrow
			            resize();
			        }
			    });
			});';

			$js .= '
				var refresh_manager = new RefreshManager('.$update_id.');
				refresh_manager.connect(App.webServerAddress, "app/sql_request.php?request=update_id", '.$update_check_interval.');
			';

			$js .= '
				$(function(){
					$("body").css("background-color", "'.$background_color.'");
				});
			';


			return $js;
		}else{
			return '
			$(function(){
      			$("#slides").slidesjs({
        			width: window.innerWidth,
        			height: window.innerHeight - 20,
        			play: {
        				play: false
        			},
        			navigation: false
      			});
    		});';
		}
	}
}

