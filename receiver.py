#!/usr/bin/env python3

import scapy.all as scapy
import re
import subprocess

class staticClass:
    pass
static = staticClass()

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPacket, filter="ip")

def processSniffedPacket(packet):
    try:
        if(packet[scapy.IP].src != static.selfIP):
            response = ""
            response += re.search(r"roomba:.*\"", str(scapy.raw(packet))).group(0)
            response = re.search(r"'.*'", response).group(0)
            command = response[1:-1]                                                #uhhhh you can figure it out
            if command != "":
                ip = packet[scapy.IP].src
                print("[+] Got a command '" + command + "' from " + ip)
                runCommand(command, ip)
    except:
        pass

def reply(string, ip):
    packet = scapy.IP(dst=ip) / scapy.Raw(load=string)
    for x in range(0, 25):
        print("[+] Replying '" + string + "' to " + ip)
        scapy.send(packet)

def runCommand(command, mac):
    if command == "Are you roomba?":
        reply("roomba:'I am roomba'", mac)
    elif command == "Python_Dictionaries":
        print("Python dictionaries are not objects. That's final.")

def getOwnIp(interface):
    output = subprocess.check_output(["ifconfig", interface])
    ip = re.search(r"\d*\.\d*\.\d*\.\d*", str(output)).group(0)
    print(ip)
    return ip

static.selfIP = getOwnIp("wlan0")
sniff("wlan0")
