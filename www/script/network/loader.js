/**
 * Load the dispatcher of websocket data comming from the NDOP server.
 **/

if(typeof App != 'undefined'){
	dispatcher = new DataDispatcher(App.NDOPAddress);
}
