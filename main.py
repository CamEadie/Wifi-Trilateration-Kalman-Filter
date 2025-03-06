#from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d
#simulate_kalman_filter_1d()

from scapy.all import sniff, Dot11Beacon, Dot11ProbeReq

def packet_callback(packet):
    print("sniff")
    if packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeReq):
        rssi = getattr(packet, "dBm_AntSignal", "N/A")  # Handle missing RSSI
        ssid = getattr(packet, "info", b"Hidden SSID").decode(errors="ignore")  # Handle missing SSID
        mac = packet.addr2

        packetType = "Beacon" if packet.haslayer(Dot11Beacon) else "Probe"
        macType = "Access Point" if packet.haslayer(Dot11Beacon) else "Device"

        print(f"[{packetType}] Frame: SSID: {ssid} dBm, RSSI: {rssi}, {macType}: {mac}")

def start_sniffing(interface):
    print(f"Sniffing on interface {interface}...")
    sniff(iface=interface, prn=packet_callback, store=0, monitor=True)

if __name__ == "__main__":
    start_sniffing("mon0")

