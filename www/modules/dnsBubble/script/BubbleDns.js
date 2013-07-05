function BubbleDns(context, x, y, text, limitY, image, size) {
	this.context = context;
	this.x = x;
	this.y = y;
	this.text = text;
	this.limitY = limitY;
	this.image = image;
	this.size = size;

	this.moveX = 0;

}

BubbleDns.prototype.display = function() {
	this.context.font = "bold 15pt ChampWoff";
	// this.context.fillStyle = color;
	this.context.textAlign = 'center';
	var size = this.context.measureText(this.text).width + 20;
	this.context.fillText(this.text, this.x + size/2, this.y + size/2);

	this.context.drawImage(this.image, this.x, this.y, size, size);

	this.size = size;
};

BubbleDns.prototype.update = function() {
	this.y -= 2;

	this.moveX += (Math.random()-0.5) / 10;
	this.x += this.moveX;
	return this.limitY < this.y + this.size;
};