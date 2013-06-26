function StackedColumnChartAjax(id){
	// inheritance from AjaxManager
	AjaxManager.call(this, id + '-alert');
}

// inheritance from AjaxManager
BandwidthChartAjax.prototype = Object.create(AjaxManager.prototype);



StackedColumnChartAjax.prototype.connect = function(address, port, path) {
	 
};