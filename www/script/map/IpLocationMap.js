function IpLocationMap(id) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	//Ip displayed on the map
	this.ips = [];

}

// inheritance from WebSocketManager
IpLocationMap.prototype = Object.create(WebSocketManager.prototype);



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
	if (obj.iplist != null) {
		for (var i = 0; i < obj.iplist.length; i++) {
			if (this.ips[obj.iplist[i]] == null) {
				this.addPointFromIP(obj.iplist[i]);
				// console.log('ip ajoutee ' + obj.ip_dst[i]);
				this.ips[obj.iplist[i]] = 1;
			}
		}
	}
}