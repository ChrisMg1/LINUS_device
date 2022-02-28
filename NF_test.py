import sys
sys.path.append("/home/pi/.local/lib/python3.9/site-packages")
# import my_module

#import NetfilterQueue

from netfilterqueue import NetfilterQueue
from scapy.all import *


def print_and_accept(pkt):
    print('==> CM: IPtables packet')
    print(pkt)
# Here I 'convert' nfqueue to scapy:
    sc_pkt = IP(pkt.get_payload())
    print('==> CM: scapy packet begin')
    print ( sc_pkt.show())
    print(type(sc_pkt) )
    for byte in sc_pkt:
        pass
#        print( byte )

#    print('DST', sc_pkt.dst )
#    print('SRC', sc_pkt.src )
#    print('CHK', sc_pkt.chksum)
#    print('IP checksum: ', sc_pkt[IP].chksum)

# TCP payload is the actual data to be encrypted
    if sc_pkt.haslayer(TCP):
        payload_before = len(sc_pkt[TCP].payload)

    if sc_pkt.haslayer(Raw):
        sc_pkt[Raw].load = 'cm_re\n'
        del sc_pkt.chksum
        sc_pkt = sc_pkt.__class__(bytes(sc_pkt))

        payload_after = len(sc_pkt[TCP].payload)
        payload_dif = payload_after - payload_before
        sc_pkt[IP].len = sc_pkt[IP].len + payload_dif
#        sc_pkt[TCP].payload = bytes('ex\n', 'UTF-8')


        print('==> CM: scapy packet end')
        print ( sc_pkt.show())

# TODO: The packet is crafted, but how to send the manipulated packet??


#TODO: Either use nfqueue (...verdict... seems deprecated) or scapy (drop/send seems have trouble with packet format str/byte)
#        pkt.set_verdict_modified(nfqueue.NF_ACCEPT, str(sc_pkt), len(sc_pkt))


        pkt.drop()
        sendp(sc_pkt)

#        pkt.accept()

    else:
        pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
