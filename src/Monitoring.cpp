// Class header
#include <Monitoring.hpp>

// Library header
#include <sys/time.h>
#include <sys/resource.h>
#include <sigar/sigar.h>
#include <sigar/sigar_format.h>

using namespace std;

Monitoring::Monitoring()
{

};

sigar_t *_sigar = NULL;
sigar_cpu_t _prev_cpu, *_prev_cpup = NULL;

sigar_t *sigar() {
  if (!_sigar)
  {
  	if (sigar_open(&_sigar) != SIGAR_OK)
  	{
  		cout << "Can't launch sigar" << endl;
  	}
  }

  return _sigar;
}

void Monitoring::getCpu()
{
	cout << "++CPU"  << endl;
	sigar_cpu_t curr;
    if (sigar_cpu_get(sigar(), &curr) != SIGAR_OK)
    {
    	return;
    }
    	


    sigar_cpu_get(sigar(), &_prev_cpu);
    _prev_cpup = &_prev_cpu;


    sigar_cpu_perc_t p;
    sigar_cpu_perc_calculate(&_prev_cpu, &curr, &p);


    // user = p.user * 100.;
    // sys = p.sys * 100.;
    // nice = p.nice * 100.;
    // idle = p.idle * 100.;
    // wait = p.wait * 100.;
    // irq = p.irq * 100.;
    // soft_irq = p.soft_irq * 100.;
    // stolen = p.stolen * 100.;
    // total = p.combined * 100.;

    // cout << curr.number << " " << curr.size << " "  << endl;


    cout << "--CPU"  << endl;
};

