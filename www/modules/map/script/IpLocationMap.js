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
		var i = obj.iplist.length;
		for (;i--;) {
			var ip = obj.iplist[i];
			if (this.ips[ip] == null) {
				this.addPointFromIP(ip);
				this.ips[ip] = 1;
			}
		}
	}
}