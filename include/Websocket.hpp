#ifndef WEBSOCKET_HPP
#define WEBSOCKET_HPP

/**
 * Websocket
 * 
 * 
 */

// Library header
#include <pthread.h>
#include <libwebsockets.h>

#include <string>
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