/**
 * IpLocationMap, abstract class handling data from the NDOP program and requesting 
 * freegeoip to get location of IPs address.
 * @author Matrat Erwan
 **/

function IpLocationMap(id) {

    // inheritance from WebSocketManager
    WebSocketManager.call(this, id + '-alert');

    //Ips displayed on the map
    this.ips = [];

}

// inheritance from WebSocketManager
IpLocationMap.prototype = Object.create(WebSocketManager.prototype);



IpLocationMap.prototype.addPointFromIP = function(ip, color) {
    $.ajax({
        type: "GET",
        url: "http://" + App.freeGeoIpAdress + "/json/" + ip,
        async: true,
        success: function(data) {
            this.addPoint(data.latitude, data.longitude, color);
        }.bind(this)
    });
};

// method called by WebSocketManager
IpLocationMap.prototype.dataManager = function(obj) {
    if (obj.iplist !== null) {
        var i = obj.iplist.length;
        for (;i--;) {
            var ip = obj.iplist[i];
            if (!(ip in this.ips) ) {
                this.addPointFromIP(ip);
                this.ips[ip] = 1;
            }
        }
    }
};