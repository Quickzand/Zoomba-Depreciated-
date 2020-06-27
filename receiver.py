#!/usr/bin/env python3

import scapy.all as scapy
import re
import subprocess
from _thread import start_new_thread

class staticClass:
    pass
static = staticClass()

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processSniffedPacket, filter="ip")

def processSniffedPacket(packet):
    try:
        if(packet[scapy.IP].src != static.selfIP):
            response = ""
            response += re.search(r"zoomba:.*\"", str(scapy.raw(packet))).group(0)
            response = re.search(r"'.*'", response).group(0)
            command = response[1:-1]                                                #uhhhh you can figure it out
            if command != "":
                ip = packet[scapy.IP].src
                print("[+] Got a command '" + command + "' from " + ip)
                runCommand(command, ip)
    except:
        pass

def reply(string, ip):
    start_new_thread(replyThread, (string, ip,))
def replyThread(string, ip):
    packet = scapy.IP(dst=ip) / scapy.Raw(load=string)
    print("[+] Replying '" + string + "' to " + ip)
    scapy.send(packet)

def runCommand(command, mac):
    if command == "Are you zoomba?":
        reply("zoomba:'I am zoomba'", mac)
    elif command == "Python_Dictionaries":
        print("Python dictionaries are not objects. That's final.")

def getOwnIp(interface):
    output = subprocess.check_output(["ifconfig", interface])
    ip = re.search(r"\d*\.\d*\.\d*\.\d*", str(output)).group(0)
    print(ip)
    return ip

if __name__ == "__main__":
    static.selfIP = getOwnIp("wlan0")
    sniff("wlan0")
