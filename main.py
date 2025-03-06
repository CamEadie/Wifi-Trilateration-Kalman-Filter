#from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d
#simulate_kalman_filter_1d()

from scapy.all import sniff, Dot11Beacon, Dot11ProbeReq, Dot11ProbeResp

def packet_callback(packet):
    rssi = getattr(packet, "dBm_AntSignal", "N/A")  # Handle missing RSSI
    ssid = getattr(packet, "info", b"Hidden SSID").decode(errors="ignore")  # Handle missing SSID
    sender = packet.addr2
    receiver = packet.addr1

    if packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeReq) or packet.haslayer(Dot11ProbeResp):
        packetType = "Beacon   " if packet.haslayer(Dot11Beacon) else "ProbeReq " if packet.haslayer(Dot11ProbeReq) else "ProbeResp"
        print(f"[{packetType}]: RSSI: {rssi} dBm, Sender: {sender}, Receiver: {receiver}, SSID: {ssid}")
    else:
        print(f"[Other    ]: RSSI: {rssi} dBm, Sender: {sender}, Receiver: {receiver}, SSID: {ssid}")

def start_sniffing(interface):
    print(f"Sniffing on interface {interface}...")
    sniff(iface=interface, prn=packet_callback, store=0, monitor=True)

if __name__ == "__main__":
    start_sniffing("mon0")

