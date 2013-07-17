function InformationsDisplay(id_container) {
    this.loadConf();
    this.infos = [];

    this.id_container = id_container;
}



InformationsDisplay.prototype.loadConf = function() {

    for (var i = 0; i < Network3DMaskList.length; i++) {
        var tab = Network3DMaskList[i].address.split('.');
        Network3DMaskList[i].addressHexa = 0;
        for (var j = 0; j < 4; j++) {
            var val = parseFloat(tab[j]);
            Network3DMaskList[i].addressHexa += (val << (8 * j));
        }
    }

};


InformationsDisplay.prototype.addIp = function(ip) {
    var i = 0,
        length = Network3DMaskList.length;

    while (i < length && (Network3DMaskList[i].addressHexa != this.maskIp(ip, Network3DMaskList[i].mask))) {
        i++;
    }
    if (i != length) {
        if (!((Network3DMaskList[i].address + '/' + Network3DMaskList[i].mask) in this.infos)) {
            this.infos[Network3DMaskList[i].address + '/' + Network3DMaskList[i].mask] = {
                number: 1,
                textureColor: Network3DMaskList[i].textureColor,
                fontColor: Network3DMaskList[i].fontColor
            };
        } else {
            this.infos[Network3DMaskList[i].address + '/' + Network3DMaskList[i].mask].number++;
        }
        this.refreshDisplay();
        return {
            textureColor: Network3DMaskList[i].textureColor,
            fontColor: Network3DMaskList[i].fontColor
        };
    }
};


InformationsDisplay.prototype.maskIp = function(ip, mask) {
    var maskBin = 0xFFFFFFFF >>> (32 - mask);

    return (ip & maskBin);
};

InformationsDisplay.prototype.refreshDisplay = function() {
    var result = '<table class="table"><thead><tr><th>Network / IP</th><th>Number</th></tr></thead>';

    for (var mask in this.infos) {
        result += '<tr style="background-color:' + this.infos[mask].textureColor + ';color:' + this.infos[mask].fontColor + '"><td>' + mask + '</td><td>' + this.infos[mask].number + '</td></tr>';
    }

    result += '</table>';
    var container = $('#' + this.id_container + '-table-container');
    container.html(result);
};