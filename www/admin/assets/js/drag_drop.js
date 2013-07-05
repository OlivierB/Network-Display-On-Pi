// add the dataTransfer property for the drag and drop functions
$.event.props.push('dataTransfer');



$(document).ready(function() {

    var config = new LayoutConfig();

});

function LayoutConfig() {

    this.layout = [];

    // intial number of pages we can drop on
    this.nb_page = parseInt($('#nb_page').html());

    this.nb_module_chosen = this.nb_page;
    this.truc = 5;
    console.log(this.nb_module_chosen)

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

LayoutConfig.prototype.refreshDropper = function(that) {
    $('.page-dropper').on({

        drop: function(e) {
            e.preventDefault();
            var id = e.dataTransfer.getData('text');
            $('#' + this.id).html($('#' + id).html());

            
            if(that.layout[parseInt(this.id.substr(4))] == null){
                that.nb_module_chosen++;
                console.log('dop ' + that.nb_module_chosen)
            }
            that.layout[parseInt(this.id.substr(4))] = parseInt(id.substr(7));
            
            console.log(that.layout)
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


    $('#pageContainer').append(html);

    this.refreshDropper(this);
    this.refreshSupprCallback();
}

LayoutConfig.prototype.resizePagesContainer = function() {
    $('#pages').height(window.innerHeight - 100);
    $('#panel').height(window.innerHeight - 100);
}

LayoutConfig.prototype.saveConfig = function() {
    var i = 0;
    var length = this.layout.length;

    console.log(this.layout)
    while (i < length && this.layout[i] != null) {
        i++;
    }
    var nb = 0;
    var is_null = false;
    for(var elm in this.layout){
        console.log('elm ' + elm);
        if(elm!=nb){
            is_null = true;
        }
        
        nb++;
        
    }
    console.log('l ' + is_null + ' ' + this.nb_module_chosen + ' ' + nb)



    if (nb !== this.nb_module_chosen || is_null) {
        alert("You can't let blank page.")
    } else {
        $.ajax({
            type: "POST",
            url: "/admin/sql/save_config_layout.php",
            data: {
                'pages[]': this.layout,
                success: function(){
                    alert('Layout saved');
                }
            },
        });
    }
}

LayoutConfig.prototype.supprPage = function(event) {
    var id = parseInt(this.id.substr(5));
    var that = event.data.that;
    if(that.layout[id] != null){
        delete that.layout[id];
        that.nb_module_chosen--;
        console.log('mod ch ' + that.nb_module_chosen)
        $('#page' + id).html($('#saveImage').html());
    }
    
    
}

LayoutConfig.prototype.refreshSupprCallback = function() {
    // callback on the 'save' button
    $('.suppr').click({
        that: this
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