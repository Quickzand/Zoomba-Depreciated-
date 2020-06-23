#!/usr/bin/env python3

import scapy.all as scapy
import re

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPacket)

def processSniffedPacket(packet):
    try:
        response = ""
        response += re.search(r"roomba:.*\"", str(scapy.raw(packet))).group(0)
        response = re.search(r"'.*'", response).group(0)
        command = response[1:-1]                                                #uhhhh you can figure it out
        print(command)
        if command != "":
            mac = packet.src
            print(mac)
            runCommand(command, mac)
    except:
        pass

def reply(string, mac):
    packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP() / scapy.Raw(load=string)
    print(packet.show())
    scapy.send(packet)

def runCommand(command, mac):
    if command == "Are you roomba?":
        reply("roomba:'I am roomba'", mac)


sniff("wlan0")
