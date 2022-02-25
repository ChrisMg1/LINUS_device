import sys
sys.path.append("/home/pi/.local/lib/python3.9/site-packages")
# import my_module

#import NetfilterQueue

from netfilterqueue import NetfilterQueue
from scapy.all import *


def print_and_accept(pkt):
    print(pkt)
# Here I 'convert' nfqueue to scapy:
    print('CM:Do fancy stuff')
    sc_pkt = IP(pkt.get_payload())
    print ( sc_pkt )
    for byte in sc_pkt:
        pass
#        print( byte )

    print('DST', sc_pkt.dst )
    print('SRC', sc_pkt.src )

    print('looking into IP')
    print(sc_pkt.show())
    print('IP checksum: ', sc_pkt[IP].chksum)

# TCP payload is the actual data to be encrypted
    if sc_pkt.haslayer(TCP):
        print('TCP checksum: ', sc_pkt[TCP].chksum)
        print('PAYLOAD before: ', sc_pkt[TCP].payload)
        payload_before = len(sc_pkt[TCP].payload)
        sc_pkt[TCP].payload = str(sc_pkt[TCP].payload).replace('err','txx')
        payload_after = len(sc_pkt[TCP].payload)
        payload_dif = payload_after - payload_before
        sc_pkt[IP].len = sc_pkt[IP].len + payload_dif
#        sc_pkt[TCP].payload = bytes('ex\n', 'UTF-8')

#TODO: Here seems to be the problem: The packet is not properly crafted after 'replace'; confusing byte / str when trying 'print(sc_pkt.show())'
        print('PAYLOAD after: ', sc_pkt[TCP].payload)

#        pkt.set_payload(bytes(sc_pkt))

#TODO: Either use nfqueue (...verdict... seems deprecated) or scapy (drop/send seems have trouble with packet format str/byte)
#        pkt.set_verdict_modified(nfqueue.NF_ACCEPT, str(sc_pkt), len(sc_pkt))
#        pkt.drop()
#        send(sc_pkt)
        pkt.accept()

    else:
        pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
