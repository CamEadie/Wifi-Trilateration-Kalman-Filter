from datetime import datetime, timedelta
import time

import numpy as np
import pandas as pd

from kf import KalmanFilter2D
from kf_simulation import simulate_kalman_filter_1d, simulate_kalman_filter_2d, simulate_static_wifi_2d, simulate_kalman_filter_live_2d
from wifi_sniffer import WifiSniffer

SIMULATE = True
WIFI_INTERFACE = 'wlp3s0'

DT = 0.1
RUN_TIME_SECONDS = 100
MAX_ACCELERATION = 1.5 # 1.5m/s² is a decent estimate of max acceleration indoors
ACCELERATION_VARIANCE = MAX_ACCELERATION ** 2 / 3.0

access_point_known_positions = {
    "84:af:ec:7b:f5:99": ([0, 0], 'SORANOZAWA'),
    "00:25:36:fb:b0:4f": ([0, 35], 'SunshineKyohei1F'),
    "74:03:bd:df:95:b0": ([20, 20], 'Buffalo-G-95BE')
}

data_log = []

# Constants for RSSI to distance conversion - ML could learn accurate values or fit regression to real data
RSSI_REF = -40  # Reference RSSI at 1m
PATH_LOSS_EXPONENT = 3  # Typical values range from 2 to 4

def get_known_access_point_info():
    found_access_points = []
    while True:
        print(f"Searching for {len(access_point_known_positions) - len(found_access_points)} remaining known access point details...")
        access_points = sniffer.get_wifi_info()
        for ap in access_points:
            if ap in access_point_known_positions.keys() and ap not in found_access_points:
                found_access_points.append(ap)
        
        if len(access_point_known_positions) == len(found_access_points):
            print(f"Found all {len(found_access_points)} access points")
            break
        else:
            time.sleep(1)

def rssi_to_distance(rssi):
    return 10 ** ((RSSI_REF - rssi) / (10 * PATH_LOSS_EXPONENT))

def trilaterate(access_points, access_point_known_positions):
    positions = []
    distances = []
    distances_lookup = {}
    
    for ap in access_points:
        mac = ap['MAC Address']
        if mac in access_point_known_positions:
            positions.append(access_point_known_positions[mac][0])
            distance = rssi_to_distance(ap['Signal Level (RSSI)'])
            distances.append(distance)
            distances_lookup['MAC Address'] = distance
    
    positions = np.array(positions)
    distances = np.array(distances)
    
    if len(positions) < 3:
        raise ValueError("At least three access points are required for 2D trilateration")

    # Constructing A and b for least squares Ax = b
    A = -2 * (positions[:-1] - positions[-1])
    b = distances[:-1]**2 - distances[-1]**2 + np.sum(positions[-1]**2) - np.sum(positions[:-1]**2, axis=1)
    
    # Least squares solution - considered scipy.optimize.least_squares but this is faster for a linear solution
    estimated_position = np.linalg.lstsq(A, b, rcond=None)[0]

    # Compute Jacobian
    J = np.array([
        [2 * (estimated_position[0] - x), 2 * (estimated_position[1] - y)]
        for x, y in positions
    ])

    # Measurement noise covariance (assuming small Gaussian noise on RSSI-derived distances)
    sigma_rssi = 10  # Estimated RSSI noise in dBm
    distance_noise = (np.log(10) / (10 * PATH_LOSS_EXPONENT)) * distances * sigma_rssi
    R = np.diag(distance_noise ** 2)

    J_inv = np.linalg.pinv(J.T @ J) @ J.T  # Pseudo-inverse of J for stability
    cov = J_inv @ R @ J_inv.T

    return estimated_position[0], estimated_position[1], cov, distances_lookup

if __name__ == "__main__":
    if SIMULATE:
        # simulate_kalman_filter_1d()
        # simulate_kalman_filter_2d()
        # simulate_static_wifi_2d()
        simulate_kalman_filter_live_2d()
    else:
        sniffer = WifiSniffer(WIFI_INTERFACE)
        get_known_access_point_info(sniffer)

        current_known_access_points = [ap for ap in sniffer.access_points.values() if ap['MAC Address'] in access_point_known_positions.keys()]
        x, y, _ = trilaterate(current_known_access_points, access_point_known_positions)
        my_device = KalmanFilter2D(initial_x=x, 
                                   initial_y=x, 
                                   initial_v_x=0.0, 
                                   initial_v_y=0.0, 
                                   acceleration_variance=ACCELERATION_VARIANCE)

        sniffer.start_sniffing()
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=RUN_TIME_SECONDS)
        last_updated = datetime.now()

        while True:
            current_known_access_points = [ap for ap in sniffer.access_points.values() if ap['MAC Address'] in access_point_known_positions.keys()]
            # Updated within the last second (recent data) and after the last update (new data)
            new_update_access_points = [ap for ap in current_known_access_points if 
                                        ap['Last Updated'] > datetime.now() - timedelta(seconds=1) and
                                        ap['Last Updated'] > last_updated]
            
            my_device.predict(DT)
            if len(new_update_access_points) >= 3:
                x, y, cov, distances = trilaterate(current_known_access_points, access_point_known_positions)
                my_device.update([x, y], cov)
            
            # Log data
            log_entry = {"timestamp": datetime.now(), "x": x, "y": y, **distances}
            data_log.append(log_entry)

            if end_time < datetime.now():
                sniffer.stop_sniffing()
                break

            time.sleep(DT)
        
        # Save data to CSV
        df = pd.DataFrame(data_log)
        csv_label = f"wifi_tracking_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        df.to_csv(f"live_data/{csv_label}", index=False)
        print(f"Data saved to {csv_label}")
