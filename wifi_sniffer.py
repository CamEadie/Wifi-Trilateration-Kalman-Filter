import os
import re
import subprocess
import time
from datetime import datetime
from threading import Thread, Event

from scapy.all import sniff, Dot11Beacon, Dot11ProbeReq, Dot11ProbeResp

class WifiSniffer:
    def __init__(self, interface):
        self._access_points = {}
        self.interface = interface
        self.running = False
        self.stop_event = Event()
    
    @property
    def access_points(self) -> dict:
        return self._access_points
    
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
                'Signal Level (RSSI)': float(match[2]),  # RSSI in dBm
                'SSID': match[3],
                'Last Updated': datetime.now()
            }
            self._access_points[match[0]] = ap_info
            networks.append(ap_info)
            print(f"[Lookup   ]: RSSI: {match[2]} dBm, Sender: {match[0]}, SSID: {match[3]}")
        print(f"{'-'*10} Lookup Complete {'-'*10}")
        return networks
    
    def _channel_hopper(self):
        channels_2g = list(range(1, 14))
        channels_5g = list(range(36, 65, 4)) #+ list(range(100, 141, 4)) + list(range(149, 166, 4))
        channels = channels_2g + channels_5g

        while not self.stop_event.is_set():
            for channel in channels:
                os.system(f"iw dev {self.interface} set channel {channel}")
                time.sleep(0.1)

    def _packet_callback(self, packet):
        if not self.running:
            raise KeyboardInterrupt # This stops `sniff()`
        
        rssi = packet.dBm_AntSignal
        ssid = getattr(packet, "info", b"Hidden SSID").decode(errors="ignore")  # Handle missing SSID
        sender = packet.addr2
        receiver = packet.addr1

        match packet:
            case _ if packet.haslayer(Dot11Beacon):
                packetType = "Beacon   "
                if ssid != "Hidden SSID" and sender in self._access_points.keys():
                    # TODO Update Frequency in case it changes
                    self._access_points[sender]['Signal Level (RSSI)'] = float(rssi)
                    self._access_points[sender]['SSID'] = ssid
                    self._access_points[sender]['Last Updated'] = datetime.now()
            case _ if packet.haslayer(Dot11ProbeReq):
                packetType = "ProbeReq "
            case _ if packet.haslayer(Dot11ProbeResp):
                packetType = "ProbeResp"
            case _:
                packetType = "Other    "
        
        if packetType != "Other    ":
            print(f"[{packetType}]: RSSI: {rssi} dBm, Sender: {sender}, Receiver: {receiver}, SSID: {ssid}")

    def _run_sniffer(self):
        try:
            print("Starting channel hopper...")
            Thread(target=self._channel_hopper, daemon=True).start()
            print(f"Sniffing on interface {self.interface}...")
            sniff(iface=self.interface, prn=self._packet_callback, store=0, monitor=True)
        except KeyboardInterrupt:
            print("Sniffing stopped.")

    def start_sniffing(self):
        if self.running:
            print("Sniffer is already running.")
            return

        self.running = True
        self.stop_event.clear()
        
        self.sniff_thread = Thread(target=self._run_sniffer, daemon=True)
        self.sniff_thread.start()

    def stop_sniffing(self):
        if not self.running:
            print("Sniffer is not running.")
            return

        print("Stopping sniffer...")
        self.running = False
        self.stop_event.set()
