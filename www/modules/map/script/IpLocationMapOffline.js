function IpLocationMapOffline(id) {

	this.id = id;

	// inheritance from IpLocationMap
	IpLocationMap.call(this, id);

	// add the canvas to the DOM
	this.canvas = document.createElement('canvas');
	document.getElementById(id).appendChild(this.canvas);

	// handle the resize of the window
	


	this.context = this.canvas.getContext('2d');

	this.resize();

	// Map Load
	var imageObj = new Image();
	imageObj.src = '/res/img/earth_bw.png';

	imageObj.onload = function() {

		// computing width, height, and position of the map so it is centered and the bigger possible
		// without distortions
		var screenRatio = this.canvas.width / this.canvas.height;
		var imageRatio = imageObj.width / imageObj.height;

		// if the width is blocking
		if (screenRatio < imageRatio) {
			this.mapWidth = this.canvas.width;
			this.mapHeight = this.canvas.width / imageRatio;

			this.paddingHeight = (this.canvas.height - this.mapHeight) / 2;
			this.paddingWidth = 0;
		} else {
		// if the height is blocking
			this.mapHeight = this.canvas.height;
			this.mapWidth = this.canvas.height * imageRatio;

			this.paddingHeight = 0;
			this.paddingWidth = (this.canvas.width - this.mapWidth) / 2;
		}

		this.context.drawImage(imageObj, this.paddingWidth, this.paddingHeight, this.mapWidth, this.mapHeight);

	}.bind(this);



}

// inheritance from IpLocationMap
IpLocationMapOffline.prototype = Object.create(IpLocationMap.prototype);

IpLocationMapOffline.prototype.addPoint = function(lat, long, color) {

	color = color || "red";

	// conversion from long, lat (deg) in x, y coordinate (Equidistant Cylindrical Projection)
	var x = this.mapWidth * (180 + long) / 360 + this.paddingWidth;
	var y = this.mapHeight * (90 - lat) / 180 + this.paddingHeight;

	this.drawCircle(x, y, 3, color);
	// console.log('ajout');

}


IpLocationMapOffline.prototype.drawCircle = function(centerX, centerY, radius, color) {
	this.context.beginPath();
	this.context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
	this.context.fillStyle = color;
	this.context.fill();
	this.context.lineWidth = 1;
	this.context.strokeStyle = 'black';
	this.context.stroke();
}

IpLocationMapOffline.prototype.resize = function() {
	this.canvas.width = $('#' + this.id).width();
	this.canvas.height = $('#' + this.id).height();	
}