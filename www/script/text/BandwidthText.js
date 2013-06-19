BandwidthText = function(id) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.id = id;
}


// inheritance from WebSocketManager
BandwidthText.prototype = Object.create(WebSocketManager.prototype);


BandwidthText.prototype.dataManager = function(obj) {


	var res = '<table>'

	res = '<tr><td>Global</td>  <td><span class="bandwidth-number">' + $.number(obj.Ko) + ' kB/s </span></td></tr>';
	res +='<tr><td>Local</td>  <td><span class="bandwidth-number">' + $.number(obj.loc_Ko) + ' kB/s  </span></td></tr>';
	res +='<tr><td>Incoming</td> <td><span class="bandwidth-number">' + $.number(obj.in_Ko) + ' kB/s  </span></td></tr>';
	res +='<tr><td>Outcoming</td>  <td><span class="bandwidth-number">' + $.number(obj.out_Ko) + ' kB/s  </span></td></tr>';

	$('#' + this.id).html(res);

	// obj.loc_Ko obj.in_Ko, obj.out_Ko, obj.Ko
}