/**
 * DnsDisplayerText, class displaying the dns request coming through the network as a table.
 **/

function DnsDisplayerText(id, number_item_dns_list, font_size) {
    // inheritance from DnsDisplayer
    DnsDisplayer.call(this, id);

    this.container = $('#' + id);
    this.nbElemDisplayed = 0;

    this.number_item_dns_list = number_item_dns_list;

    this.container.css('font-size', font_size);
}


// inheritance from DnsDisplayer
DnsDisplayerText.prototype = Object.create(DnsDisplayer.prototype);


// method need to make the inheritance from DnsDisplayer work
DnsDisplayerText.prototype.addItem = function() {
    if (this.elems.length > 0) {
        this.busy = true;

        str = '<tr><td>' + this.elems[0].dnsName + '</td><td>' + this.elems[0].nb + '</td></tr>';

        $('#dns-table > tbody:first').prepend(str);
        this.elems.shift();

        if (this.nbElemDisplayed < this.number_item_dns_list) {
            this.nbElemDisplayed++;
        } else {
            $('#dns-table tr:last').detach();
        }

        setTimeout(this.addItem.bind(this), 1000);
    } else {
        this.busy = false;
    }
};