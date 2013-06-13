// Map creation in the div with id='map'
var IpMap = new IpLocationMap('map');

// Add the location of our IP
IpMap.addPointFromIP('', 'blue');

// Connection to the IP provider programm
IpMap.connect(App.serverAddress, App.ipListProtocol);

