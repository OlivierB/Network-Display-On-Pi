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


struct nread_ip {
    u_int8_t        ip_vhl;          /* header length, version    */
#define IP_V(ip)    (((ip)->ip_vhl & 0xf0) >> 4)
#define IP_HL(ip)   ((ip)->ip_vhl & 0x0f)
    u_int8_t        ip_tos;          /* type of service           */
    u_int16_t       ip_len;          /* total length              */
    u_int16_t       ip_id;           /* identification            */
    u_int16_t       ip_off;          /* fragment offset field     */
#define IP_DF 0x4000                 /* dont fragment flag        */
#define IP_MF 0x2000                 /* more fragments flag       */
#define IP_OFFMASK 0x1fff            /* mask for fragmenting bits */
    u_int8_t        ip_ttl;          /* time to live              */
    u_int8_t        ip_p;            /* protocol                  */
    u_int16_t       ip_sum;          /* checksum                  */
    struct  in_addr ip_src;          /* source address   */ 
    struct  in_addr ip_dst;          /* dest address   */
};

struct nread_tcp {
    u_short th_sport; /* source port            */
    u_short th_dport; /* destination port       */
    u_short th_seq;   /* sequence number        */
    u_short th_ack;   /* acknowledgement number */
#if BYTE_ORDER == LITTLE_ENDIAN
    u_int th_x2:4,    /* (unused)    */
    th_off:4;         /* data offset */
#endif
#if BYTE_ORDER == BIG_ENDIAN
    u_int th_off:4,   /* data offset */
    th_x2:4;          /* (unused)    */
#endif
    u_char th_flags;
#define TH_FIN 0x01
#define TH_SYN 0x02
#define TH_RST 0x04
#define TH_PUSH 0x08
#define TH_ACK 0x10
#define TH_URG 0x20
#define TH_ECE 0x40
#define TH_CWR 0x80
    u_short th_win; /* window */
    u_short th_sum; /* checksum */
    u_short th_urp; /* urgent pointer */
};

u_char* ip_handler(u_char *args, const struct pcap_pkthdr* pkthdr, const u_char* packet)
{
    const struct nread_ip* ip;   /* packet structure         */
    const struct nread_tcp* tcp; /* tcp structure            */
    u_int length = pkthdr->len;  /* packet header length  */
    u_int off;                   /* offset, version       */
    //u_int version;
    int len;                        /* length holder         */
    
    ip = (struct nread_ip*)(packet + sizeof(struct ether_header));
    length -= sizeof(struct ether_header);
    tcp = (struct nread_tcp*)(packet + sizeof(struct ether_header) + sizeof(struct nread_ip));

    len     = ntohs(ip->ip_len); /* get packer length */
    //version = IP_V(ip);          /* get ip version    */

    off = ntohs(ip->ip_off);

    string src(inet_ntoa(ip->ip_src));
    string dst(inet_ntoa(ip->ip_dst));


    cout << "\t" << "IP: " << src << ":" << tcp->th_sport << " -> " 
        << dst << ":" << tcp->th_dport;


    // cout << " tos " <<  ip->ip_tos << " len " << len << " off " << off << " ttl " << ip->ip_ttl << " prot " << ip->ip_p << " cksun " << ip->ip_sum; 

    fprintf(stdout,
    "tos %u len %u off %u ttl %u prot %u cksum %u ",
    ip->ip_tos, len, off, ip->ip_ttl,
    ip->ip_p, ip->ip_sum);

    fprintf(stdout,"seq %u ack %u win %u ",
    tcp->th_seq, tcp->th_ack, tcp->th_win);
    

    cout << endl;

    return NULL;
}


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

        // update
        gettimeofday(&time_collect, NULL);
        p_number_tmp = p_number;
        p_size_tmp = p_size;
    }

    // for (unsigned int i = 0; i < header->len; i++)
    //     cout << std::dec << packet[i];
    // cout << endl << endl;




    //u_int caplen = header->caplen; /* length of portion present from bpf  */
    u_int length = header->len;    /* length of this packet off the wire  */
    struct ether_header *eptr;     /* net/ethernet.h                      */
    u_short ether_type;            /* the type of packet (we return this) */
    eptr = (struct ether_header *) packet;
    ether_type = ntohs(eptr->ether_type);

    cout << p_number << " - eth: " << ether_ntoa((struct ether_addr*)eptr->ether_shost)
        << " " << ether_ntoa((struct ether_addr*)eptr->ether_dhost) << " ";

    bool bip = false;

    if (ether_type == ETHERTYPE_IP) {
            cout << "(ip)";
            bip = true;
    } else  if (ether_type == ETHERTYPE_ARP) {
            cout << "(arp)";
    } else  if (ether_type == ETHERTYPE_REVARP) {
            cout << "(rarp)";
    } else {
            cout << "(?)";
    }

    cout << " " << length << endl;

    if(bip)
        ip_handler(NULL, header, packet);








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
            collect(packet, &header);
        }
    }

    pcap_close(handle);
};

string Pcap::getInfo()
{
    Json s;

    s.add("o", speed);
    s.add("Ko", speed/1024.0);
    s.add("Mo", speed/(1024.0*1024.0));

    return s.toString();
};

void* th_packet_grab(void* data)
{
    Pcap *p = (Pcap*) data;

    cout << "Start Sniffing" << endl;
    
    p->packet_grab();

    return NULL;

};

