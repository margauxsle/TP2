# GNS3 TP2: Common network attacks

## I. Setup

On drag'n drop tous les switchs/VPCS/routeurs/NAT

On câble tous les équipements entre eux en suivant la topo 

1. Configuration du serveur dhcp légitime en 10.2.1.11:

sudo nano /etc/netplan/01-network-manager-all.yaml:

network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp0s8:
      dhcp4: no
      addresses:
        - 10.2.1.11/24
      routes:
        - to: default
          via: 10.2.1.254

sudo nano /etc/dhcp/dhcpd.conf:

subnet 10.2.1.0 netmask 255.255.255.0 {
    range 10.2.1.100 10.2.1.200;
    option subnet-mask 255.255.255.0;
    option routers 10.2.1.254;
}

sudo nano /etc/default/isc-dhcp-server

INTERFACESv4="enp0s8"

2. Configuration des IP des VPCS

On attribe des ip statiques à PC1 et PC2 avec la commande: ip [IP] [gateway]
Pour les autres VPCS, on utilise la commande "dhcp" pour récupérer une ip avec le serveur dhcp en .11

3. Configuration du routeur

### Accès Internet

Configurer l'interface pour obtenir une adresse IP via DHCP, dans un terminal du router on entre:

conf t
interface FastEthernet1/0
ip address dhcp
no shutdown
exit
exit
sh ip int br
ping 8.8.8.8

Configurer l'adresse ip de l'interface LAN sur le routeur:

conf t
interface FastEthernet0/0
ip address 10.2.1.254 255.255.255.0
no shutdown

Activer la NAT pour router les paquets du LAN vers Internet:

conf t
interface FastEthernet0/0
ip nat inside
interface FastEthernet1/0
ip nat outside
exit
access-list 1 permit any
ip nat inside source list 1 interface FastEthernet1/0 overload
exit
copy running-config startup-config

On check depuis routeur et vpcs: ping 1.1.1.1

## II. Attaques DHCP

### Configuration du serveur illégitime

1. Installer et configurer dnsmasq

sudo apt install dnsmasq -y
sudo systemctl stop dnsmasq

sudo nano /etc/dnsmasq.conf:

interface=enp0s8
dhcp-range=10.2.1.220,10.2.1.230
dhcp-option=3,10.2.1.254
dhcp-option=6,1.1.1.1

sudo nano /etc/netplan/01-network-manager-all.yaml:

network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp0s8:
      addresses:
        - 10.2.1.113/24
      routes:
        - to: default
          via: 10.2.1.254

netplan apply

sudo sysctl -w net.ipv4.ip_forward=1    (pour router paquets)

on déconnecte le serveur dhcp légitime

on crée un nouveau VPCS, cmd "dhcp" => notre serveur illégitime lui donne une ip et lui dit qu'on est sa gateway
