# HostScanner
This tool uses system commands to perform port scanning on the given hosts and IP addresses

## Usage
First of all, we need to install libraries and code: 
```bash 
git clone https://github.com/nijatmazanli/HostScanner.git
pip3 install argparse subprocess
chmod +x Scanner.py
./Scanner.py -h 
```

For now, providing host names and target ports enough to run proper scan.
```bash
./Scanner.py 192.168.0.1/24 80,22,21,23
```

## What is going in background
In background, program uses tool named ```nmap```. The full command is ```  "nmap " + hosts + " -sn -n -oG - | awk '/Up$/{print $2}' > ip-list.txt" ```.
In the host place filled with hosts or IPs or IP ranges that given by you. The command will find which IPs are active and saves active IPs to file named ```ip-list.txt```.

After detecting active IPs, ```nc``` command starts to find active ports that given by you. The full command is  ``` "nc -nv -w 4 -z " + i + " " + ports + "> data/Results/ncScanResults" + i + ".txt 2>&1"```.
This commands performs port scanning and saves the output to specific file. With this file, python code can show which ports are open.

## Future improvements
I am actually thinking about automation of banner grabbing and adding more flexibility for users. Still working on them. 
