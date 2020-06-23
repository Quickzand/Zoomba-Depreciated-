#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import subprocess
import re
from networkScanner import scan

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
    range = scan(getIpRange(interface))
    for ip in range:
        print(ip["ip"])
        packet = scapy.IP(dst = ip["ip"]) / "roomba: 'Are you roomba?'"
        print(packet.show())
        scapy.send(packet)

    scapy.sniff(iface=interface, store=False, prn=listenForRoomba, timeout=1)
    if not roomba.isFound:
        print("[-] Roomba not found trying again")
        findRoomba(interface)

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
        packet.show()
        pass

def getIpRange(interface):
    output = subprocess.check_output(["ifconfig", interface])
    gateway = re.search(r"\d*\.\d*\.\d*\.", str(output))
    ipRange = gateway.group(0) + "1/24"
    return ipRange

if __name__ == "__main__":
    options = getOptions()
    findRoomba(options.interface)
