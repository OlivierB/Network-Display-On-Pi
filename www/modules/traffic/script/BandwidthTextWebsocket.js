BandwidthTextWebsocket = function(id) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.id = id;
	this.container = $('#' + this.id);
}


// inheritance from WebSocketManager
BandwidthTextWebsocket.prototype = Object.create(WebSocketManager.prototype);


BandwidthTextWebsocket.prototype.dataManager = function(obj) {


	var res = '<table><thead><tr><th colspan="2">Current traffic</th></tr></thead>'

	res += '<tr><td>Global</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.Ko) + '/s </span></td></tr>';
	res +='<tr><td>Local</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.loc_Ko) + '/s  </span></td></tr>';
	res +='<tr><td>Incoming</td> <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.in_Ko) + '/s  </span></td></tr>';
	res +='<tr><td>Outcoming</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.out_Ko) + '/s  </span></td></tr>';

	this.container.html(res);

	// obj.loc_Ko obj.in_Ko, obj.out_Ko, obj.Ko
}