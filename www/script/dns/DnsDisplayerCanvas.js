/**
 * DnsDisplayerCanvas, class displaying the bubbles showing the dns request.
 * @author Matrat Erwam
 **/

function DnsDisplayerCanvas(id, font_size, draw_bubble) {
    // inheritance from DnsDisplayer
    DnsDisplayer.call(this, id);

    this.bubbles = [];

    this.id = id;
    this.font_size = font_size;
    this.draw_bubble = draw_bubble;

    // add the canvas to the DOM
    this.canvas = document.createElement('canvas');
    this.resize();
    document.getElementById(id).appendChild(this.canvas);

    // make sure the canvas stay fitted to the page
    $(window).resize(this.resize.bind(this));

    this.context = this.canvas.getContext('2d');

    this.images = [];

    var img = new Image();
    img.src = '/res/img/redBubble.png';
    this.images[0] = img;

    img = new Image();
    img.src = '/res/img/blueBubble.png';
    this.images[1] = img;

    img = new Image();
    img.src = '/res/img/greenBubble.png';
    this.images[2] = img;

    img = new Image();
    img.src = '/res/img/bubble.png';
    this.images[3] = img;
    img.onload = function() {
        this.busy = false;
    }.bind(this);


    this.bubbleSize = 150;

    // avoid to stack the bubble when the canvas is not drawn (window hidden)
    this.needRedraw = false;

    this.animate();

}


// inheritance from DnsDisplayer
DnsDisplayerCanvas.prototype = Object.create(DnsDisplayer.prototype);



DnsDisplayerCanvas.prototype.addItem = function() {
    // display items one by one
    if (this.elems.length > 0) {
        this.busy = true;

        // avoid to draw when requestAnimationFrame() isn't called
        if(!this.needRedraw){
            this.addBubble(this.elems[0].dnsName);
        }

        this.needRedraw = true;

        this.elems.shift();
        setTimeout(this.addItem.bind(this), 1000);
    } else {
        this.busy = false;
    }
};

DnsDisplayerCanvas.prototype.addBubble = function(dnsName) {
    // var x = Math.random() * (this.canvas.width - this.bubbleSize/2);
    // var y = this.canvas.height ;
    var indexImg = Math.floor(Math.random()*this.images.length);

    var bubble = new BubbleDns(this.context, this.canvas.width, this.canvas.height, dnsName, 0, this.images[indexImg], this.font_size, this.draw_bubble);

    this.bubbles.push(bubble);
};

DnsDisplayerCanvas.prototype.animate = function() {
    requestAnimationFrame(this.animate.bind(this));

    this.render();
};

DnsDisplayerCanvas.prototype.render = function() {

    this.needRedraw = false;

    // clear the canvas
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

    var i = this.bubbles.length;
    for (; i--;) {
        if (!this.bubbles[i].update()) {
            delete this.bubbles[i];
            this.bubbles.splice(i, 1);
        }else{
            this.bubbles[i].display();
        }
    }
};

DnsDisplayerCanvas.prototype.resize = function() {
    this.canvas.width = $('#' + this.id).width();
    this.canvas.height = $('#' + this.id).height();
};