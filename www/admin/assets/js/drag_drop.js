// add the dataTransfer property for the drag and drop functions
$.event.props.push('dataTransfer');



$(document).ready(function() {

    var config = new LayoutConfig();

});

function LayoutConfig() {

    this.layout = [];

    // set callback to every objects we can drag and drop
    this.refreshDroppable();

    // set callback to every objects we can drop on
    this.refreshDropper(this.layout);

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

    // intial number of pages we can drop on
    this.nb_page = parseInt($('#nb_page').html()) || 0;

    // load the current layout stored in database in a js variable
    this.loadLayout();


}

LayoutConfig.prototype.refreshDroppable = function() {
    $('*[draggable="true"]').on({
        // on commence le drag
        dragstart: function(e) {
            $(this).css('opacity', '0.5');

            // on garde le texte en mémoire (A, B, C ou D)
            e.dataTransfer.setData('text', this.id);
        },
        // fin du drag (même sans drop)
        dragend: function() {
            $(this).css('opacity', '1');
        }
    });
}

LayoutConfig.prototype.refreshDropper = function(layout) {
    $('.page-dropper').on({

        drop: function(e) {
            e.preventDefault();
            var id = e.dataTransfer.getData('text');
            $('#' + this.id).html($('#' + id).html());

            console.log(layout)
            layout[parseInt(this.id.substr(4))] = parseInt(id.substr(7));
            console.log(layout)
        },

        dragover: function(e) {
            e.preventDefault();
        }
    })
}

LayoutConfig.prototype.addPage = function() {
    this.nb_page++;
    // console.log(this.nb_page)
    var html = "<div class='page thumbnail'>\
       <div class='legend_page'>Page " + this.nb_page + "</div>\
       <i id='suppr" + (this.nb_page - 1) + "' class='icon-remove suppr'></i>\
       <div class='page-dropper module' id='page" + (this.nb_page - 1) + "'>\
       " + $('#saveImage').html() + "\
       </div>\
       </div>";


    $('#add_page').before(html);

    this.refreshDropper(this.layout);
    this.refreshSupprCallback();
}

LayoutConfig.prototype.resizePagesContainer = function() {
    $('#pages').height(window.innerHeight - 100);
    $('#panel').height(window.innerHeight - 100);
}

LayoutConfig.prototype.saveConfig = function() {
    console.log(this.layout)
    var i = 0;
    var length = this.layout.length;

    console.log('len ' + i +'<' + length  + '=' + (i < length))

    while (i < length && this.layout[i] != null) {
        console.log(i + ' ' + length + ' ' + this.layout[i]);
        i++;
    }


    function success(data) {
        console.log('success ' + data)
    }

    if (i !== length) {
        console.log('manque des cases')
    } else {
        console.log(this.layout)

        $.ajax({
            type: "POST",
            url: "/admin/sql/save_config_layout.php",
            data: {
                'pages[]': this.layout
            },
            success: success,
            // dataType: dataType
        });
    }
}

LayoutConfig.prototype.supprPage = function(event) {
    var id = parseInt(this.id.substr(5));

    delete event.data.layout[id];
    event.data.layout.length--;
    console.log(id)
    $('#page' + id).html($('#saveImage').html());
}

LayoutConfig.prototype.refreshSupprCallback = function() {
    // callback on the 'save' button
    $('.suppr').click({
        layout: this.layout
    }, this.supprPage);
}

LayoutConfig.prototype.loadLayout = function() {
    function success(data){

    for (var i = 0; i < data.length; i++) {
        this.layout[parseInt(data[i].page)] = parseInt(data[i].id_module);
    };
    }
    $.ajax({
        type: "GET",
        url: "/admin/sql/get_config_layout.php",
        success: success.bind(this),
        dataType: 'json',
    });

};

LayoutConfig.prototype.clearConfig = function(){
    this.layout = [];
    $('#pageContainer').html('');
}