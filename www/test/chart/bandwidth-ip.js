
function current_ip_bandwidth_pie(id, service) {

  $('#' + id).easyPieChart({
    animate:100
  });

  var updateChart = function (percent) {
    $('#' + id).data('easyPieChart').update(percent);
    $('#' + id + " span").text(percent + "%");
    
  }


  

  var connect = function (service){
    var connection = new WebSocket('ws://localhost:9000', 'test');

    // When the connection is open, send some data to the server
    connection.onopen = function () {
      connection.send('Ping'); // Send the message 'Ping' to the server
    };

    // Log errors
    connection.onerror = function (error) {
      console.log('WebSocket Error ' + error);
    };

    // Log messages from the server
    connection.onmessage = function (e) {
      console.log('Server: ' + e.data);

      var percent = parseInt(e.data); 

      if(!isNaN(percent))
        updateChart(percent);
      

    };

  }
  connect(service);

  //setInterval(function(){updateChart(Math.round(Math.random() *(100)))}, 500); 

}



