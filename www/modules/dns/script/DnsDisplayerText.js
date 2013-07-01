function DnsDisplayerText(id) {
	// inheritance from DnsDisplayer
	DnsDisplayer.call(this, id);

	this.container = $('#' + id);
	this.nbElemDisplayed = 0;

}


// inheritance from DnsDisplayer
DnsDisplayerText.prototype = Object.create(DnsDisplayer.prototype);



DnsDisplayerText.prototype.addItem = function() {
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