function IpLocationMap(id) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	//Ip displayed on the map
	this.ips = [];


	this.map = L.map(id).setView([45.597889, -11.304932], 2);

	L.tileLayer('http://{s}.tile.cloudmade.com/6b0ce74e6f434a7eb264a178d75f0458/997/256/{z}/{x}/{y}.png', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
		maxZoom: 18
	}).addTo(this.map);

}

// inheritance from WebSocketManager
IpLocationMap.prototype = Object.create(WebSocketManager.prototype);

IpLocationMap.prototype.addPoint = function(lat, long, color) {

	color = color || "red";

	var circle = L.circle([lat, long], 100, {
		color: color,
		fillColor: color,
		fillOpacity: 0.5
	}).addTo(this.map);
}

IpLocationMap.prototype.addPointFromIP = function(ip, color) {
	
	// console.log("http://" + App.freeGeoIpAdress + "/json/" + ip)
	$.ajax({
		type: "GET",
		url: "http://" + App.freeGeoIpAdress + "/json/" + ip,
		async: true,
		success: function(data) {
			this.addPoint(data.latitude, data.longitude, color);
		}.bind(this)
	});
}


IpLocationMap.prototype.dataManager = function(obj) {
	if(obj.iplist != null){
		for (var i = 0; i < obj.iplist.length; i++) {
			if (this.ips[obj.iplist[i]] == null) {
				this.addPointFromIP(obj.iplist[i]);
				// console.log('ip ajoutee ' + obj.ip_dst[i]);
				this.ips[obj.iplist[i]] = 1;
			}
		}
	}
}
