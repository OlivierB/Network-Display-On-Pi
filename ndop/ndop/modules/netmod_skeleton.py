# encoding: utf-8

"""
Skeleton
Base Module

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule


class NetModChild(NetModule):
    """
    Example class - Do not use it except for create a new one !
    """

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, savecode=('m', 30), protocol='skeleton', savebdd=True, *args, **kwargs)
        
        # module variable embed in configuration file
        self.myConfigVariable = 10
        self.add_conf_override("myConfigVariable")

    def pkt_handler(self, pkt):
        """
        Called by sniffer when a new packet arrive

        pkt is formated with Packet class
        """
        pass

    def flow_handler(self, flow):
        """
        Called by sniffer when a new flow of packets arrive

        pkt is formated with flow class
        """

        # Flow variables :
        #     dFlows
        #     dOctets
        #     dPkts
        #     dst_as
        #     dst_mask
        #     dst_tag
        #     dstaddr
        #     dstport
        #     engine_id
        #     engine_type
        #     exaddr
        #     extra_pkts
        #     first
        #     in_encaps
        #     input
        #     last
        #     marked_tos
        #     nexthop
        #     out_encaps
        #     output
        #     peer_nexthop
        #     prot
        #     router_sc
        #     src_as
        #     src_mask
        #     src_tag
        #     srcaddr
        #     srcport
        #     sysUpTime
        #     tcp_flags
        #     tos
        #     unix_nsecs
        #     unix_secs


    # Flowtools exception
    # import flowtools
    # except flowtools.Error:


        pass

    def update(self):
        """
        Refresh method called every updatetime

        Return values to send to clients (websockets)
        automatically convert in json

        You have to return a dict or None if nothing
        """

        return None

    def database_init(self, db_class):
        """
        Clalled to init module database
        """

#         req = \
# """
# CREATE TABLE IF NOT EXISTS `skeleton_example` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   `text` varchar(60) NOT NULL,
#   `value` int(11) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;
# """
#         db_class.execute(req)

        pass


    def database_save(self, db_class):
        """
        Called to save module data in sql database every savetime

        return a list of sql request to save module content
            else return None

        """

        # # Create a SQL request
        # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # req = "INSERT INTO skeleton_example(date, text, value) VALUES (\"" + sql_date + "\", \"test\", 0);"

        # # execute SQL
        # db_class.execute(req)


        pass