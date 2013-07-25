function Widget(data, id) {
    this.dom_id = ++Widget.number_widgets;

    if (data) {
        this.loadFromData(data);
    } else {
        this.loadFromDatabase(id);
    }

    this.loadParameter();
}

Widget.number_widgets = 0;

Widget.prototype.loadFromDatabase = function(id) {
    function success(data) {
        data = data[0];
        this.db_id = parseInt(id);
        this.name = data['widget_name'];
        this.folder_name = data['folder_name'];

        this.x = 0;
        this.y = 0;
        this.width = 1;
        this.height = 1;

        this.current_id_parameter_set = parseInt(data['set_id']);
    }
    $.ajax({
        type: "GET",
        url: "../../../admin/sql/get_widget.php?id=" + id,
        success: success.bind(this),
        dataType: 'json',
        async: false
    });
};

Widget.prototype.loadFromData = function(data) {
    this.db_id = parseInt(data['id_widget']);
    this.name = data['widget_name'];
    this.folder_name = data['folder_name'];

    this.x = parseInt(data['x']);
    this.y = parseInt(data['y']);
    this.width = parseInt(data['width']);
    this.height = parseInt(data['height']);

    this.current_id_parameter_set = parseInt(data['id_widget_parameter_set']);
};

// Add a widget in the DOM, if an empty name is provided a blank widget is created
Widget.prototype.addToDOM = function(container) {

    var html = '<div class="span' + this.width + ' line" style="background-color:">';

    if (this.name) {
        html += "<div class='module chosen_widget' id='chosen_widget_" + this.dom_id + "'>";
        html += "   <img src='/widgets/" + this.folder_name + "/thumbnail.png'>";
        html += "</div>";
    }
    html += '</div>';
    container.append(html);
};

// add the panel to configure the widget corresponding to id
Widget.prototype.loadParameter = function() {
    function success(data) {
        // var widget = data[0];
        this.parameter_set = [];
        for (var i = 0; i < data.length; i++) {
            this.parameter_set.push({
                'id': data[i]['set_id'],
                'name': data[i]['set_name']
            });
        }
    }
    $.ajax({
        type: "GET",
        url: "../../../admin/sql/get_widget.php?id=" + this.db_id,
        success: success.bind(this),
        dataType: 'json',
        async: false
    });
};

Widget.prototype.addParameterPanelToDOM = function(container) {

    var html = "<legend>" + this.name + "</legend>\
            <div>\
                <input class='input-mini' type='number' min='0' max='11' id='x' value=" + this.x + ">\
                <label for='x'>x (0-11)</label>\
            </div>\
            <div>\
                <input class='input-mini' type='number' min='0' max='1' id='y' value=" + this.y + "> \
                <label for='y'>y (0-1)</label>\
            </div>\
            <div>\
                <input class='input-mini' type='number' min='1' max='12' id='width' value=" + this.width + ">\
                <label for='width'>width (1-12)</label>\
            </div>\
            <div>\
                <input class='input-mini'type='number' min='1' max='2' id='height' value=" + this.height + ">\
                <label for='height'>height (1-2)</label>\
            </div>\
            <div>\
                <select class='input-small' id='parameter_set'>";

    var selected;
    for (var i = 0; i < this.parameter_set.length; i++) {
        if (parseInt(this.parameter_set[i]['id']) == this.current_id_parameter_set) {
            selected = "selected='selected'";
        } else {
            selected = "";
        }
        html += "   <option value='" + this.parameter_set[i]['id'] + "' " + selected + ">" + this.parameter_set[i]['name'] + "</option>";
    }

    html += "   </select>\
                <label for='parameter_set'>Parameters</label>\
            </div>\
            <div>\
                <button id='add_widget_btn' class='btn'>Submit</button>\
                <button id='delete_widget_btn' class='btn'>Delete</button>\
            </div>";
    container.html(html);


};

Widget.prototype.setBorder = function() {
    $('#chosen_widget_' + this.dom_id).addClass('selected_module');
};

Widget.prototype.clone = function() {
    return $.extend(true, {}, this);
};