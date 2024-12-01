from scapy.all import *

domainName = "efrei.net"
dnsServer = "8.8.8.8"

def craftDnsRequest(domainName, dnsServer):
    dnsQuery = DNS(rd=1, qd=DNSQR(qname=domainName))

    packet = (
        Ether(dst="ca:03:06:a0:00:00") /  # Mac de la gateway
        IP(dst=dnsServer) /
        UDP(sport=RandShort(), dport = 53) /
        dnsQuery
    )

    return packet

def sendDnsPacket(dnsPacket):
    response = srp(dnsPacket, timeout=10)
    if response[0]:
        for sent, received in response[0]:
            if received.haslayer(DNS):
                print(f"Réponse recue de {received[DNS].qd.qname.decode()}")
    else:
        print("Pas de réponse")

dnsPacket = craftDnsRequest(domainName, dnsServer)
sendDnsPacket(dnsPacket)