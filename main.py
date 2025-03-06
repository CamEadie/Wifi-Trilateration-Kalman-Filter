#from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d
#simulate_kalman_filter_1d()

import os
from scapy.all import sniff, Dot11Beacon, Dot11ProbeReq

def packet_callback(packet):
    if (packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeReq)) and (packet.dBm_AntSignal is not None and hasattr(packet, "info")):
        # Extract Signal Strength (RSSI)
        rssi = packet.dBm_AntSignal
        ssid = packet.info
        mac = packet.addr2
        
        packetType = "Beacon" if packet.haslayer(Dot11Beacon) else "Probe"
        macType = "Access Point" if packet.haslayer(Dot11Beacon) else "Device"

        print(f"{packetType} Frame: SSID: {ssid} dBm, RSSI: {rssi}, {macType}: {mac}")

def start_sniffing(interface):
    print(f"Sniffing on interface {interface}...")
    sniff(iface=interface, prn=packet_callback, store=0)

if __name__ == "__main__":
    start_sniffing("mon0")

