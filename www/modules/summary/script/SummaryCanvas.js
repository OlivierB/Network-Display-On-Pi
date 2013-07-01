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

	// used to make sure the legend fit in the bar
	this.minHeight = -1;
}

// inheritance from BandwidthChart
SummaryCanvas.prototype = Object.create(AjaxManager.prototype);

// method called by AjaxManager
SummaryCanvas.prototype.dataManager = function(obj) {
	// in order to redraw the data whe the window is resized
	this.save = obj;

	this.drawFromData(obj);
}

SummaryCanvas.prototype.drawFromData = function(data) {
	// clear the context
	this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

	var list = data.list;
	this.addBar(list.out_Ko, list.Ko, 0, 'rgb(69, 194, 197)');
	this.addBar(list.in_Ko, list.Ko, 1, 'rgb(247, 141, 63)');
	this.addBar(list.loc_Ko, list.Ko, 2, 'rgb(16, 46, 55)');

	this.drawDate(data.date_begin);

	this.drawLegend();
	
}


SummaryCanvas.prototype.addBar = function(value, global, position, color) {
	var ratio = value / global;

	// values correspond to the disposition on the page
	var x = 1 / 6 + 3 / 12 * position;
	var y = 1 / 8 + (1 - ratio) * (1 / 2);

	var width = 1 / 6;
	var height = ratio * 1 / 2 + (1 / 35);

	// keep the smallest height of bars
	if(this.minHeight == -1 || this.minHeight > height)
		this.minHeight = height;

	// draw bars
	this.context.beginPath();
	this.context.rect(this.ratioX(x), this.ratioY(y), this.ratioX(width), this.ratioY(height));
	this.context.fillStyle = color;
	this.context.fill();

	// draw value on top of the bar
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

	// redraw from the saved data
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
	var color1 = 'black';
	var color2 = '#9A9A9A';

	// if the smallest bar is smaller than the size of font, the text goes out of the bar
	if(this.minHeight > -1 && this.minHeight < 1/30 * this.canvas.width/this.canvas.height + 1/70){
		y += 1/30 * this.canvas.width/this.canvas.height + 1/70;
		color2 = 'black';
	}
		

	

	this.drawText('UP', this.ratioX(3 / 12), this.ratioY(y), color1, this.ratioX(1 / 30), 'bold');
	this.drawText('DOWN', this.ratioX(6 / 12), this.ratioY(y), color1, this.ratioX(1 / 30), 'bold');
	this.drawText('LOCAL', this.ratioX(9 / 12), this.ratioY(y), color2, this.ratioX(1 / 30), 'bold');
}

SummaryCanvas.prototype.drawDate = function(date) {
	var y = 6 / 8 + 1 / 30;

	this.drawText('Since ' + date, this.ratioX(3 / 12), this.ratioY(y), 'black', this.ratioX(1 / 40), 'bold');
}