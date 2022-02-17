import sys
sys.path.append("/home/pi/.local/lib/python3.9/site-packages")
# import my_module

#import NetfilterQueue

from netfilterqueue import NetfilterQueue
from scapy.all import *


def print_and_accept(pkt):
    print(pkt)
    print('CM:Do fancy stuff')
    my_pay = pkt.get_payload()
    # print ( my_pay )
    for byte in my_pay:
        pass
#        print( byte )

#    print(my_pay[TCP].payload)

    print('DST', IP(my_pay).dst )
    print('SRC', IP(my_pay).src )
# Here I 'convert' nfqueue to scapy: 
    sc_pkt = IP(pkt.get_payload())
    print(sc_pkt.show())
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
