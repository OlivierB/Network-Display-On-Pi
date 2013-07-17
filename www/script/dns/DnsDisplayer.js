/**
 * DnsDisplayer, abstract class handling dns data coming from the websocket.
 * @author Matrat Erwan
 **/

function DnsDisplayer(id) {
    // inheritance from WebSocketManager
    WebSocketManager.call(this, id + '-alert');

    this.elems = [];
    this.busy = false;
}


// inheritance from WebSocketManager
DnsDisplayer.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the DnsDisplayer inheritance works
DnsDisplayer.prototype.dataManager = function(obj) {
    var i = obj.list_dns_name.length;
    for (; i--;) {

        if (this.elems.length > 0 && obj.list_dns_name[i] == this.elems[this.elems.length - 1].dnsName) {
            this.elems[this.elems.length - 1] = {
                dnsName: this.elems[this.elems.length - 1].dnsName,
                nb: this.elems[this.elems.length - 1].nb + 1
            };
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
};