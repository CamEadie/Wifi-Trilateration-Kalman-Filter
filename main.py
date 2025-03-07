#from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d, simulate_static_wifi_2d, simulate_kalman_filter_live_2d
from wifi_sniffer import start_sniffing
import subprocess
import re

wifi_interface = 'wlp3s0'
wifi_monitor_interface = 'mon0'

def get_wifi_info(interface):
    # Run the iwlist command to scan for networks
    print(f"Running 'iw dev {interface} scan' subprocess")
    result = subprocess.run(['iw', 'dev', interface, 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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
            'Frequency': match[1], # Frequency in MHz
            'Signal Level (RSSI)': match[2],  # RSSI in dBm
            'SSID': match[3]
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
        print("-" * 30)

    start_sniffing(wifi_monitor_interface)
