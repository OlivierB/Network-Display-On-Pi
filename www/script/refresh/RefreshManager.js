function RefreshManager(update_id) {
    // inheritance from AjaxManager
    AjaxManager.call(this);

    this.update_id = update_id;
}

// inheritance from AjaxManager
RefreshManager.prototype.connect = AjaxManager.prototype.connect;
RefreshManager.prototype.load = AjaxManager.prototype.load;

RefreshManager.prototype.dataManager = function(obj) {

    if (this.update_id != parseInt(obj.update_id)) {
        this.update_id = parseInt(obj.update_id);
        document.location.reload();
    }
};