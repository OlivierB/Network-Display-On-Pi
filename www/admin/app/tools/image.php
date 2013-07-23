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
}
