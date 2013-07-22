// add the dataTransfer property for the drag and drop functions
$.event.props.push('dataTransfer');



$(document).ready(function() {

    var config = new LayoutConfig();

});

function LayoutConfig() {

    this.layout = [];
    // load the current layout stored in database in a this layout
    this.loadLayout();

    // intial number of pages we can drop on
    this.nb_page = parseInt($('#nb_page').html());

    // set callback to every objects we can drag and drop
    this.refreshDroppable();

    // set callback to every objects we can drop on
    this.refreshDropper(this);

    // resize the height of the container to the height of the window
    this.resizePagesContainer();

    // set the callback to keep the height when the window is resized
    $(window).resize(this.resizePagesContainer.bind(this));

    // callback on the 'addpage' button
    $('#add_page').click(this.addPage.bind(this));

    // callback on the 'save' button
    $('#save').click(this.saveConfig.bind(this));

    // callback on the 'clear' button
    $('#clear').click(this.clearConfig.bind(this));

    this.refreshSupprCallback();


}

LayoutConfig.prototype.refreshDroppable = function() {
    $('*[draggable="true"]').on({

        dragstart: function(e) {
            $(this).css('opacity', '0.5');
            // recored the id of the dragged module
            e.dataTransfer.setData('text', this.id);
        },
        // end of the drag (even without drop)
        dragend: function() {
            $(this).css('opacity', '1');
        }
    });
};

LayoutConfig.prototype.refreshDropper = function(that) {
    $('.page-dropper').on({

        drop: function(e) {
            e.preventDefault();
            // get the id of the module
            var id = e.dataTransfer.getData('text');

            // set the new module to the correct place
            $('#' + this.id).html($('#' + id).html());

            that.layout[parseInt(this.id.substr(4))] = parseInt(id.substr(7));

        },

        dragover: function(e) {
            e.preventDefault();
        }
    })
};
LayoutConfig.prototype.addPage = function() {
    this.nb_page++;
    var html = "<div class='page thumbnail'>\
       <div class='legend_page'>Page " + this.nb_page + "</div>\
       <i id='suppr" + (this.nb_page - 1) + "' class='icon-remove suppr'></i>\
       <div class='page-dropper module' id='page" + (this.nb_page - 1) + "'>\
       " + $('#saveImage').html() + "\
       </div>\
       </div>";

    $('#page-container').append(html);

    // refresh the drag and drop callbacks
    this.refreshDropper(this);
    this.refreshSupprCallback();
};

LayoutConfig.prototype.resizePagesContainer = function() {
    $('#pages').height(window.innerHeight - 100);
    $('#panel').height(window.innerHeight - 100);
};

// save the config in the database
LayoutConfig.prototype.saveConfig = function() {

    var nb = 0;
    var is_null = false;
    for (var elm in this.layout) {
        // we check if the recorded pages are 0, 1, 2, ...
        if (elm != nb) {
            is_null = true;
        }
        nb++;
    }

    // if there is a blank page between the filled page
    if (is_null) {
        alert("You can't let blank page.");
    } else {
        $.ajax({
            type: "POST",
            url: "/admin/sql/save_config_layout.php",
            data: {
                'pages[]': this.layout

            },
            success: function() {
                alert('Layout saved.');
            }
        });
    }
};

LayoutConfig.prototype.supprPage = function(event) {
    var id = parseInt(this.id.substr(5));
    var that = event.data.that;

    // erase the page from the layout variable and from the dom
    if (id in that.layout) {
        delete that.layout[id];
        // a default image is stored in the page
        $('#page' + id).html($('#saveImage').html());
    }
};

LayoutConfig.prototype.refreshSupprCallback = function() {
    // callback on the 'save' button
    $('.suppr').click({
        that: this
    }, this.supprPage);
};

LayoutConfig.prototype.loadLayout = function() {
    function success(data) {

        // we fill our variabe with the response of the ajax request
        for (var i = 0; i < data.length; i++) {
            this.layout[parseInt(data[i].page)] = parseInt(data[i].id_module);
        }
    }
    $.ajax({
        type: "GET",
        url: "/admin/sql/get_config_layout.php",
        success: success.bind(this),
        dataType: 'json'
    });

};

LayoutConfig.prototype.clearConfig = function() {
    // clear our variable and the dom from the previsous layout config
    this.layout = [];
    $('#page-container').html('');
    this.nb_page = 0;
};