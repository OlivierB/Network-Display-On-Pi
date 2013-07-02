#encoding: utf-8

"""
Network implementation data

Services list

@author: Olivier BLIN
"""

# Python lib import
from ... import layer


class DNS(layer.Layer):
    def __init__(self, pktdata):
        layer.Layer.__init__(self, protocol="DNS")

        # self.transaction_id = socket.ntohs(struct.unpack('H', pktdata[0:2])[0])
        self.dns_name = ''
        flags1 = ord(pktdata[2])

        if (flags1 >> 7) == 0:
            # print 'requete', self.transaction_id
            # print 'nb questions', socket.ntohs(struct.unpack('H', pktdata[4:6])[0])

            if (ord(pktdata[3]) & 0xf) == 0:
                # print 'pas d erreur', self.transaction_id

                i = 12
                string = ''

                length = ord(pktdata[i])

                while length != 0:
                    i += 1
                    string += (pktdata[i:i+length])
                    i += length
                    length = ord(pktdata[i])
                    if length != 0:
                        string += '.'

                self.dns_name = string
        # else:
        #     print 'reponse', self.transaction_id

        # if((flags1 >> 3) & 0xf == 0):
        #     print 'standard query'
        # else:
        #     print 'else'

        # if (flags2 & 0xf) == 0:
        #     print 'pas d erreur', self.transaction_id
        # else:
        #     print 'erreur', self.transaction_id

        # print 'nb reponses', socket.ntohs(struct.unpack('H', pktdata[6:8])[0])


class HTTP(layer.Layer):
    def __init__(self, pktdata):
        layer.Layer.__init__(self, protocol="HTTP")

        stype = ""
        cnt = 0
        dlen = min(len(pktdata), 10)
        if dlen > 0:
            while cnt < dlen and not (pktdata[cnt] == "/" or pktdata[cnt] == " "):
                stype += pktdata[cnt]
                # print pktdata[cnt]
                cnt += 1
        
        if stype in ["HTTP", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]:
            self.type = stype
        else:
            self.type = ""

        self.data = pktdata 


class HTTPS(layer.Layer):
    def __init__(self, pktdata):
        layer.Layer.__init__(self, protocol="HTTPS")

        self.payload = layer.Layer(pktdata)


dUDPType = {
    53: {'callback': DNS, 'protocol': 'DNS', 'description': 'DNS'}
}

dTCPType = {
    80: {'callback': HTTP, 'protocol': 'HTTP', 'description': 'HTTP'},
    443: {'callback': HTTPS, 'protocol': 'HTTPS', 'description': 'HTTPS'}
}
