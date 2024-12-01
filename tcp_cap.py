from scapy.all import *

def printResult(packet):
    print("TCP SYN ACK reçu !")
    print(f"- Adresse IP src : {packet['IP'].src}")
    print(f"- Adresse IP dst : {packet['IP'].dst}")
    print(f"- Port TCP src : {packet['TCP'].sport}")
    print(f"- Port TCP dst : {packet['TCP'].dport}")
    return

def packetFilter(packet):
    return TCP in packet and packet[TCP].flags == 0x12

def captureSynAck():
    packet = sniff(lfilter=packetFilter, count=1)[0]
    printResult(packet)
    return

captureSynAck()