from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d, simulate_static_wifi_2d, simulate_kalman_filter_live_2d
from wifi_sniffer import WifiSniffer

wifi_interface = 'wlp3s0'
wifi_monitor_interface = wifi_interface #'mon0'
simulate = False

if __name__ == "__main__":
    if simulate:
        # simulate_kalman_filter_1d()
        # simulate_kalman_filter_2d()
        # simulate_static_wifi_2d()
        simulate_kalman_filter_live_2d()
    else:
        sniffer = WifiSniffer(wifi_interface, wifi_monitor_interface)
        sniffer.get_wifi_info()
        sniffer.start_sniffing()
