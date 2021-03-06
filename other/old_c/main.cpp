// Class header
#include <Pcap.hpp>
#include <Websocket.hpp>
#include <Json.hpp>
#include <Update.hpp>
#include <Monitoring.hpp>


// Library header
#include <unistd.h>
#include <signal.h>
#include <libwebsockets.h>

#include <iostream>
#include <vector>
#include <string>


using namespace std;


int running = 1;

void sig_handler(int signo)
{
    if (signo == SIGINT)
    {
        running = 0;
        printf("received SIGINT ... stopping\n");
    } 
}



int main()
{
    // int argc, char **argv
    if (signal(SIGINT, sig_handler) == SIG_ERR)
        printf("\ncan't catch SIGINT\n");
    
    cout << "Sniffing program" << endl;
    cout << " - pcap lib" << endl;
    cout << " - websocket" << endl;
    cout << " - mysql connector" << endl;
    cout << "----------------------------" << endl;

    // Var
    Pcap p;
    Monitoring m;
    Update u;
    u.set(p);

    // Start listening
    p.start();
    Websocket::getInstance()->start();

    // LOOP
    while(running == 1)
    {
        sleep(1);
        u.update();
        // p.getInfo();  
        m.getCpu();
    }
    
    // Stop
    p.stop();
    Websocket::getInstance()->stop();

    return 0;
}