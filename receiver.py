#!/usr/bin/env python3

import scapy.all as scapy
import re

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPacket)

def processSniffedPacket(packet):
    try:
        packet.show()
        response = ""
        response += re.search(r"roomba:.*\"", str(scapy.raw(packet))).group(0)
        response = re.search(r"'.*'", response).group(0)
        command = response[1:-1]                                                #uhhhh you can figure it out
        print(command)
        if command != "":
            mac = packet.src
            runCommand(command, mac)
    except:
        packet.show()
        pass

def reply(string, mac):
    packet = scapy.Ether(dst=mac) / scapy.ARP() / string
    print(packet.show())
    scapy.send(packet)

def runCommand(command, mac):
    if command == "Are you roomba?":
        reply("roomba:'I am roomba'", mac)


sniff("wlan0")
