from scapy.all import *

def checkIfDnsRequest(packet):
    if packet.haslayer(DNS) and packet[DNS].qd:
        dnsQuery = packet[DNS].qd.qname.decode()
        print(f"Requete DNS envoyé à {dnsQuery}")

        if packet[DNS].ancount > 0:
            for i in range(packet[DNS].ancount):
                try:
                    dnsAnswer = packet[DNS].an[i]
                    if dnsAnswer.type == 1:
                        print(f"Réponse DNS: {dnsAnswer.rdata}")
                except IndexError:
                    print("IndexError: Réponse non trouvée")

sniff(filter="udp port 53", prn=checkIfDnsRequest)