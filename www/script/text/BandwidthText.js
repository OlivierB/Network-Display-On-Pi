/**
 * BandwidthText, abstract class displaying bandwidth informations in a text format.
 * @author Matrat Erwan
 **/

function BandwidthText(id, font_size) {

    this.id = id;

    this.container = $('#' + this.id);
    this.font_size = font_size;
}



BandwidthText.prototype.dataManager = function(data) {

    var obj;
    if(data.list){
        obj = data.list;
    }else{
        obj = data;
    }
    var res = '<table style="font-size:' + this.font_size + 'px;line-height:' + this.font_size + 'px;"><thead><tr><th colspan="2">Total traffic</th></tr></thead>';

    res += '<tr><td>Global</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.Ko) + ' </span></td></tr>';
    res += '<tr><td>Local</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.loc_Ko) + '  </span></td></tr>';
    res += '<tr><td>Incoming</td> <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.in_Ko) + '  </span></td></tr>';
    res += '<tr><td>Outcoming</td>  <td><span class="bandwidth-number">' + TextFormatter.formatNumber(obj.out_Ko) + '  </span></td></tr>';

    this.container.html(res);

};