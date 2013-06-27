function DnsDisplayer(id){
	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.container = $('#' + id);

}


// inheritance from WebSocketManager
DnsDisplayer.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the DnsDisplayer inheritance works
DnsDisplayer.prototype.dataManager = function(obj) {
	console.log(obj);
	this.container.html('');
	var i = obj.list_dns_name.length;
	for(;i--;){
		this.container.append(obj.list_dns_name[i] + '<br/>');
	}
}
