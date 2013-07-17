function BandwidthChartAjax(id) {

    // inheritance from BandwidthChart
    BandwidthChart.call(this, id, false, -1);

    // inheritance from AjaxManager
    AjaxManager.call(this, id + '-alert');

}


// inheritance from BandwidthChart
BandwidthChartAjax.prototype = Object.create(BandwidthChart.prototype);

// inheritance from AjaxManager
BandwidthChartAjax.prototype.connect = AjaxManager.prototype.connect;
BandwidthChartAjax.prototype.load = AjaxManager.prototype.load;

BandwidthChartAjax.prototype.dataManager = function(obj) {
    var i = 0,
        length = obj.length;
    for (; i < length; i++) {
        var tmp = obj[i];
        this.updateChart(parseInt(tmp.local), parseInt(tmp.incoming), parseInt(tmp.outcoming), parseInt(tmp.global), (tmp.date));
    }
    this.refresh();
    this.clean();
};