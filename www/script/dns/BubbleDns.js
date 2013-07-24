/**
 * BubbleDns, class modeling the dns request bubble.
 * @author Matrat Erwan
 **/

function BubbleDns(context, canvas_width, canvas_height, text, limitY, image, font_size) {
    this.context = context;

    this.canvas_width = canvas_width;
    this.canvas_height = canvas_height;

    this.text = text;
    this.limitY = limitY;
    this.image = image;
    this.font_size = font_size;


    this.moveX = 0;


    this.context.font = "bold "+this.font_size+"pt ChampWoff";
    this.context.textAlign = 'center';

    this.size = this.context.measureText(this.text).width + 20;
    this.semi_size = this.size / 2;

    this.x = Math.random() * (this.canvas_width - this.size);
    this.y = this.canvas_height + this.semi_size;

}

BubbleDns.prototype.display = function() {

    this.context.fillText(this.text, this.x + 0, this.y + 0);

    this.context.drawImage(this.image, this.x - this.semi_size, this.y - this.semi_size, this.size, this.size);

};

// Make the bubble go up and give a random change of direction
BubbleDns.prototype.update = function() {
    this.y -= 2;

    this.moveX += (Math.random()-0.5) / 10;
    this.x += this.moveX;
    return this.limitY < this.y + this.size;
};