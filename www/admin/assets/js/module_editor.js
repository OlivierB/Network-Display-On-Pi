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

    this.container_parameter = $('#widget_param');
    this.current_widget = -1;

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



    // this.refreshSupprCallback();

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
};

ModuleConfig.prototype.refreshDropper = function(that) {
    $('#module_content').on({
        drop: function(e) {
            e.preventDefault();
            // get the id of the module without the 'module_' part
            var id = parseInt(e.dataTransfer.getData('text').substr(7));

            var widget = new Widget(null, id);

            that.setFocus(widget);

            that.current_widget_id_dom = -1;
            that.new_widget = widget;

            that.setPendingMode(true);

        },

        dragover: function(e) {
            e.preventDefault();
        }
    });
};

ModuleConfig.prototype.refreshOnClickChosenWidget = function() {
    $('.chosen_widget').click({
        that: this
    }, this.clickOnChosenWidget);
};

ModuleConfig.prototype.resizePagesContainer = function() {
    $('#pages').height(window.innerHeight - 100);
    $('#panel').height(window.innerHeight - 100);
};

ModuleConfig.prototype.refreshSubmitWidgetCallback = function() {
    // callback ont the submit button for the widget
    $('#add_widget_btn').click(this.addWidget.bind(this));
};

ModuleConfig.prototype.refreshDeleteWidgetCallback = function() {
    // callback ont the submit button for the widget
    $('#delete_widget_btn').click(this.supprWidget.bind(this));
};

// save the config in the database
ModuleConfig.prototype.saveConfig = function() {

    this.module_name = $('#module_name').val();
    this.module_description = $('#module_description').val();


    if (this.module_name === '') {
        alert('You must define a name.');
    } else if (this.module_description === '') {
        alert('You must define a description.');
    } else {
        $.ajax({
            type: "POST",
            url: "../../../admin/sql/save_config_module.php",
            data: {
                module: JSON.stringify(this.layout),
                'id': this.id_module,
                'name': this.module_name,
                'description': this.module_description
            },
            success: success.bind(this)
        });
    }

    function success(code_html, statut) {
        this.id_module = parseInt(code_html);
    }

};


ModuleConfig.prototype.loadModule = function() {
    var id_str = $('#id_module').val();

    if (id_str) {
        this.id_module = parseInt(id_str);
    }


    function success(data) {
        // we fill our variable with the response of the ajax request
        if (data.length > 0 && data[0]['id']) {
            for (var i = 0; i < data.length; i++) {
                var widget = new Widget(data[i]);
                this.layout[widget.dom_id] = widget;
            }
        }

        this.addAllWidgetsToDOM();
    }
    $.ajax({
        type: "GET",
        url: "../../../admin/sql/get_config_module.php?id=" + this.id_module,
        success: success.bind(this),
        dataType: 'json'
    });


};

ModuleConfig.prototype.clearConfig = function() {
    // clear our variable and the dom from the previsous layout config
    this.layout = [];
    this.clearModuleContent();
};

ModuleConfig.prototype.clearModuleContent = function() {
    $('#first_line').html('');
    $('#first_line').attr('class', 'height-half');
    $('#second_line').html('');
    $('#second_line').show();

    this.container = $('#first_line');

    this.current_x = 0;
    this.current_y = 0;
};

ModuleConfig.prototype.addAllWidgetsToDOM = function() {
    function compare(a, b) {
        if (a.y < b.y) {
            return -1;
        } else if (a.y > b.y) {
            return 1;
        } else {
            if (a.x > b.x) {
                return 1;
            } else {
                return -1;
            }
        }
    }
    var layout_cpy = this.layout.slice();
    layout_cpy.sort(compare);

    for (var widget_id_dom in layout_cpy) {
        var widget = layout_cpy[widget_id_dom];

        // if the widget is set to be on the second line then every following 
        // widgets willl be on the second line
        if (widget.y == 1 && this.current_y === 0) {
            this.container = $('#second_line');
            this.current_x = 0;
            this.current_y = 1;
        }

        // if the widget is set to take the whole height, the second line doesn't exists anymore
        if (widget.height == 2) {
            $('#second_line').hide();
            $('#first_line').attr('class', 'height-full');
        }

        // if there is a blank before the widget, we fill it with nothing
        if (widget.x > this.current_x) {
            var diff = widget.x - this.current_x;
            var blank = new Widget({
                width: diff
            });
            blank.addToDOM(this.container);
            this.current_x += diff;
        }
        widget.addToDOM(this.container);
        this.current_x += widget.width;
    }
    this.refreshOnClickChosenWidget();
};


// add a widget to the local variable from the form in the page
ModuleConfig.prototype.addWidget = function() {

    var x, y, width, height;
    var correct_numbers = true;

    // check if our inputs are really number
    if ((x = this.checkInput('x')) >= 0 && (y = this.checkInput('y')) >= 0 &&
        (width = this.checkInput('width')) > 0 && (height = this.checkInput('height')) > 0) {

        if (!(0 <= x <= 11)) {
            alert('X must be between 0 and 11.');
            correct_numbers = false;
        }

        if (!(0 <= y <= 1)) {
            alert('Y must be between 0 and 1.');
            correct_numbers = false;
        }

        if (!(1 <= width <= 12)) {
            alert('Width must be between 1 and 12.');
            correct_numbers = false;
        }

        if (!(1 <= height <= 2)) {
            alert('Height must be between 1 and 2.');
            correct_numbers = false;
        }

        if (correct_numbers) {
            var widget;
            var widget_cpy;

            if (this.current_widget_id_dom > 0) {
                // if it's a move of a widget
                widget = this.layout[this.current_widget_id_dom];
                widget_cpy = widget.clone();
                delete this.layout[this.current_widget_id_dom];
            } else {
                // if it's a new widget
                widget = this.new_widget;
            }

            widget.x = x;
            widget.y = y;
            widget.width = width;
            widget.height = height;
            widget.current_id_parameter_set = this.checkInput('parameter_set');


            if (this.checkOverlapping(widget)) {
                // if the position of the widget is correct, we add it to our layout
                this.layout[widget.dom_id] = widget;
                this.clearModuleContent();
                this.addAllWidgetsToDOM();
                this.setFocus(widget);
                // that.current_widget_id_dom = widget.id_dom;
                if (this.current_widget_id_dom <= 0) {
                    this.current_widget_id_dom = widget.dom_id;
                }
            } else {
                alert('Your widget is overlapping an existing widget or is out of bound.');
                if (this.current_widget_id_dom > 0) {
                    // if it was a move and not a creation, we put the widget back to its previous place
                    this.layout[widget.dom_id] = widget_cpy;
                    this.clearModuleContent();
                    this.addAllWidgetsToDOM();
                    this.setFocus(widget_cpy);
                }
            }

        }

    } else {
        alert('Every inputs must be filled with number.');
    }
};

ModuleConfig.prototype.checkInput = function(id) {
    var val = $('#' + id).val();
    if (!isNaN(parseInt(val))) {
        return parseInt(val);
    } else {
        return -1;
    }
};

ModuleConfig.prototype.checkOverlapping = function(widget_to_check) {

    for (var id_dom in this.layout) {
        var widget = this.layout[id_dom];
        // every height must be equal, there can't be both a full and half height widgets at the same time
        if (widget_to_check.height != widget.height) {
            return false;
        }
        // check overlap
        if ((widget.x + widget.width) > widget_to_check.x && widget.x < (widget_to_check.x + widget_to_check.width) && (widget.y + widget.height) > widget_to_check.y && widget.y < (widget_to_check.y + widget_to_check.height)) {
            return false;
        }
    }

    // check out of bounds
    if ((widget_to_check.x + widget_to_check.width) > 12 || (widget_to_check.y + widget_to_check.height) > 2) {
        return false;
    }

    return true;
};

ModuleConfig.prototype.clickOnChosenWidget = function(event) {

    var that = event.data.that;
    var id = parseInt(this.id.substr(14));
    that.setFocus(that.layout[id]);

    that.current_widget_id_dom = id;
};

ModuleConfig.prototype.setFocus = function(widget) {
    widget.addParameterPanelToDOM(this.container_parameter);
    this.refreshSubmitWidgetCallback();
    this.refreshDeleteWidgetCallback();

    $('.selected_module').removeClass('selected_module');
    widget.setBorder();

    this.setPendingMode(false);
};

ModuleConfig.prototype.supprWidget = function() {
    if (this.current_widget_id_dom in this.layout) {
        delete this.layout[this.current_widget_id_dom];
        this.clearModuleContent();
        this.addAllWidgetsToDOM();
    }
    this.container_parameter.html('');
    this.setPendingMode(false);
};

ModuleConfig.prototype.setPendingMode = function(pendingMode) {
    if (pendingMode) {
        $('.line').css('opacity', 0.3);
    } else {
        $('.line').css('opacity', 1);
    }

};