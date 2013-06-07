// Class header
#include <Websocket.hpp>

// Library header
#include <libwebsockets.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#include <iostream>
#include <vector>
#include <string>



using namespace std;

// Clients list used in callback function
std::set<libwebsocket *> l_client;

// Callback function
static int callback_http(struct libwebsocket_context *context,
                         struct libwebsocket *wsi,
                         enum libwebsocket_callback_reasons reason, void *user,
                         void *in, unsigned long len)
{
    cout << ">>>>>>>>>>>>>>" << endl;
    switch (reason) {
        case LWS_CALLBACK_ESTABLISHED:
            cout << "connection established" << endl;
            l_client.insert(wsi);
            break;
        case LWS_CALLBACK_HTTP:
            cout << "HTTP" << endl;
            break;
        case LWS_CALLBACK_RECEIVE:
            cout << "RECEIVE - " << (char *) in << endl;
            break;
        case LWS_CALLBACK_CLOSED:
            cout << "CLOSE" << endl;
            l_client.erase(wsi);
        default:
            cout << "unhandled callback" << endl;
            break;
    }
    cout << "<<<<<<<<<<<<<<" << endl << endl;
    return 0;
};

Websocket::Websocket()
{
    running = true;
};

void Websocket::start()
{
    cout << "start" << endl;
    pthread_create( &thread_websocket, NULL, th_websocket, (void*) this);
};

void Websocket::stop()
{
    running = false;
};

void Websocket::run()
{
    // list of supported protocols and callbacks
    static struct libwebsocket_protocols protocols[] = {
        /* first protocol must always be HTTP handler */
        {
            "bandwidth",        /* name */
            callback_http,      /* callback */
            0,                  /* max frame size / rx buffer */
        },
        { NULL, NULL, 0 }       /* terminator */
    };

    // Websocket context
    struct libwebsocket_context *context;
    // param managment
    struct lws_context_creation_info info;

    // init
    memset(&info, 0, sizeof info);
    info.protocols = protocols;             // protocol for callback
    info.ssl_cert_filepath = NULL;          // SSL info
    info.ssl_private_key_filepath = NULL;   // SSL info
    info.gid = -1;                          // access right
    info.uid = -1;
    info.options = 0;                       // no option
    info.port = 9000;                       // listen port
    info.extensions = libwebsocket_get_internal_extensions();

    // create the websocket context
    context = libwebsocket_create_context(&info);
    
    // error
    if (context == NULL) {
        fprintf(stderr, "libwebsocket init failed\n");      
        return;
    }
    
    cout << "starting server..." << endl;
    

    while (running) {

        libwebsocket_service(context, 50);

    }
    
    // clean
    libwebsocket_context_destroy(context);
};


void Websocket::send(string val)
{
    for (std::set< libwebsocket *>::iterator it=l_client.begin(); it!=l_client.end(); ++it)
        libwebsocket_write(*it, (unsigned char*) val.c_str(), val.length(), LWS_WRITE_TEXT);
};


void* th_websocket(void* data)
{
    Websocket *w = (Websocket*) data;

    cout << "Start Websocket" << endl;
    
    w->run();

    return NULL;
};



