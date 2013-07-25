/**
 * IpLocationMapOffline, class inheriting from IpLocation and using a local map o the earth
 * (Equidistant Cylindrical Projection) to display IPs.
 * @author Matrat Erwan
 **/

function IpLocationMapOffline(id, dither, opacity) {

    this.id = id;
    this.dither = dither;
    this.opacity = opacity;

    // inheritance from IpLocationMap
    IpLocationMap.call(this, id);

    // add the canvas to the DOM
    this.canvas = document.createElement('canvas');
    document.getElementById(id).appendChild(this.canvas);



    this.context = this.canvas.getContext('2d');

    this.resize();

    // Map Load
    var imageObj = new Image();
    imageObj.src = 'res/img/earth_bw.png';

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

IpLocationMapOffline.prototype.addPoint = function(lat, longi, color) {

    color = color || "red";

    // conversion from long, lat (deg) in x, y coordinate (Equidistant Cylindrical Projection)
    var x = this.mapWidth * (180 + longi) / 360 + this.paddingWidth;
    var y = this.mapHeight * (90 - lat) / 180 + this.paddingHeight;

    x += (Math.random()-0.5) * this.dither;
    y += (Math.random()-0.5) * this.dither;

    this.drawCircle(x, y, 3, color);

};


IpLocationMapOffline.prototype.drawCircle = function(centerX, centerY, radius, color) {
    this.context.globalAlpha = this.opacity;
    this.context.beginPath();
    this.context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
    this.context.fillStyle = color;
    this.context.fill();
 };

IpLocationMapOffline.prototype.resize = function() {
    this.canvas.width = $('#' + this.id).width();
    this.canvas.height = $('#' + this.id).height();
};