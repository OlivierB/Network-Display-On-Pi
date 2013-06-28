// Class header
#include <Update.hpp>

// Library header
#include <iostream>
#include <vector>
#include <string>


using namespace std;

Update::Update()
{

};

void Update::set(Pcap &p)
{
	this->p = &p;
};
   
void Update::update()
{
	Websocket::getInstance()->send("bandwidth", p->getBandwidth());
   	Websocket::getInstance()->send("iplist", p->getIpListDist());
};
