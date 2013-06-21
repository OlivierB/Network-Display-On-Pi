function IpLocationMapOnline(id){

	IpLocationMap.call(this, id);

	this.map = L.map(id).setView([45.597889, -11.304932], 2);

	L.tileLayer('http://{s}.tile.cloudmade.com/6b0ce74e6f434a7eb264a178d75f0458/997/256/{z}/{x}/{y}.png', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
		maxZoom: 18
	}).addTo(this.map);
}

// inheritance from IpLocationMap
IpLocationMapOnline.prototype = Object.create(IpLocationMap.prototype);

IpLocationMapOnline.prototype.addPoint = function(lat, long, color) {

	color = color || "red";


	var circle = L.circle([lat, long], 100, {
		color: color,
		fillColor: color,
		fillOpacity: 0.5
	}).addTo(this.map);

}