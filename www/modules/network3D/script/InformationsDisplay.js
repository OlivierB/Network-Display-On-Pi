function InformationsDisplay() {
	this.loadConf();
	this.infos = [];
}



InformationsDisplay.prototype.loadConf = function() {

	for (var i = 0; i < Network3DMakList.length; i++) {
		var tab = Network3DMakList[i].address.split('.');
		Network3DMakList[i].addressHexa = 0;
		for (var j = 0; j < 4; j++) {
			var val = parseFloat(tab[j]);
			Network3DMakList[i].addressHexa += (val << (8 * j));
		}
		// console.log(Network3DMakList[i].addressHexa)
	}

}


InformationsDisplay.prototype.addIp = function(ip) {
	var i = 0,
		length = Network3DMakList.length;

	while (i < length && (Network3DMakList[i].addressHexa != this.maskIp(ip, Network3DMakList[i].mask))) {
		// console.log(Network3DMakList[i].addressHexa);
		// console.log(ip + ' ' +  Network3DMakList[i].mask);
		// console.log(this.maskIp(ip, Network3DMakList[i].mask));
		i++;
	}
	// console.log('Hexa :' + ip);
	// console.log(Network3DMakList[i].color);
	if (i != length) {
		// var info = this.infos[Network3DMakList[i].address + '/' + Network3DMakList[i].mask];
		if (this.infos[Network3DMakList[i].address + '/' + Network3DMakList[i].mask] == null){
			this.infos[Network3DMakList[i].address + '/' + Network3DMakList[i].mask] = {number :1, textureColor: Network3DMakList[i].textureColor, fontColor: Network3DMakList[i].fontColor};
		} else{
			this.infos[Network3DMakList[i].address + '/' + Network3DMakList[i].mask].number++;
		}
		this.refreshDisplay();
		return {textureColor: Network3DMakList[i].textureColor, fontColor: Network3DMakList[i].fontColor};
	}
}


InformationsDisplay.prototype.maskIp = function(ip, mask) {
	var maskBin = 0xFFFFFFFF >>> (32 - mask);

	return (ip & maskBin);
}

InformationsDisplay.prototype.refreshDisplay = function() {
	var result = '<table class="table"><thead><tr><th>Network / IP</th><th>Number</th></tr></thead>';
	
	for(var mask in this.infos){
		// console.log(mask + ' ' + this.infos[mask].number);
		result += '<tr style="background-color:' + this.infos[mask].textureColor +';color:' + this.infos[mask].fontColor + '"><td>' + mask + '</td><td>' +  this.infos[mask].number + '</td></tr>';
	}

	result += '</table>';
	var container = $('#network3D-table-container');
	// container.empty();
	container.html(result);
}