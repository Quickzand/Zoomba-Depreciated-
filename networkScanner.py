#!/usr/bin/env python3

import scapy.all as scapy
import argparse

def getOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--t", dest="target", help="Option to set the target of the scan (required)")
    options = parser.parse_args()
    if not options.target:
        parser.error("A target is required, use --help for more info")

    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    (answered, unanswered) = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    list = []
    for element in answered:
        dict = {"mac":element[1].hwsrc, "ip":element[1].psrc}
        list.append(dict)
    return list

def printData(data):
    print("IP\t\t\tMAC\n-----------------------------------------")
    for dict in data:
        print(dict["ip"]+"\t\t"+dict["mac"])

if __name__ == "__main__":
    options = getOptions()
    printData(scan(options.target))
