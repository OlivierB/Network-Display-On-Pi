
function IpLocationMap(id){
	//Ip displayed on the map
	this.ips = [];


	this.map = L.map(id).setView([45.597889, -11.304932], 2);

	L.tileLayer('http://{s}.tile.cloudmade.com/6b0ce74e6f434a7eb264a178d75f0458/997/256/{z}/{x}/{y}.png', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
		maxZoom: 18
	}).addTo(this.map);

}

IpLocationMap.prototype = {
	constructor: IpLocationMap,

	addPoint : function (lat, long, color){

		color = color || "red";

		var circle = L.circle([lat, long], 100, {
			color: color,
			fillColor: color,
			fillOpacity: 0.5
		}).addTo(this.map);
	},

	addPointFromIP : function (ip, color){
		var that = this;
		// console.log("http://" + App.freeGeoIpAdress + "/json/" + ip)
		$.ajax({ type: "GET",   
			url: "http://" + App.freeGeoIpAdress + "/json/" + ip,   
			async: true,
			success: function(data){
				that.addPoint(data.latitude, data.longitude, color);
			}
		});


	},

	connect : function (address, protocol){
		var that = this;
		// console.log('tentative de connexion');

		this.address = address || App.serverAddress || 'localhost';
		this.prot = protocol || App.ipListProtocol || 'iplist';
		
		this.connection = new WebSocket(this.address, this.prot);

		// When the connection is open, send some data to the server
		this.connection.onopen = function () {
			console.log(" IPlconnexion");
			$('#alert-map').html('');
		  	that.connection.send('Ping'); // Send the message 'Ping' to the server

		  };

		// Log errors
		this.connection.onerror = function (error) {
			console.log('WebSocket Error ' + error);
			$('#alert-map').text('Connection error : ' + error);
		};

		// Log messages from the server
		this.connection.onmessage = function (e) {
			// console.log('Server: ' + e.data);

			var obj = JSON.parse(e.data);

			// console.log('last ' + last + ', length ' + obj.ip_dst.length);
			if(obj.iplist != null){
				for(var i= 0; i < obj.iplist.length; i++)
				{
					if(that.ips[obj.iplist[i]] == null)
					{
						that.addPointFromIP(obj.iplist[i]);
						// console.log('ip ajoutee ' + obj.ip_dst[i]);
						that.ips[obj.iplist[i]] = 1;
					}
				}
			}
			
		};

		this.connection.onclose = function (e) {
			// console.log('Deconnexion tentative de reconnexion dans 5 sec !');
			$('#alert-map').html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
			setTimeout(function(){that.connect(that.address, that.prot);}, 5000);
		};

	}
}