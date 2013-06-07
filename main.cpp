#include <iostream>


// pcap lib
#include "include/pcap.hpp"
#include "include/Websocket.hpp"
#include <unistd.h>
#include <signal.h>

#include <libwebsockets.h>

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
    Websocket w;

    // Start listening
    p.start();
    w.start();

    // LOOP
    while(running == 1)
    {
        sleep(1);
        w.send(p.getInfo());
        // p.getInfo();  
    }
    
    // Stop
    p.stop();
    w.stop();

    return 0;
}