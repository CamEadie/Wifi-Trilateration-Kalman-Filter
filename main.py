#from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d
#simulate_kalman_filter_1d()

import os
from scapy.all import sniff, Dot11

def packet_callback(packet):
    if packet.haslayer(Dot11):
        # Extract Signal Strength (RSSI)
        rssi = packet.dBm_AntSignal if packet.dBm_AntSignal is not None else "N/A"

        ssid = packet.info.decode() if packet.info else "Hidden SSID"
        mac = packet[Dot11].addr2 if packet[Dot11] else "No MAC"

        # Check Beacon frames (WiFi Routers advertising)
        if packet.type == 0 and packet.subtype == 8:
            print(f"Beacon Frame: SSID: {ssid} dBm, RSSI: {rssi}, Access Point: {mac}")
        # Check Probe frames (Devices looking for WiFi Routers)
        elif packet.type == 0 and packet.subtype == 4:
            print(f"Probe Frame: SSID: {ssid} dBm, RSSI: {rssi}, Device: {mac}")

def start_sniffing(interface="wlan0mon"):
    print(f"Sniffing on interface {interface}...")
    sniff(iface=interface, prn=packet_callback, store=0)

if __name__ == "__main__":
    interface = "wlp3s0"
    monitor_interface = "mon1"
    #os.system(f"airmon-ng start {interface}")
    start_sniffing(monitor_interface)

