// Map creation in the div with id='map'
if(App.offline)
	var IpMap = new IpLocationMapOffline('map');
else
	var IpMap = new IpLocationMapOnline('map');

// Connection to the IP provider programm
IpMap.connect(dispatcher, 'iplist');

