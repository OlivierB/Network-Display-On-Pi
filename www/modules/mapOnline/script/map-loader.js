// Map creation in the div with id='map'
var IpMap = new IpLocationMapOnline('map-online');


// Connection to the IP provider programm
IpMap.connect(dispatcher, 'iplist');

