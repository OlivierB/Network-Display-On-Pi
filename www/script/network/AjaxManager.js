/**
 * AjaxManager abstract class, allow to get the result of the ajax request for a given
 * url and refresh by a time given. The inheriting class should implement a dataManager
 * function which will receive the data in the form of a js object.
 * @author Erwan Matrat
 **/

function AjaxManager(id_alert_container) {
    this.alertContainer = $('#' + id_alert_container);
}

AjaxManager.prototype.connect = function(address, path, time) {

    this.address = address;
    this.path = path;
    this.time = time;

    this.load();


};

AjaxManager.prototype.load = function() {

    $.ajax({
        type: "GET",
        url: this.path,
        async: true,
        success: function(data) {
            data = $.parseJSON(data);

            // give the data to the inheriting class
            this.dataManager(data);

            // will run a new request in the given time
            setTimeout(this.load.bind(this), this.time);
        }.bind(this),

        error: function() {
            // display an error warning on the page if the page cannot be reach
            var msg = '<span class="alert">Cannot reach the page.</span>';
            this.alertContainer.html(msg);
        }.bind(this)
    });
};