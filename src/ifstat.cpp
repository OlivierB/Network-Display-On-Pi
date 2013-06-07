/* Name: ifstat
 * Date: Thu Oct  2 12:34:33 CEST 2003
 * Author: Rainer Wichmann
 * 
 * code from kstat by FuSyS
 * bug fixed (buffer overflow in dumpHW)
 * listing of all interfaces by default
 *
 * Usage: ifstat [interface]
 *
 * Compile: 
 *  gcc -static -O2 -Wall -I/usr/src/linux/include -o ifstat ifstat.c
 *
 * NOTE: You need the kernel headers (/usr/src/linux/include) to compile !!!
 */

/*
 * Name: kstat v.1.1 if.c
 * Date: Sun Feb 10 02:49:49 CET 2002
 * Author: FuSyS [fusys@s0ftpj.org, fusys@sikurezza.org]
 *
 * SoftProject Digital Security for Y2K
 * Sikurezza.org - Italian Security Mailinglist
 *
 * MOJITO-WARE LICENSE - This source code is like "THE BEER-WARE LICENSE" by
 * Poul-Henning Kamp <phk@FreeBSD.ORG> but you can give me in return a mojito.
 *
 * Tested on: Slackware 8 Linux MaNTRa 2.4.16 #4 i686 unknown
 */

/* 
   gcc -O2 -Wall -I/usr/src/linux/include -o ifstatus ifstatus.c 
*/
/* #include "linux.h"  */

/*
 * Name: kstat v.1.1 linux.h
 * Date: Sun Feb 10 02:49:49 CET 2002
 * Author: FuSyS [fusys@s0ftpj.org, fusys@sikurezza.org]
 *
 * SoftProject Digital Security for Y2K
 * Sikurezza.org - Italian Security Mailinglist
 *
 * MOJITO-WARE LICENSE - This source code is like "THE BEER-WARE LICENSE" by
 * Poul-Henning Kamp <phk@FreeBSD.ORG> but you can give me in return a mojito.
 *
 * Tested on: Slackware 8 Linux MaNTRa 2.4.16 #4 i686 unknown
 */

#define NR_TASKS PID_MAX

#define __KERNEL__
#include <linux/netdevice.h>
#include <linux/inetdevice.h>
#include <net/ipv6.h>
#include <net/if_inet6.h>
#include <linux/if_arp.h>
#include <net/sock.h>
#include <linux/sched.h>
#include <linux/capability.h>
#include <linux/module.h>
#include <linux/types.h>
#undef __KERNEL__

#include <errno.h>
#include <getopt.h>
#include <linux/version.h>

/*
 * Name: kstat v.1.1 libc.h
 * Date: Sun Feb 10 02:49:49 CET 2002
 * Author: FuSyS [fusys@s0ftpj.org, fusys@sikurezza.org]
 *
 * SoftProject Digital Security for Y2K
 * Sikurezza.org - Italian Security Mailinglist
 *
 * MOJITO-WARE LICENSE - This source code is like "THE BEER-WARE LICENSE" by
 * Poul-Henning Kamp <phk@FreeBSD.ORG> but you can give me in return a mojito.
 *
 * Tested on: Slackware 8 Linux MaNTRa 2.4.16 #4 i686 unknown
 */

#define SEEK_SET        0
typedef struct _IO_FILE FILE;
extern unsigned int sleep (unsigned int __seconds);
extern void *memmem (__const void *__haystack, size_t __haystacklen,
		__const void *__needle, size_t __needlelen);
extern FILE *fopen __P ((__const char *__restrict __filename,
                         __const char *__restrict __modes));
extern int fprintf (FILE *__restrict __stream,
                    __const char *__restrict __format, ...);
extern int fseek (FILE *__stream, long int __off, int __whence);
extern int fclose (FILE *__stream);
extern char *fgets __P ((char *__restrict __s, int __n,
                         FILE *__restrict __stream));
extern char *fputs __P ((__const char *__restrict __s,
			 FILE *__restrict __stream));
extern int fflush __P ((FILE *__stream));
extern int getchar __P(());
extern int getpid (void);
extern int atoi __P ((__const char *__nptr));
extern unsigned long int strtoul __P ((__const char *__restrict __nptr,
                                       char **__restrict __endptr,
                                       int __base));
extern int printf __P ((__const char *__restrict __format, ...));
extern int open __P ((__const char *__file, int __oflag, ...));
extern int close (int __fd);
extern __ptr_t realloc __P ((__ptr_t __ptr, size_t __size));
extern void free __P ((__ptr_t __ptr));
extern off_t lseek __P ((int __fd, off_t __offset, int __whence));
extern ssize_t read __P ((int __fd, __ptr_t __buf, size_t __nbytes));
extern ssize_t write __P ((int __fd, __ptr_t __buf, size_t __nbytes));
extern __ptr_t malloc __P ((size_t __size));
extern int system __P ((__const char *__command));
extern void exit (int __status);


#define KMEM		"/dev/kmem"
#define DEV_BASE_OFF	"dev_base"
#define TASK_OFF	"init_task"
#define SYSCALL		"sys_call_table"
#define IOPORT		"ioport_resource"
#define INETOPS		"inet_stream_ops"
#define PROC_ROOT	"proc_root"

/* 
 * TCPOFF is inet_stream_ops - tcp_prot
 * UDPOFF is inet_stream_ops - udp_prot
 * RAWOFF is inet_stream_ops - raw_prot
 * HEXOFF is ioport_resource - kernel_module
 */
#if LINUX_VERSION_CODE == KERNEL_VERSION(2,4,18)
#define TCPOFF  3136
#define UDPOFF  2656
#define RAWOFF  2848
#define HEXOFF  184
#elif LINUX_VERSION_CODE >= KERNEL_VERSION(2,4,16)
#define TCPOFF  3136
#define UDPOFF  2656
#define RAWOFF  2848
#define HEXOFF	188
#elif LINUX_VERSION_CODE >= KERNEL_VERSION(2,4,7)
#define TCPOFF  3136
#define UDPOFF  2656
#define RAWOFF  2848
#define HEXOFF	156
#else
#define TCPOFF  3136
#define UDPOFF  2656
#define RAWOFF  2848
#define HEXOFF	160
#endif

#define FPRINT_SIZE	10

int errno, fd, flag_unknown = 0;
char *iff, name[1024];


int find_kmem_offset(char*);
int find_module_addr();
int kread(int, unsigned long, void*, int);
int iff_stat();

/* PLEASE NOTE THAT FOLLOWING IS A STRIPPED DOWN VERSION FROM MODUTILS */

struct new_module_symbol
{
  unsigned long value;
  unsigned long name;
};

struct new_module_info
{
  unsigned long address;
  unsigned long size;
  unsigned long flags;
};

struct module_stat {
        char *name;
        unsigned long addr;
        unsigned long modstruct;
	unsigned long size;
        unsigned long flags;
        long usecount;
        size_t nsyms;
        struct module_symbol *syms;
        size_t nrefs;
        struct module_stat **refs;
        unsigned long status;
};

int query_module(const char *name, int which, void *buf, size_t bufsize,
                 size_t *ret);

/* Values for query_module's which.  */

#define QM_MODULES      1
#define QM_DEPS         2
#define QM_REFS         3
#define QM_SYMBOLS      4
#define QM_INFO         5

/* END FROM MODUTILS */



// void perror(const char *s);

char *ntoa(unsigned long ip) {
        static char buff[18];
        char *p;
        p = (char *) &ip;
        sprintf(buff, "%d.%d.%d.%d",
                (p[0] & 255), (p[1] & 255), (p[2] & 255), (p[3] & 255));
        return(buff);
}

#ifdef IPV6
char *ntoa6(struct in6_addr addr) {
        static char buff[40];
	int j, w=1, len=0, i=1, lo=0;
	char x[16]={0,};

	for (j=0; j<16; j++) {
                if(j==15 && (!(x[14]) && !(x[13]) && !(x[12]))){
                        sprintf(buff+len, "::");
                        len+=2; lo++;
                }
		if(addr.s6_addr[j]){
			i++; x[j]=1;
			sprintf(buff+len, "%02x", (addr.s6_addr[j]));
                	len += 2;
		}
		if(!(w++%2) && (x[j] || (!(x[j]) && !(x[j-1]) && x[j-2])) && j<15){
			sprintf(buff+len, ":");
			len++;
		}
        }
	if(i==1 && !lo) sprintf(buff+len, "::");

	return(buff);
}
#endif


void err(char *str)
{
	printf("%s\n", str);
	exit(1);
}

int find_kmem_offset(char *sym_name)
{
	struct new_module_symbol *syms, *s;
	size_t ret, bufsize, nsymbols, j;

	syms=malloc(bufsize = sizeof(struct new_module_symbol));
	retry_kern_symbol_load:
	if(query_module(NULL, QM_SYMBOLS, syms, bufsize, &ret)){
        	if (errno == ENOSPC){
              		syms =(struct new_module_symbol *)realloc(syms, bufsize = ret);
              		goto retry_kern_symbol_load; 
            	}
          	printf("find_kmem_offset: QM_SYMBOLS error %d\n", errno);
          	return -1;
        }
      	nsymbols = ret;

      	for (j = 0, s = syms; j < nsymbols; ++j, ++s){
		if(strstr((char *)syms+s->name, sym_name)){
			free(syms);
			return s->value;
		}
	}
	printf("%s Kmem Offset Not Found\n\n", sym_name);
	free(syms);
	return -1;
}


int kread(int des, unsigned long addr, void *buf, int len)
{
	int rlen;

	if(lseek(des, (off_t)addr, SEEK_SET) == -1)
	  {
	    printf("kread: lseek: %d\n", errno);
	    return -1;
	  }
	if((rlen = read(des, buf, len)) != len)
	  {
	    if (flag_unknown == 1)
	      {
		printf("No further data\n");
		return 0;
	      }
	    printf("kread: read: %d\n", errno);
	    return -1;
	  }
	return rlen;
}

char *dumpHW (unsigned char *hw_s) {
        static char buffer[256];
        sprintf(buffer, "%02X:%02X:%02X:%02X:%02X:%02X",
           hw_s[0], hw_s[1], hw_s[2], hw_s[3], hw_s[4], hw_s[5]);
        return buffer;
}

void looking_if(unsigned short type)
{
  flag_unknown = 0;
  switch(type){
    
    case ARPHRD_NETROM:	printf("NET/ROM");
      break;
    case ARPHRD_ETHER:	printf("Ethernet");
      break;
    case ARPHRD_EETHER:	printf("Experimental Ethernet");
      break;
    case ARPHRD_AX25:	printf("AX.25 lv2");
      break;
    case ARPHRD_PRONET:	printf("PROnet");
      break;
    case ARPHRD_CHAOS:	printf("Chaosnet");
      break;
    case ARPHRD_IEEE802:	printf("IEEE 802.2");
      break;
    case ARPHRD_ARCNET:	printf("ARCnet");
      break;
    case ARPHRD_APPLETLK:	printf("APPLEtalk");
      break;
    case ARPHRD_DLCI:	printf("Frame Relay DLCI");
      break;
    case ARPHRD_METRICOM:	printf("STRIP");
      break;
    case ARPHRD_SLIP:	printf("Serial Line IP");
      break;
    case ARPHRD_CSLIP:	printf("Compressed SLIP");
      break;
    case ARPHRD_X25:	printf("X.25");
      break;
    case ARPHRD_PPP:        printf("Point-to-Point Protocol");
      break;
    case ARPHRD_HDLC:	printf("Cisco HDLC");
      break;
    case ARPHRD_TUNNEL:	printf("IPIP Tunnel");
      break;
    case ARPHRD_LOOPBACK:   printf("Local Loopback");
      break;
    case ARPHRD_LOCALTLK:	printf("Localtalk");
      break;
    case ARPHRD_FDDI:	printf("Fiber Distributed Data Interface");
      break;
    case ARPHRD_IPGRE:	printf("GRE over IP");
      break;
    case ARPHRD_IRDA:	printf("Linux/InfraRed");
      break;
    default:		printf("Unknown"); flag_unknown = 1;
      break;		
  }
}

void print_if(struct net_device dev)
{
	struct in_device in_dev;
	struct in_ifaddr ifa;
#ifdef IPV6
	struct inet6_dev in6_dev;
	struct inet6_ifaddr ifa6;
#endif

	printf("%s\t", name);
	printf("Link encap:");
	looking_if(dev.type);
	printf("  Internal Index:%d", dev.ifindex);
	if(dev.type==1)
	printf("  MAC:%s\n\t", dumpHW(dev.dev_addr));
	else printf("\n\t");
	if(dev.flags & IFF_UP) printf("UP ");
	if(dev.flags & IFF_BROADCAST) printf("BROADCAST ");
	if(dev.flags & IFF_DEBUG) printf("DEBUG ");
	if(dev.flags & IFF_LOOPBACK) printf("LOOPBACK ");
	if(dev.flags & IFF_POINTOPOINT) printf("POINTOPOINT ");
	if(dev.flags & IFF_NOTRAILERS) printf("NOTRAILERS ");
	if(dev.flags & IFF_RUNNING) printf("RUNNING ");
	if(dev.flags & IFF_NOARP) printf("NOARP ");
	if(dev.flags & IFF_PROMISC || dev.gflags & IFF_PROMISC || 
		dev.promiscuity != 0) printf("PROMISC ");
	if(dev.flags & IFF_ALLMULTI || dev.allmulti != 0) printf("ALLMULTI ");
	if(dev.flags & IFF_MASTER) printf("MASTER ");
	if(dev.flags & IFF_SLAVE) printf("SLAVE ");
	if(dev.flags & IFF_MULTICAST) printf("MULTICAST ");
	if(dev.flags & IFF_DYNAMIC) printf("DYNAMIC ");
	printf(" MTU:%d", dev.mtu);
	if(dev.type == 1)
                printf("  IRQ:%d Base:0x%lx\n\t", dev.irq, dev.base_addr&0x0000ffff);
        else
                printf("\n\t");
	if (flag_unknown == 1)
	  {
	    flag_unknown = 0;
	    return;
	  }
	if(kread(fd, (unsigned long)dev.ip_ptr, &in_dev, sizeof(struct in_device)) == -1) err("kread error");
	if(kread(fd, (unsigned long)in_dev.ifa_list, &ifa, sizeof(struct in_ifaddr)) == -1) err("kread error");
	if(dev.flags & IFF_UP)
		printf("inet addr:%s", ntoa(ifa.ifa_local));
	if(dev.flags & IFF_UP && dev.flags & IFF_POINTOPOINT)
		printf("  P-t-P:%s", ntoa(ifa.ifa_address));
	else
		printf("  Bcast:%s", ntoa(ifa.ifa_broadcast));
	printf("  Mask:%s\n\t", ntoa(ifa.ifa_mask));
#ifdef IPV6
	if((dev.type == ARPHRD_ETHER || dev.type == ARPHRD_LOOPBACK) && (dev.flags & IFF_UP)) {
	 if(kread(fd, (unsigned long)dev.ip6_ptr, &in6_dev, sizeof(struct inet6_dev)) == -1) err("kread error");
	 if(kread(fd, (unsigned long)in6_dev.addr_list, &ifa6, sizeof(struct inet6_ifaddr)) == -1) err("kread error");
	 printf("inet6 addr: %s/%d", ntoa6(ifa6.addr), ifa6.prefix_len);
	 switch(ifa6.scope){
		
		case IFA_LINK:		printf("  Scope:Link\n\t");
					break;
		case IFA_HOST:		printf("  Scope:Host\n\t");
					break;
		case IFA_SITE:		printf("  Scope:Site\n\t");
					break;
		case IFA_GLOBAL:	printf("  Scope:Global\n\t");
					break;
		default:		printf("  Scope:Unknown\n\t");
					break;
	 }
	}
#endif
	printf("IPv4 Sysctl Params:\n\t\t");
	printf("accept_redirects:\t\t%s\n\t\t", (in_dev.cnf.accept_redirects)?"yes":"no");
	printf("send_redirects:\t\t\t%s\n\t\t", (in_dev.cnf.send_redirects)?"yes":"no");
	printf("secure_redirects:\t\t%s\n\t\t", (in_dev.cnf.secure_redirects)?"yes":"no");
	printf("accept_source_route:\t\t%s\n\t\t", (in_dev.cnf.accept_source_route)?"yes":"no");
        printf("shared_media:\t\t\t%s\n\t\t", (in_dev.cnf.shared_media)?"yes":"no");
	printf("rp_filter:\t\t\t%s\n\t\t", (in_dev.cnf.rp_filter)?"yes":"no");
	printf("proxy_arp:\t\t\t%s\n\t\t", (in_dev.cnf.proxy_arp)?"yes":"no");
	printf("arp_filter:\t\t\t%s\n\t\t", (in_dev.cnf.arp_filter)?"yes":"no");
	printf("bootp_relay:\t\t\t%s\n\t\t", (in_dev.cnf.bootp_relay)?"yes":"no");
	printf("log_martians:\t\t\t%s\n\t\t", (in_dev.cnf.log_martians)?"yes":"no");
	printf("forwarding:\t\t\t%s\n\t\t", (in_dev.cnf.forwarding)?"yes":"no");
	printf("mc_forwarding:\t\t\t%s\n\t\t", (in_dev.cnf.mc_forwarding)?"yes":"no");
	printf("tag:\t\t\t\t%s\n\t\t\n\t", (in_dev.cnf.tag)?"yes":"no");
#ifdef IPV6
	if((dev.type == ARPHRD_ETHER) && (dev.flags & IFF_UP)) {
         printf("IPv6 Sysctl Params:\n\t\t");
         printf("forwarding:\t\t\t%s\n\t\t", (in6_dev.cnf.forwarding)?"yes":"no");
         printf("hop_limit:\t\t\t%s\n\t\t", (in6_dev.cnf.hop_limit)?"yes":"no");
         printf("mtu:\t\t\t\t%s\n\t\t", (in6_dev.cnf.mtu6)?"yes":"no");
         printf("accept_ra:\t\t\t%s\n\t\t", (in6_dev.cnf.accept_ra)?"yes":"no");
         printf("accept_redirects:\t\t%s\n\t\t", (in6_dev.cnf.accept_redirects)?"yes":"no");
         printf("autoconf:\t\t\t%s\n\t\t", (in6_dev.cnf.autoconf)?"yes":"no");
         printf("dad_transmits:\t\t\t%s\n\t\t", (in6_dev.cnf.dad_transmits)?"yes":"no");
         printf("router_solicitations:\t\t%s\n\t\t", (in6_dev.cnf.rtr_solicits)?"yes":"no");
         printf("router_solicitation_interval:\t%s\n\t\t", (in6_dev.cnf.rtr_solicit_interval)?"yes":"no");
         printf("router_solicitation_delay:\t%s\n\t\t", (in6_dev.cnf.rtr_solicit_delay)?"yes":"no");
	}
#endif
	if(dev.promiscuity) 
		printf("\n\tPROMISC Descriptors:\t\t%d", dev.promiscuity);
	printf("\n\n");	
}

int iff_stat()
{
	struct net_device *p, dev;
	unsigned long kaddr=0;

	name[9] = '\0';
	p=NULL;
	kaddr=find_kmem_offset(DEV_BASE_OFF);
	if(kaddr)
	  p=(struct net_device *)kaddr;
	else
	  {
	    printf("Cannot find %s\n", DEV_BASE_OFF);
	    exit (1);
	  }

	fd=open(KMEM, O_RDONLY);
	if(kread(fd, (unsigned long)p, &p, sizeof(struct net_device)) == -1) 
	  err("kread error");
	for(; p; p = dev.next){
	  if(kread(fd, (unsigned long)p, &dev,sizeof(struct net_device)) == -1)
	    err("kread error");
	  if(kread(fd, (unsigned long)dev.name, &name, 9) == -1) 
	    err("kread error");
	  name[9] = '\0';
	  if (iff != NULL)
	    {
	      if(!strcmp(name, iff)) {
		print_if(dev);
		exit(0);
	      }
	    }
	  else
	    {
	      print_if(dev);
	    }
	}
	printf("\n");
	exit(0);
}

int main (int argc, char *argv[])
{
  if ( (argc == 2) && (argv[1][0] == '-') && 
       ( (argv[1][1] == 'h') || (argv[1][1] == '-' && argv[1][2] == 'h')))
    {
      err("Usage: ifstatus <interface>");
      return 0;
    }
  iff = argv[1];
  iff_stat();
  return 0;
}
