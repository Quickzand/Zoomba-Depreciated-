#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import subprocess
import re
from networkScanner import scan
import sys
from _thread import start_new_thread
import json
import ast

class zoombaClass:
    pass
zoomba = zoombaClass()
zoomba.isFound = False
zoomba.ip = ""

def getOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Option to set the interface")
    options =  parser.parse_args()

    if not options.interface:
        parser.error("You did not specify an interface")

    return options

def findzoomba(interface):
    range = scan(getIpRange(interface))                                         #Gets a range of ips, sends them all the packet are you zoomba, listens for a response
    for ip in range:
        packet = scapy.IP(dst = ip["ip"], src = getOwnIp(interface)) / "zoomba: 'Are you zoomba?'"
        scapy.send(packet, verbose=False)
    if not zoomba.isFound:
        print("[-] zoomba not found trying again")
        findzoomba(interface)

def sniffForZoomba(interface):
    scapy.sniff(iface=interface, store=False, prn=listenForzoomba, filter="ip")

def listenForzoomba(packet):
    try:
        if packet[scapy.IP].src != getOwnIp(options.interface):
            response = ""
            response += re.search(r"zoomba:.*\"", str(scapy.raw(packet))).group(0)
            response = re.search(r"'.*'", response).group(0)
            response = response[1:-1]
            if(response == "I am zoomba"):
                zoomba.isFound = True
                zoomba.ip = packet[scapy.IP].src
                print("\r[+] zoomba found at " + zoomba.ip, end="")
            elif "JSON=" in response:
                response = response[5:]
                writeJson("zoombaStats.json", ast.literal_eval(response))
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

def updateJson(interface):
    while True:
        runCommand("sendJson", interface)
        time.sleep(0.1)
def runCommand(command, interface):
    if command == "clear":
        subprocess.run(["clear"])
        print("Zoomba Controller Shell")
    elif command == "exit":
        sys.exit("exiting...")
    else:
        fullCommand = "zoomba: '"+command+"'"
        packet = scapy.IP(dst = zoomba.ip, src = getOwnIp(interface)) / scapy.Raw(load=fullCommand)
        scapy.send(packet, verbose=False)
        
def writeJson(fName,data):
    with open(fName,'w') as outfile:
        json.dump(data,outfile)

if __name__ == "__main__":
    options = getOptions()
    start_new_thread(sniffForZoomba, (options.interface,))
    print("[+] Locating zoomba")
    findzoomba(options.interface)
    start_new_thread(updateJson, (options.interface, ))
    print("\nZoomba Controller Shell")
    while True:
        command = input(" >> ")
        runCommand(command, options.interface)
