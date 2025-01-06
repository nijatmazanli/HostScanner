#!/usr/bin/env -S python3 -W ignore
import argparse
import re
import subprocess
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

from colorama import Fore, init, Style

# Colorama Colors
init()


def ncScan(ipList):
    for i in ipList:
        i = i.replace("\n", "")
        print(
            infoColor + "     |\n     |-----> Scanning :: " + Style.RESET_ALL + i + " :" + portNumColor + ports + Style.RESET_ALL)
        ncScanCommand = "nc -nv -w 4 -z " + i + " " + ports + "> data/Results/ncScanResults" + i + ".txt 2>&1"
        ncScanCmd = subprocess.run(ncScanCommand, shell=True)

        file = open("data/Results/ncScanResults" + i + ".txt", "r")
        file = file.readlines()
        matches = []
        for line in file:
            line = line.replace("\n", "")
            founded = re.findall("\[.*?\] (\d+) \((.*?)\) open", line)
            matches.append(founded)
            if founded:
                print(infoColor, "            |----> Open port:", successColor, founded[0][0], infoColor, " Service:",
                      successColor, founded[0][1], Style.RESET_ALL, )


def writeIPs(ipList):
    allIPs = open("data/all_IPs.csv", "a")
    for i in ipList:
        allIPs.writelines(i)
    allIPs.close()


errColor = Fore.RED
errMessage = Fore.LIGHTRED_EX
testColor = Fore.MAGENTA
infoColor = Fore.CYAN
successColor = Fore.GREEN
warningColor = Fore.YELLOW
portNumColor = Fore.LIGHTCYAN_EX

# Parser
parser = argparse.ArgumentParser(description="Network Scanner using Netcat",
                               usage="Scanner.py <targets> <ports>\n\nExample:\nScanner.py 192.168.0.1 21,25,80,443,1")
parser.add_argument("targets",type=str, nargs='+',help="Target IPs of hostnames (or just hostnames or IP range like \24 \16")
parser.add_argument("ports",type=str, nargs='+',help="Port numbers of hostnames")
parsedData = parser.parse_args()
print(parsedData)

# Get Argunments
hosts = ""
ports = ""

try:
    targetIP = parsedData.targets[0].split(",")
    for host in targetIP:
        hosts += " " + host

except IndexError:
    targetIP = []

try:
    targetPorts = parsedData.ports[0].split(",")
    for port in targetPorts:
        ports += " " + port

except IndexError:
    targetPorts = []

# Nmap Scanning part. Filtering and writing them to ip-list.txt file part
nmapScanCommand = "nmap " + hosts + " -sn -n -oG - | awk '/Up$/{print $2}' > ip-list.txt"
subprocess.run([nmapScanCommand], stdout=subprocess.PIPE, shell=True)

ipList = open("ip-list.txt", "r")
ipList = ipList.readlines()
writeIPs(ipList)

if ipList == []:
    print(warningColor + "[*] Warning:" + Style.RESET_ALL + "No active host found.")

else:
    print(infoColor + "[+] Founded Hosts: " + Style.RESET_ALL)
    for i in ipList:
        print(infoColor + "     |-----> " + Style.RESET_ALL + i, end="")

# NetCat scanning part.
print(infoColor, "[*] Scanning ports")
ncScan(ipList)
