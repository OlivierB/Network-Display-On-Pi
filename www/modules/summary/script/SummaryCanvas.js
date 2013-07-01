/**
 * To make sure the canvas is fitted to the page, every coordinates
 * are considered as a ratio on the page.
 **/

function SummaryCanvas(id) {

	this.id = id;

	// inheritance from AjaxManager
	AjaxManager.call(this, id + '-alert');

	// add the canvas to the DOM
	this.canvas = document.createElement('canvas');
	this.resize();
	document.getElementById(id).appendChild(this.canvas);

	// make sure the canvas stay fitted to the page
	$(window).resize(this.resize.bind(this));


	this.context = this.canvas.getContext('2d');


}

// inheritance from BandwidthChart
SummaryCanvas.prototype = Object.create(AjaxManager.prototype);

// method called by AjaxManager
SummaryCanvas.prototype.dataManager = function(obj) {
	this.save = obj[0];
	this.drawFromData(obj[0]);
}

SummaryCanvas.prototype.drawFromData = function(data) {
	this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);


	this.addRectangle(data.out_Ko, data.Ko, 0, 'rgb(69, 194, 197)');
	this.addRectangle(data.in_Ko, data.Ko, 1, 'rgb(247, 141, 63)');
	this.addRectangle(data.loc_Ko, data.Ko, 2, 'rgb(16, 46, 55)');

	this.drawLegend();
}


SummaryCanvas.prototype.addRectangle = function(value, global, position, color) {
	var ratio = value / global;

	var x = 1 / 6 + 3 / 12 * position;
	var y = 1 / 8 + (1 - ratio) * (1 / 2);

	var width = 1 / 6;
	var height = ratio * 1 / 2 + (1 / 35);

	this.context.beginPath();
	this.context.rect(this.ratioX(x), this.ratioY(y), this.ratioX(width), this.ratioY(height));
	this.context.fillStyle = color;
	this.context.fill();

	this.drawText(TextFormatter.formatNumber(value), this.ratioX(x + 1 / 12), this.ratioY(y - 1 / 35), color, this.ratioX(1 / 35), '');
}


SummaryCanvas.prototype.drawText = function(text, x, y, color, size, style) {
	this.context.font = style + " " + size + "pt ChampWoff";
	this.context.fillStyle = color;
	this.context.textAlign = 'center';
	this.context.fillText(text, x, y);
}



SummaryCanvas.prototype.resize = function() {
	this.canvas.width = $('#' + this.id).width();
	this.canvas.height = $('#' + this.id).height();

	if (this.save != null) {
		this.drawFromData(this.save);
		this.drawLegend();
	}
}

SummaryCanvas.prototype.ratioX = function(value) {
	return value * this.canvas.width;
}

SummaryCanvas.prototype.ratioY = function(value) {
	return value * this.canvas.height;
}


SummaryCanvas.prototype.drawLegend = function() {
	var y = 5 / 8 + 1 / 70;

	this.drawText('UP', this.ratioX(3 / 12), this.ratioY(y), 'black', this.ratioX(1 / 30), 'bold');
	this.drawText('DOWN', this.ratioX(6 / 12), this.ratioY(y), 'black', this.ratioX(1 / 30), 'bold');
	this.drawText('LOCAL', this.ratioX(9 / 12), this.ratioY(y), '#9A9A9A', this.ratioX(1 / 30), 'bold');
}