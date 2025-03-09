from scapy.all import sniff, Dot11Beacon, Dot11ProbeReq, Dot11ProbeResp
import subprocess
import re
from datetime import datetime, timedelta
import os
import time
from threading import Thread

class WifiSniffer:
    def __init__(self, interface, monitor_interface):
        self.routers = {}
        self.interface = interface
        self.monitor_interface = monitor_interface
    
    @property
    def routers(self) -> dict:
        return self.routers
    
    def get_wifi_info(self):
        # Run the iwlist command to scan for networks
        print(f"Running 'iw dev {self.interface} scan' subprocess")
        result = subprocess.run(['iw', 'dev', self.interface, 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return

        # Use regex to find Frequency for each AP
        scan_data = result.stdout
        networks = []

        # Regex pattern to extract information
        ap_pattern = r"(?s)BSS ([0-9a-f:]+).*?freq: (\d+).*?signal: (-?\d+.\d+) dBm.*?SSID: *([^\r\n]*\S)"

        matches = re.findall(ap_pattern, scan_data, re.DOTALL)

        for match in matches:
            ap_info = {
                'MAC Address': match[0],
                'Frequency': int(match[1]), # Frequency in MHz
                'Signal Level (RSSI)': int(match[2]),  # RSSI in dBm
                'SSID': match[3],
                'Last Updated': datetime.now()
            }
            self.routers[match[0]] = ap_info
            networks.append(ap_info)
            print(f"[Lookup   ]: RSSI: {match[2]} dBm, Sender: {match[0]}, SSID: {match[3]}")
        print(f"{'-'*10} Lookup Complete {'-'*10}")
        return networks
    
    def channel_hopper(self):
        channels_2g = list(range(1, 14))
        channels_5g = [64]#list(range(36, 65, 4)) + list(range(100, 141, 4)) + list(range(149, 166, 4))
        channels = channels_2g + channels_5g

        while True:
            for channel in channels:
                os.system(f"iw dev {self.interface} set channel {channel}")
                time.sleep(0.1)

    def packet_callback(self, packet):
        rssi = packet.dBm_AntSignal
        ssid = getattr(packet, "info", b"Hidden SSID").decode(errors="ignore")  # Handle missing SSID
        sender = packet.addr2
        receiver = packet.addr1

        match packet:
            case _ if packet.haslayer(Dot11Beacon):
                packetType = "Beacon   "
                if ssid != "Hidden SSID" and sender in self.routers.keys():
                    self.routers[sender]['Signal Level (RSSI)'] = rssi
                    self.routers[sender]['SSID'] = ssid
                    self.routers[sender]['Last Updated'] = datetime.now()
            case _ if packet.haslayer(Dot11ProbeReq):
                packetType = "ProbeReq "
            case _ if packet.haslayer(Dot11ProbeResp):
                packetType = "ProbeResp"
            case _:
                packetType = "Other    "
        
        if packetType != "Other    ":
            print(f"[{packetType}]: RSSI: {rssi} dBm, Sender: {sender}, Receiver: {receiver}, SSID: {ssid}")

    def start_sniffing(self, interface):
        print(f"Sniffing on interface {interface}...")
        Thread(target=self.channel_hopper, daemon=True).start()
        sniff(iface=interface, prn=self.packet_callback, store=0, monitor=True)
