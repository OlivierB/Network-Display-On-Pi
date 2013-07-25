BaseAlert = function(id) {
    this.id = id;
    this.alertContainer = $("#" + this.id + "-alert");
    this.container = $("#" + this.id);
}

BaseAlert.prototype.load = function() {

    $.ajax({
        type: "GET",
        url: this.url,
        async: true,
        success: function(data) {
            this.container.html(data);
            this.alertContainer.html('');
        }.bind(this),

        error: function() {
            var msg = '<span class="alert">Cannot reach the BASE page (Snort web page).</span>';
            this.alertContainer.html(msg);
        }.bind(this)
    });
    setTimeout(this.load.bind(this), this.timeout);
};

BaseAlert.prototype.connect = function(address, url, timeout) {
    this.url = url;
    this.address = address;
    this.timeout = timeout;

    this.load();
};