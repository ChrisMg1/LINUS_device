import sys
sys.path.append("/home/pi/.local/lib/python3.9/site-packages")
from netfilterqueue import NetfilterQueue

#import nfqueue
from scapy.all import *
import os
os.system('iptables -A OUTPUT -p udp --dport 53 -j NFQUEUE')
def callback(payload):
    data = payload.get_data()
    pkt = IP(data)
    if pkt.haslayer(DNSQR): # Beginning modifications
        pkt[IP].dst = '192.168.115.118'
        pkt[IP].len = len(str(pkt))
        pkt[UDP].len = len(str(pkt[UDP]))
        del pkt[IP].chksum
        payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(pkt), len(pkt))
def main():
    q = NetfilterQueue()
#    q = nfqueue.queue()
#    q.open()
    q.bind(0, socket.AF_INET)
    q.set_callback(callback)
    q.create_queue(0)
    try:
        q.try_run() # Main loop
    except KeyboardInterrupt:
        q.unbind(socket.AF_INET)
        q.close()
        os.system('iptables -F')
        os.system('iptables -X')
main()
