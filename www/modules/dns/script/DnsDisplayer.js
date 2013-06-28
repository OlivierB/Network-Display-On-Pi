function DnsDisplayer(id) {
	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.container = $('#' + id);
	this.nbElemDisplayed = 0;

	this.elems = [];
	this.busy = false;

	this.lastElem = '';
}


// inheritance from WebSocketManager
DnsDisplayer.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the DnsDisplayer inheritance works
DnsDisplayer.prototype.dataManager = function(obj) {

	var i = obj.list_dns_name.length;
	for (; i--;) {
		console.log(obj.list_dns_name[i])

		if (this.elems.length > 0 && obj.list_dns_name[i] == this.elems[this.elems.length - 1].dnsName) {
			this.elems[this.elems.length - 1] = {
				dnsName: this.elems[this.elems.length - 1].dnsName,
				nb: this.elems[this.elems.length - 1].nb + 1
			}
		} else {
			this.elems.push({
				dnsName: obj.list_dns_name[i],
				nb: 1
			});
		}

		if (!this.busy) {
			this.addItem();
		}
	}
}

DnsDisplayer.prototype.addItem = function() {
	if (this.elems.length > 0) {
		this.busy = true;

		str = '<tr><td>' + this.elems[0].dnsName + '</td><td>' + this.elems[0].nb + '</td></tr>'

		$('#dns-table > tbody:first').prepend(str);
		this.elems.shift();

		if (this.nbElemDisplayed < App.NumberItemDNSList) {
			this.nbElemDisplayed++;
		} else {
			$('#dns-table tr:last').detach();
		}

		setTimeout(this.addItem.bind(this), 1000);
	} else {
		this.busy = false;
	}
};