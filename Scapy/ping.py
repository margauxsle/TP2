from scapy.all import *

ipSrc = "10.2.1.112"
macSrc = "08:00:27:1e:36:4a"

targets = [
    {"name" : "Gateway", "ip" : "10.2.1.254", "mac" : "ca:03:06:a0:00:00"},
    {"name" : "DHCP Server", "ip" : "10.2.1.11", "mac" : "08:00:27:18:2b:a1"},
]

def sendPing(target):
    ping = ICMP(type=8)
    packet = IP(src=ipSrc, dst=target["ip"])
    frame = Ether(src=macSrc, dst=target["mac"])
    final_frame = frame/packet/ping
    answers, unanswered_paquets = srp(final_frame, timeout=10)
    return answers

for target in targets:
    answers = sendPing(target)
    print(f"Test de ping {target['name']}")
    if len(answers) > 0 and target["name"] == "Gateway":
        print(f"La gateway a répondu, pong reçu: {answers[0]}")
        break
    elif len(answers) > 0 and target["name"] == "DHCP Server":
        print(f"Pong recu : {answers[0]}")
    else:
        print("Pas de réponse mon reuf")
