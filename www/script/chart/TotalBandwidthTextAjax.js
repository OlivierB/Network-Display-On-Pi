TotalBandwidthText = function(id) {

	// inheritance from WebSocketManager
	AjaxManager.call(this, id + '-alert');

	this.id = id;

	this.container = $('#' + this.id);
}


// inheritance from WebSocketManager
TotalBandwidthText.prototype = Object.create(AjaxManager.prototype);


TotalBandwidthText.prototype.dataManager = function(obj) {

	var obj =(obj[0])
	// console.log(obj)
	var res = '<table><thead><tr><th colspan="2">Total traffic</th></tr></thead>'

	res += '<tr><td>Global</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.Ko) + ' </span></td></tr>';
	res +='<tr><td>Local</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.loc_Ko) + '  </span></td></tr>';
	res +='<tr><td>Incoming</td> <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.in_Ko) + '  </span></td></tr>';
	res +='<tr><td>Outcoming</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.out_Ko) + '  </span></td></tr>';

	this.container.html(res);

}

