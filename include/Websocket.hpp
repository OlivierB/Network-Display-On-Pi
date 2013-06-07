#ifndef WEBSOCKET_HPP
#define WEBSOCKET_HPP

/**
 * Websocket
 * 
 * 
 */

#include <pcap.h>
#include <pthread.h>

#include <string>

#include <libwebsockets.h>
#include <set>

class Websocket
{
public:
    Websocket();
    void run();
    void start();
    void stop();
    void send(std::string val);

private:
	bool running;
	pthread_t thread_websocket;

};

// websocket thread
void* th_websocket(void* data);


#endif