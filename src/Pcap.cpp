// Class header
#include <Pcap.hpp>
#include <Json.hpp>

// Library header
#include <pcap.h>
#include <time.h>

// packet analisys
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <net/ethernet.h>
#include <netinet/ether.h>
#include <netinet/if_ether.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
 
#include <fcntl.h>
#include <getopt.h>
#include <ifaddrs.h>
#include <netdb.h>
#include <pcap.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
#include <unistd.h>

#include <iostream>
#include <ostream>
#include <sstream>
#include <stack>
#include <ctime>
#include <bitset>
#include <string>


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

    speed_in = 0;
    speed_out = 0;
    speed_local = 0;

    p_size_in = 0;
    p_size_out = 0;
    p_size_local = 0;

    gettimeofday(&time_collect, NULL);
};

void Pcap::start()
{
    cout << "start" << endl;
    pthread_create( &thread_packet_grab, NULL, th_packet_grab, (void*) this);
};

void Pcap::stop()
{
    // struct in_addr addr;
    // addr.s_addr = net;
    // printf("NET: %s\n", inet_ntoa(addr));

    // addr.s_addr = mask;
    // printf("MASK: %s\n", inet_ntoa(addr));

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


        speed_in = p_size_in/diff;
        speed_out = p_size_out/diff;
        speed_local = p_size_local/diff;


        // update
        gettimeofday(&time_collect, NULL);
        p_number_tmp = p_number;
        p_size_tmp = p_size;


        p_size_in = 0;
        p_size_out = 0;
        p_size_local = 0;
    }

    // for (unsigned int i = 0; i < header->len; i++)
    //     cout << std::dec << packet[i];
    // cout << endl << endl;



    //u_int caplen = header->caplen; /* length of portion present from bpf  */
    //u_int length = header->len;    /* length of this packet off the wire  */
    struct ether_header *eptr;     /* net/ethernet.h                      */
    u_short ether_type;            /* the type of packet (we return this) */
    eptr = (struct ether_header *) packet;
    ether_type = ntohs(eptr->ether_type);

    // cout << p_number << " - eth: " << ether_ntoa((struct ether_addr*)eptr->ether_shost)
    //     << " " << ether_ntoa((struct ether_addr*)eptr->ether_dhost) << " ";

    

    bool bip = false;


    if (ether_type == ETHERTYPE_IP) {
            // cout << "(ip)";
            bip = true;
    } else  if (ether_type == ETHERTYPE_ARP) {
            // cout << "(arp)";
    } else  if (ether_type == ETHERTYPE_REVARP) {
            // cout << "(rarp)";
    } else {
            // cout << /"(?)";
    }

    // cout << " " << length << endl;

    if(bip)
        handler_ip(header, packet);

};

void Pcap::handler_ip(const struct pcap_pkthdr* pkthdr, const u_char* packet)
{
    const struct nread_ip* ip;      /* packet structure         */
    // const struct nread_tcp* tcp;    /* tcp structure            */
    // u_int length = pkthdr->len;     /* packet header length     */
    // u_int off;                      /* offset        */
    // u_int version;                  /* version       */
    // int len;                        /* length holder            */
    
    ip = (struct nread_ip*)(packet + sizeof(struct ether_header));
    // length -= sizeof(struct ether_header);
    // tcp = (struct nread_tcp*)(packet + sizeof(struct ether_header) + sizeof(struct nread_ip));

    // len     = ntohs(ip->ip_len); /* get packer length */
    // version = IP_V(ip);          /* get ip version    */

    // off = ntohs(ip->ip_off);

    string src(inet_ntoa(ip->ip_src));
    string dst(inet_ntoa(ip->ip_dst));

    // cout << (ip->ip_src.s_addr & 0xff) << "." << ((ip->ip_src.s_addr >> 8) & 0xff) << "." << ((ip->ip_src.s_addr >> 16) & 0xff) << "." << (ip->ip_src.s_addr >> 24);

    // cout << (mask & 0xff) << "." << ((mask >> 8) & 0xff) << "." << ((mask >> 16) & 0xff) << "." << (mask >> 24);

    if(((ip->ip_src.s_addr & mask) == net) && ((ip->ip_dst.s_addr & mask) == net))
    {
        // cout << "IN:" << src << " -> " << "IN:" << dst << endl;
        p_size_local += pkthdr->len;
    } else if(((ip->ip_src.s_addr & mask) == net) && !((ip->ip_dst.s_addr & mask) == net))
    {
        // cout << "IN:" << src << " -> " << "OUT:" << dst << endl;
        p_size_out += pkthdr->len;
    } else if(!((ip->ip_src.s_addr & mask) == net) && ((ip->ip_dst.s_addr & mask) == net))
    {
        // cout << "OUT:" << src << " -> " << "IN:" << dst << endl;
        p_size_in += pkthdr->len;
    } else
        cout << "OUT -> OUT ???????" << endl;



    // cout << "\t" << "IP: " << src << ":" << tcp->th_sport << " -> " 
    //     << dst << ":" << tcp->th_dport;

    // fprintf(stdout,
    // "tos %u len %u off %u ttl %u prot %u cksum %u ",
    // ip->ip_tos, len, off, ip->ip_ttl,
    // ip->ip_p, ip->ip_sum);

    // fprintf(stdout,"seq %u ack %u win %u ",
    // tcp->th_seq, tcp->th_ack, tcp->th_win);
    
};

void Pcap::packet_grab()
{
    pcap_t *handle;                 /* Session handle */
    char *dev;                      /* The device to sniff on */
    char errbuf[PCAP_ERRBUF_SIZE];  /* Error string */
    struct pcap_pkthdr header;      /* The header that pcap gives us */
    const u_char *packet;           /* The actual packet */


    /* Define the device */
    dev = pcap_lookupdev(errbuf);
    if (dev == NULL) {
        fprintf(stderr, "Couldn't find default device: %s\n", errbuf);
        return;
    }

    // cout << "Device : " << dev << endl;

    /* Find the properties for the device */
    if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1) {
        fprintf(stderr, "Couldn't get netmask for device %s: %s\n", dev, errbuf);
        net = 0;
        mask = 0;
    }

    

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
            // cout << "a" << endl;
            collect(packet, &header);
            // cout << "b" << endl;
        }
    }

    pcap_close(handle);
};

string Pcap::getInfo()
{
    Json s;

    s.add("Ko", speed/1024.0);
    s.add("loc_Ko", speed_local/1024.0);
    s.add("in_Ko", speed_in/1024.0);
    s.add("out_Ko", speed_out/1024.0);

    return s.toString();
};

void* th_packet_grab(void* data)
{
    Pcap *p = (Pcap*) data;

    cout << "Start Sniffing" << endl;
    
    p->packet_grab();

    return NULL;

};

