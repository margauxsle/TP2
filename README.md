# GNS3 TP2: Common network attacks

## I. Setup

On drag'n drop tous les switchs/VPCS/routeurs/NAT

On câble tous les équipements entre eux en suivant la topo 

### Configuration du serveur dhcp légitime en 10.2.1.11:

sudo nano /etc/netplan/01-network-manager-all.yaml:

```yaml
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
```

sudo nano /etc/dhcp/dhcpd.conf:

```yaml
subnet 10.2.1.0 netmask 255.255.255.0 {
    range 10.2.1.100 10.2.1.200;
    option subnet-mask 255.255.255.0;
    option routers 10.2.1.254;
}
```

sudo nano /etc/default/isc-dhcp-server

```yaml
INTERFACESv4="enp0s8"
```

### Configuration des IP des VPCS

On attribe des ip statiques à PC1 et PC2 avec la commande: ip [IP] [gateway]
Pour les autres VPCS, on utilise la commande "dhcp" pour récupérer une ip avec le serveur dhcp en .11

### Configuration du routeur

#### Accès Internet

Configurer l'interface pour obtenir une adresse IP via DHCP, dans un terminal du router on entre:

```yaml
conf t
interface FastEthernet1/0
ip address dhcp
no shutdown
exit
exit
sh ip int br
ping 8.8.8.8
```

Configurer l'adresse ip de l'interface LAN sur le routeur:

```yaml
conf t
interface FastEthernet0/0
ip address 10.2.1.254 255.255.255.0
no shutdown
```

Activer la NAT pour router les paquets du LAN vers Internet:

```yaml
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
```

On check depuis routeur et vpcs: ping 1.1.1.1

## II. Attaques DHCP

### Configuration du serveur illégitime

#### Installer et configurer dnsmasq

sudo apt install dnsmasq -y

sudo systemctl stop dnsmasq

sudo nano /etc/dnsmasq.conf:

```yaml
interface=enp0s8
dhcp-range=10.2.1.220,10.2.1.230
dhcp-option=3,10.2.1.254
dhcp-option=6,1.1.1.1
```

sudo nano /etc/netplan/01-network-manager-all.yaml:

```yaml
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
```

netplan apply

sudo sysctl -w net.ipv4.ip_forward=1    (pour router paquets)

on déconnecte le serveur dhcp légitime

on crée un nouveau VPCS, cmd "dhcp" => notre serveur illégitime lui donne une ip et lui dit qu'on est sa gateway

## III. Remédiations

### Attaques DHCP

1. Configurez les équipements réseau pour bloquer les réponses DHCP non autorisées

2. Utiliser des outils de monitoring

3. isolez le trafic DHCP dans un VLAN

4. Restreindre le nombre d'adresses MAC autorisées par port sur le switch

### Attaques ARP

1. S'assurer que seules les réponses ARP légitimes sont acceptées par notre réseau

2. Configurez manuellement les adresses ip et mac pour les équipements importants

3. Utilisez des outils pour surveiller les modifications suspectes dans le réseau

### DNS Spoofing

2. Configurez nos appareils pour qu'ils utilisent des serveurs DNS sûrs

3. Protégez le réseau en bloquant les requêtes DNS suspectes

4. Utilisez DNS over HTTPS pour chiffrer les requêtes DNS et empêcher qu'elles soient interceptées