#include <iostream>

#include <pcap.h>
#include <netinet/if_ether.h> /* includes net/ethernet.h */
#include <ctime>
#include <time.h>
#include <ostream>
#include <sstream>
#include <stack>

#include "../include/pcap.hpp"

using namespace std;


Pcap::Pcap()
{
    running = true;

    speed = 0;
    p_number = 0;
    p_size = 0;
    p_number_tmp = 0;
    p_size_tmp = 0;
    update_MS = 1000;
    gettimeofday(&time_collect, NULL);
};

void Pcap::start()
{
    cout << "start" << endl;
    pthread_create( &thread_packet_grab, NULL, th_packet_grab, (void*) this);
};

void Pcap::stop()
{
    running = false;
    pthread_join(thread_packet_grab, NULL);
    cout << "Stop" << endl;
};

void Pcap::collect(const u_char *packet, struct pcap_pkthdr * header)
{
    p_number++;
    p_size += header->len;


    gettimeofday(&time_collect2, NULL);

    long double diff = ((time_collect2.tv_sec*1000)+(time_collect2.tv_usec/1000)) - ((time_collect.tv_sec*1000)+(time_collect.tv_usec/1000));

    if (update_MS < diff)
    {
        diff /= 1000.0; // diff in Sec
        speed = (p_size-p_size_tmp)/diff;

        // update
        gettimeofday(&time_collect, NULL);
        p_number_tmp = p_number;
        p_size_tmp = p_size;
    }

    // struct ether_header *eptr;
    // u_char *ptr;
    // eptr = (struct ether_header *) packet;
    // ptr = eptr->ether_dhost;
    // int i = ETHER_ADDR_LEN;
    // printf(" Destination Address:  ");
    // do{
    //     printf("%s%x",(i == ETHER_ADDR_LEN) ? " " : ":",*ptr++);
    // }while(--i>0);
    // printf("\n");

};

void Pcap::packet_grab()
{
    pcap_t *handle;                 /* Session handle */
    char *dev;                      /* The device to sniff on */
    char errbuf[PCAP_ERRBUF_SIZE];  /* Error string */
    bpf_u_int32 mask;               /* Our netmask */
    bpf_u_int32 net;                /* Our IP */
    struct pcap_pkthdr header;      /* The header that pcap gives us */
    const u_char *packet;           /* The actual packet */


    /* Define the device */
    dev = pcap_lookupdev(errbuf);
    if (dev == NULL) {
        fprintf(stderr, "Couldn't find default device: %s\n", errbuf);
        return;
    }

    cout << "Device : " << dev << endl;

    /* Find the properties for the device */
    if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1) {
        fprintf(stderr, "Couldn't get netmask for device %s: %s\n", dev, errbuf);
        net = 0;
        mask = 0;
    }
    // cout << "IP Address : " << net << "/" << mask << endl;

    /* Open the session in promiscuous mode */
    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);

    if (handle == NULL) {
        fprintf(stderr, "Couldn't open device %s: %s\n", dev, errbuf);
        return;
    }

    gettimeofday(&time_collect, NULL);

    while(running)
    {
        packet = pcap_next(handle, &header);
        if (packet != NULL)
        {
            collect(packet, &header);
        }
    }

    pcap_close(handle);
};

string Pcap::getInfo()
{
    string var;
    ostringstream convert;
    convert << "{ \"o\" : " << speed << ", \"Ko\" : " << speed/1000 << ", \"Mo\" : " << speed/(1000*1000) << " }";
    var = convert.str(); 
    return var;
};

void* th_packet_grab(void* data)
{
    Pcap *p = (Pcap*) data;

    cout << "Start Sniffing" << endl;
    
    p->packet_grab();

    return NULL;

};
