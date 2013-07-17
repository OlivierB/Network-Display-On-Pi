/**
 * BandwidthTextAjax class displaying bandwidth informations in a text format.
 * Data come from ajax request which gathers informations from the database.
 * @author Matrat Erwan
 **/

function BandwidthTextAjax(id, font_size) {

    // inheritance from BandwidthText
    BandwidthText.call(this, id, font_size);

    // inheritance from AjaxManager
    AjaxManager.call(this, id + '-alert');
}


// inheritance from AjaxManager
BandwidthTextAjax.prototype = Object.create(AjaxManager.prototype);

// inheritance from BandwidthText
BandwidthTextAjax.prototype.dataManager = BandwidthText.prototype.dataManager;



