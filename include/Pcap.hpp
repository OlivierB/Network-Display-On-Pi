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


class Pcap
{
public:
    Pcap();
    void packet_grab();
    void start();
    void stop();
    void collect(const u_char *p, struct pcap_pkthdr *h);

    std::string getInfo();

private:
    pthread_t thread_packet_grab;
    bool running;
    

    // data
    unsigned int long p_number_tmp;
    unsigned int long p_size_tmp;
    timeval time_collect, time_collect2;
    int update_MS;

    // stat
    double speed;
    unsigned int long p_number;
    unsigned int long p_size;

};

void* th_packet_grab(void* data);

#endif