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
#include <map>


class Websocket
{
public:
    void run();
    void start();
    void stop();
    void send(std::string websocket, std::string val);
    void addClient(std::string s, libwebsocket *);
    void delClient(std::string s, libwebsocket *);

    static Websocket* getInstance();


private:
    Websocket(); 
    Websocket(Websocket const&){};             // copy constructor
    // Websocket& operator=(Websocket const& w){};  // assignment operator
    static Websocket* _wInstance;


    bool running;
    pthread_t thread_websocket;
    std::map<std::string, std::set<libwebsocket *> > list_websockets_clients;
};

// websocket thread
void* th_websocket(void* data);


#endif