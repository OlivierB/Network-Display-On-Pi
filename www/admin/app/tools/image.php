<?php

Class Thumbnail
{
	private $image; 

	private $width; 
	private $height;

	private $step_w;
	private $step_h;

	private $save_file;
	function __construct($id_module){
		$this->width = 768; 
		$this->height = $this->width / 1.62;

		$this->step_w = $this->width / 12;
		$this->step_h = $this->height / 2;

		$this->image = @imagecreatetruecolor ($this->width, $this->height);
		ImageColorAllocate ($this->image, 204, 204, 204); 
		$bg = imagecolorallocate ( $this->image, 204, 204, 204 );
		imagefill ( $this->image, 0, 0, $bg );


		$this->save_file  = 'assets/images/module_thumbnail/'.$id_module.'.png';
	}

	function add_widget($x, $y, $w, $h, $folder_name){

		$widget_file = ("../widgets/".$folder_name."/thumbnail.png"); 
		$widget = imagecreatefrompng($widget_file);

		list($img_w, $img_h) = getimagesize($widget_file);

		imagecopyresized($this->image, $widget, $x *  $this->step_w, $y * $this->step_h, 0, 0, $w * $this->step_w, $h * $this->step_h, $img_w, $img_h);
	}

	function save() {
		imagepng($this->image, $this->save_file);
	}

	function __destruct() {
        imagedestroy($this->image);
    }

    public static function check_thumbnails_existence($modules, $db){
    	$select_module_widgets = "SELECT * FROM `module` JOIN `module_composition_widget` ON `module`.`id` = `module_composition_widget`.`id_module` JOIN `widget` ON `module_composition_widget`.`id_widget` = `widget`.`id` WHERE `module`.`id` = :id_module";
		$prep_select_module_widgets = $db->prepare($select_module_widgets);

		foreach ($modules as $key => $value) {
			if(!file_exists('assets/images/module_thumbnail/'.$value['id'].'.png')){
				Thumbnail::create_thumbnail_from_id($value['id'], $prep_select_module_widgets);
			}
			
		}
    }

    public static function create_thumbnail_from_id($id, $prep_request){
		$prep_request->execute(array("id_module" => $id));
		$widgets = $prep_request->fetchAll(PDO::FETCH_OBJ);
		$thumbnail = new Thumbnail($id);
		foreach ($widgets as $key => $widget) {
			$thumbnail->add_widget($widget->x, $widget->y, $widget->width, $widget->height, $widget->folder_name);
		}
		$thumbnail->save();
	}
}
