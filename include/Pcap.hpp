#ifndef PCAP_HPP
#define PCAP_HPP

/**
 * Interface pcap lib C++
 * 
 * 
 */

// Library header
#include <pcap.h>
#include <pthread.h>

#include <iostream>
#include <vector>
#include <string>

// packet analisys
#include <netinet/in.h>


class Pcap
{
public:
    Pcap();
    void packet_grab();
    void start();
    void stop();
    void collect(const u_char *p, struct pcap_pkthdr *h);

    void handler_ip(const struct pcap_pkthdr* pkthdr, const u_char* packet);

    std::string getInfo();

private:
    pthread_t thread_packet_grab;
    bool running;
    bpf_u_int32 mask;   /* Our netmask */
    bpf_u_int32 net;    /* Our IP */
    

    // data
    unsigned int long p_number_tmp;
    unsigned int long p_size_tmp;
    timeval time_collect, time_collect2;
    int update_MS;

    // stat
    double speed;
    double speed_in;
    double speed_out;
    double speed_local;

    unsigned int long p_number;
    unsigned int long p_size;

    unsigned int long p_size_in;
    unsigned int long p_size_out;
    unsigned int long p_size_local;

};

void* th_packet_grab(void* data);

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


#endif