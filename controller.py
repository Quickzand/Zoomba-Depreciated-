#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import subprocess
import re
from networkScanner import scan
import sys

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
    range = scan(getIpRange(interface))                                         #Gets a range of ips, sends them all the packet are you roomba, listens for a response
    for ip in range:
        packet = scapy.IP(dst = ip["ip"], src = getOwnIp(interface)) / "roomba: 'Are you roomba?'"
        scapy.send(packet, verbose=False)
    scapy.sniff(iface=interface, store=False, prn=listenForRoomba, timeout=3)
    if not roomba.isFound:
        print("[-] Roomba not found trying again")
        findRoomba(interface)

def listenForRoomba(packet):
    try:
        response = ""
        response += re.search(r"roomba:.*\"", str(scapy.raw(packet))).group(0)
        response = re.search(r"'.*'", response).group(0)
        response = response[1:-1]
        if(response == "I am roomba"):
            roomba.isFound = True
            roomba.ip = packet[scapy.IP].src
            print("\r[+] Roomba found at " + roomba.ip, end="")
    except:
        pass

def getIpRange(interface):
    output = subprocess.check_output(["ifconfig", interface])
    gateway = re.search(r"\d*\.\d*\.\d*\.", str(output))
    ipRange = gateway.group(0) + "1/24"
    return ipRange

def getOwnIp(interface):
    output = subprocess.check_output(["ifconfig", interface])
    ip = re.search(r"\d*\.\d*\.\d*\.\d*", str(output)).group(0)
    return ip

def runCommand(command, interface):
    if command == "clear":
        subprocess.run(["clear"])
    elif command == "exit":
        sys.exit("exiting...")
    else:
        fullCommand = "roomba: '"+command+"'"
        packet = scapy.IP(dst = roomba.ip, src = getOwnIp(interface)) / scapy.Raw(load=fullCommand)
        scapy.send(packet, verbose=False)

if __name__ == "__main__":
    options = getOptions()
    print("[+] Locating roomba")
    findRoomba(options.interface)
    print("\n")
    while True:
        command = input(" >> ")
        runCommand(command, options.interface)
