from scapy.all import sniff, Dot11Beacon, Dot11ProbeReq, Dot11ProbeResp

routers = {}

def packet_callback(packet):
    rssi = packet.dBm_AntSignal
    ssid = getattr(packet, "info", b"Hidden SSID").decode(errors="ignore")  # Handle missing SSID
    sender = packet.addr2
    receiver = packet.addr1

    match packet:
        case _ if packet.haslayer(Dot11Beacon):
            packetType = "Beacon   "
            if ssid != "Hidden SSID":
                routers[sender] = (ssid, int(rssi))
                print(f"[{sender}]: RSSI: {rssi} dBm, SSID: {ssid}")
        case _ if packet.haslayer(Dot11ProbeReq):
            packetType = "ProbeReq "
        case _ if packet.haslayer(Dot11ProbeResp):
            packetType = "ProbeResp"
        case _:
            packetType = "Other    "
    
    # if packetType != "Other    ":
    #     print(f"[{packetType}]: RSSI: {rssi} dBm, Sender: {sender}, Receiver: {receiver}, SSID: {ssid}")

def start_sniffing(interface):
    print(f"Sniffing on interface {interface}...")
    sniff(iface=interface, prn=packet_callback, store=0, monitor=True)
