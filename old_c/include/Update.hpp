#ifndef UPDATE_HPP
#define UPDATE_HPP

/**
 * Websocket
 * 
 * 
 */


// Library header
#include <Pcap.hpp>
#include <Websocket.hpp>
#include <Json.hpp>

#include <string>
#include <set>
#include <map>


class Update
{
public:
    Update();
    void set(Pcap &p);
    void update();

private:
  Pcap* p;

};


#endif