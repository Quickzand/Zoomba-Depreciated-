#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import subprocess
import re

class roombaClass:
    pass
roomba = roombaClass()
roomba.isFound = False

def getOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Option to set the interface")
    options =  parser.parse_args()

    if not options.interface:
        parser.error("You did not specify an interface")

    return options

def findRoomba(interface):
    #range = getIpRange(interface)
    # packet1 = scapy.IP(ip["ip"])
    packet = scapy.Ether() / scapy.TCP() / "roomba:'Are you roomba?'"
    print(packet.show())
    scapy.send(packet)

    scapy.sniff(iface=interface, store=False, prn=listenForRoomba, timeout=1)

    if not roomba.isFound:
        print("[-] Roomba not found trying again")
        findRoomba(interface)
    #arp_request = scapy.ARP(pdst=ipRange)
    # broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # arp_request_broadcast = broadcast/"hi"
    # arp_request_broadcast.show()
    # (answered, unanswered) = scapy.srp(arp_request_broadcast, timeout=1)

def listenForRoomba(packet):
    try:
        response = ""
        response += re.search(r"roomba:.*\"", str(scapy.raw(packet))).group(0)
        response = re.search(r"'.*'", response).group(0)
        response = response[1:-1]
        print(response)
        if(response == "I am roomba"):
            roomba.isFound = True
            roomba.mac = packet.src
            print("[+] Roomba found at " + roomba.mac)
    except:
        pass

if __name__ == "__main__":
    options = getOptions()
    findRoomba(options.interface)
