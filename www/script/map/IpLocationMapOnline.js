/**
 * IpLocationMapOnline, class inheriting from IpLocation and using an online map system 
 * (Leaflet http://leafletjs.com/, Openstreetmap http://www.openstreetmap.org/) to display IPs.
 * @author Matrat Erwan
 **/

function IpLocationMapOnline(id, dither, opacity, freeGeoIpAdress){

    this.dither = dither;
    this.opacity = opacity;

    IpLocationMap.call(this, id, freeGeoIpAdress);

    this.map = L.map(id).setView([45.597889, -11.304932], 2);

    L.tileLayer('http://{s}.tile.cloudmade.com/6b0ce74e6f434a7eb264a178d75f0458/997/256/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 18
    }).addTo(this.map);
}

// inheritance from IpLocationMap
IpLocationMapOnline.prototype = Object.create(IpLocationMap.prototype);

IpLocationMapOnline.prototype.addPoint = function(lat, longi, color) {

    color = color || "red";

    lat += (Math.random()-0.5) * this.dither;
    longi += (Math.random()-0.5) * this.dither;

    L.circle([lat, longi], 100, {
        color: color,
        fillColor: color,
        fillOpacity: this.opacity
    }).addTo(this.map);
};