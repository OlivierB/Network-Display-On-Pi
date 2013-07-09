// Map creation in the div with id='map'
var IpMap = new IpLocationMapOffline('map-offline');


// Connection to the IP provider programm
IpMap.connect(dispatcher, 'iplist');

