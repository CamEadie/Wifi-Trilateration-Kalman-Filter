#from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d, simulate_static_wifi_2d, simulate_kalman_filter_live_2d
from wifi_sniffer import start_sniffing
import subprocess
import re

wifi_interface = 'wlp3s0'
wifi_monitor_interface = 'mon0'

def get_wifi_info(interface):
    # Run the iwlist command to scan for networks
    print(f"Running 'iwlist {interface} scan' subprocess")
    result = subprocess.run(['iwlist', interface, 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return

    # The output is a long text, so we use regex to find Tx Power and Frequency for each AP
    print(f"Output: {result.stdout}")
    scan_data = result.stdout
    networks = []
    
    # Regex pattern to extract information
    ap_pattern = r"Cell \d+ - Address: ([0-9A-F:]+).*?ESSID:\"([^\"]+)\".*?Frequency:(\d+\.\d+) GHz.*?Signal level=(-?\d+) dBm.*?Tx-Power=(\d+) dBm"
    
    matches = re.findall(ap_pattern, scan_data, re.DOTALL)

    for match in matches:
        ap_info = {
            'MAC Address': match[0],
            'SSID': match[1],
            'Frequency': match[2],  # Frequency in GHz
            'Signal Level (RSSI)': match[3],  # RSSI in dBm
            'Tx Power': match[4]  # Tx Power in dBm
        }
        networks.append(ap_info)

    return networks

if __name__ == "__main__":
    # simulate_kalman_filter_1d()
    # simulate_kalman_filter_2d()
    # simulate_static_wifi_2d()
    # simulate_kalman_filter_live_2d()

    wifi_networks = get_wifi_info(wifi_interface)

    # Print out the retrieved information
    for network in wifi_networks:
        print(f"MAC Address: {network['MAC Address']}")
        print(f"SSID: {network['SSID']}")
        print(f"Frequency: {network['Frequency']} GHz")
        print(f"Signal Level (RSSI): {network['Signal Level (RSSI)']} dBm")
        print(f"Tx Power: {network['Tx Power']} dBm")
        print("-" * 30)

    start_sniffing(wifi_monitor_interface)
