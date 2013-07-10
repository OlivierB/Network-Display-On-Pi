// add the dataTransfer property for the drag and drop functions
$.event.props.push('dataTransfer');


$(document).ready(function() {

    var config = new ModuleConfig();

});


function ModuleConfig() {

    this.layout = [];
    // load the current layout stored in database in a this layout
    this.loadModule();

    this.container = $('#first_line');
    this.current_x = 0;
    this.current_y = 0;

    // set callback to every objects we can drag and drop
    this.refreshDroppable();

    // set callback to every objects we can drop on
    this.refreshDropper(this);

    // resize the height of the container to the height of the window
    this.resizePagesContainer();

    // set the callback to keep the height when the window is resized
    $(window).resize(this.resizePagesContainer.bind(this));

    // callback on the 'save' button
    $('#save').click(this.saveConfig.bind(this));

    // callback on the 'clear' button
    $('#clear').click(this.clearConfig.bind(this));

    this.refreshSupprCallback();


}

ModuleConfig.prototype.refreshDroppable = function() {
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
}

// TO CHANGE
ModuleConfig.prototype.refreshDropper = function(that) {
    $('.widget-dropper').on({

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
}



ModuleConfig.prototype.resizePagesContainer = function() {
    $('#pages').height(window.innerHeight - 100);
    $('#panel').height(window.innerHeight - 100);
}

// save the config in the database
ModuleConfig.prototype.saveConfig = function() {

    // TODO
}

ModuleConfig.prototype.supprWidget = function(event) {
    // TODO


}

ModuleConfig.prototype.refreshSupprCallback = function() {
    // callback on the 'save' button
    $('.suppr').click({
        that: this
    }, this.supprWidget);
}

ModuleConfig.prototype.loadModule = function() {

    this.id_module = parseInt($('#id_module').val());
    console.log(this.id_module)

    function success(data) {
        // we fill our variable with the response of the ajax request
        console.log(data);
        for(var i = 0; i < data.length; i++){
            var widget = data[i];
            this.layout.push(widget);
            console.log(widget['name'])
        }

        this.addAllWidget();
    }
    $.ajax({
        type: "GET",
        url: "/admin/sql/get_config_module.php?id="+this.id_module,
        success: success.bind(this),
        dataType: 'json',
    });


};

ModuleConfig.prototype.clearConfig = function() {
    // clear our variable and the dom from the previsous layout config
    this.layout = [];
    $('#module_content').html('');
}

ModuleConfig.prototype.addAllWidget = function(){

    for (var i = 0; i < this.layout.length; i++) {
        var widget = this.layout[i];

        // if the widget is set to be on the second line then every following 
        // widgets willl be on the second line
        if(widget.y == 1 && this.current_y == 0){
            this.container = $('#second_line');
            this.current_x = 0;
            this.current_y = 1;
        }

        // if the widget is set to take the whole height, the second line doesn't exists anymore
        if(widget.height == 2){
            $('#second_line').hide();
            $('#first_line').attr('class', 'height-full');
        }

        // if there is a blank before the widget, we fill it with nothing
        if(widget.x > this.current_x){
            var diff = widget.x - this.current_x;
            this.addWidget('', diff, '');
        }
        this.addWidget(widget['name'], widget['width'], widget['folder_name'], widget['id']);
        this.current_x += parseInt(widget.width);
    };
}

ModuleConfig.prototype.addWidget = function(name, width, folder, id){
    console.log(name + width);
    var html = '<div class="span'+ width +' line" style="background-color:">';

    if(name != ''){
        html += "<div class='module' id='widget_"+id+"'>";
        html += "   <div class='legend'>"+name+"</div>";
        html += "   <img src='/widgets/"+folder+"/thumbnail.png'>";
        html += "</div>";
    }
    html += '</div>';

    this.container.append(html);
}