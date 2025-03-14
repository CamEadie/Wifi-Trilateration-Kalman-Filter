from datetime import datetime
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import pandas as pd
from scipy.stats import multivariate_normal

from kf import KalmanFilter1D, KalmanFilter2D

def simulate_kalman_filter_1d():
    plt.figure(figsize=(11.5, 6.5), dpi=110)

    x = 0.2
    v = 0.3
    a = 1.2

    real_x = 0.0
    real_v = 0.5
    meas_variance = 0.1

    kf = KalmanFilter1D(initial_x=x, initial_v=v, acceleration_variance=a)

    DT = 0.1
    NUM_STEPS = 1000
    MEAS_EVERY_STEPS = 10

    mus = []
    covs = []
    real_xs = []
    real_vs = []

    for step in range(NUM_STEPS):
        mus.append(kf.mean)
        covs.append(kf.cov)

        if step > 500:
            real_v *= 0.98
        
        real_x = real_x + DT * real_v

        kf.predict(dt=DT)
        if step != 0 and step % MEAS_EVERY_STEPS == 0:
            kf.update(meas_value=real_x + np.random.default_rng().standard_normal() * np.sqrt(meas_variance),
                    meas_variance=meas_variance)
            
        real_xs.append(real_x)
        real_vs.append(real_v)

    plt.subplot(2, 1, 1)
    plt.title('Position')
    plt.plot([mu[0] for mu in mus], 'r')
    plt.plot(real_xs, 'b')
    plt.plot([mu[0] + 2 * np.sqrt(cov[0, 0]) for mu, cov in zip(mus, covs)], 'r--')
    plt.plot([mu[0] - 2 * np.sqrt(cov[0, 0]) for mu, cov in zip(mus, covs)], 'r--')

    plt.subplot(2, 1, 2)
    plt.title('Velocity')
    plt.plot([mu[1] for mu in mus], 'r')
    plt.plot(real_vs, 'b')
    plt.plot([mu[1] + 2 * np.sqrt(cov[1, 1]) for mu, cov in zip(mus, covs)], 'r--')
    plt.plot([mu[1] - 2 * np.sqrt(cov[1, 1]) for mu, cov in zip(mus, covs)], 'r--')

    # Save the plot as an image
    # plt.savefig("simulations/simulate_kalman_filter_1d.png", dpi=300, bbox_inches="tight")

    plt.show()

def simulate_kalman_filter_2d():
    plt.figure(figsize=(11.5, 6.5), dpi=110)

    x = 0.2
    y = 0.2
    v_x = 0.0
    v_y = 0.1
    a = 1.2

    real_x = 0.0
    real_y = 0.0
    real_v_x = 0.5
    real_v_y = 0.5
    meas_variance = np.array([[0.1, 0.01], [0.01, 0.1]])

    kf = KalmanFilter2D(initial_x=x, initial_y=y, initial_v_x=v_x, initial_v_y=v_y, acceleration_variance=a)

    DT = 0.1
    NUM_STEPS = 1000
    MEAS_EVERY_STEPS = 10

    mus = []
    covs = []
    real_xs = []
    real_ys = []
    real_v_xs = []
    real_v_ys = []

    for step in range(NUM_STEPS):
        mus.append(kf.mean)
        covs.append(kf.cov)

        if 250 < step and step < 500:
            real_v_x *= 1.005
        elif step == 500:
            real_v_y *= -1
        elif 500 < step:
            real_v_x *= 0.98
        
        real_x = real_x + DT * real_v_x
        real_y = real_y + DT * real_v_y

        kf.predict(dt=DT)
        if step != 0 and step % MEAS_EVERY_STEPS == 0:
            kf.update(meas_value=[
                        real_x + np.random.default_rng().standard_normal() * np.sqrt(meas_variance[0, 0]),
                        real_y + np.random.default_rng().standard_normal() * np.sqrt(meas_variance[1, 1])
                       ],
                      meas_variance=meas_variance)
            
        real_xs.append(real_x)
        real_ys.append(real_y)
        real_v_xs.append(real_v_x)
        real_v_ys.append(real_v_y)

    plt.subplot(2, 2, 1)
    plt.title('Position (x)')
    plt.plot([mu[0] for mu in mus], 'r')
    plt.plot(real_xs, 'b')
    plt.plot([mu[0] + 2 * np.sqrt(cov[0, 0]) for mu, cov in zip(mus, covs)], 'r--')
    plt.plot([mu[0] - 2 * np.sqrt(cov[0, 0]) for mu, cov in zip(mus, covs)], 'r--')

    plt.subplot(2, 2, 2)
    plt.title('Position (y)')
    plt.plot([mu[1] for mu in mus], 'r')
    plt.plot(real_ys, 'b')
    plt.plot([mu[1] + 2 * np.sqrt(cov[1, 1]) for mu, cov in zip(mus, covs)], 'r--')
    plt.plot([mu[1] - 2 * np.sqrt(cov[1, 1]) for mu, cov in zip(mus, covs)], 'r--')

    plt.subplot(2, 2, 3)
    plt.title('Velocity (x)')
    plt.plot([mu[2] for mu in mus], 'r')
    plt.plot(real_v_xs, 'b')
    plt.plot([mu[2] + 2 * np.sqrt(cov[2, 2]) for mu, cov in zip(mus, covs)], 'r--')
    plt.plot([mu[2] - 2 * np.sqrt(cov[2, 2]) for mu, cov in zip(mus, covs)], 'r--')

    plt.subplot(2, 2, 4)
    plt.title('Velocity (y)')
    plt.plot([mu[3] for mu in mus], 'r')
    plt.plot(real_v_ys, 'b')
    plt.plot([mu[3] + 2 * np.sqrt(cov[3, 3]) for mu, cov in zip(mus, covs)], 'r--')
    plt.plot([mu[3] - 2 * np.sqrt(cov[3, 3]) for mu, cov in zip(mus, covs)], 'r--')

    # Save the plot as an image
    # plt.savefig("simulations/simulate_kalman_filter_2d.png", dpi=300, bbox_inches="tight")

    plt.show()

def plot_device(ax, x, y, cov, space, label_space_x, label_space_y, label):
    scatter = ax.scatter(x, y, color='black', s=20)
    text = ax.text(x + label_space_x, 
                   y + label_space_y, 
                   label, 
                   color='black',
                   fontsize=12, 
                   weight='bold', 
                   bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.1'))
    distribution = multivariate_normal(mean=[x, y], cov=cov).pdf(space)
    distribution /= distribution.max()
    return scatter, text, distribution

def plot_router(ax, x, y, label_space_x, label_space_y, label):
    scatter = ax.scatter(x, y, marker="^", color="red")
    text = ax.text(x + label_space_x, 
                   y + label_space_y, 
                   label, color='black', 
                   fontsize=12, 
                   weight='bold', 
                   bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.1'))
    return scatter, text

def simulate_static_wifi_2d():
    min_x, max_x, min_y, max_y = 0, 50, 0, 40
    granularity = 300
    x, y = np.linspace(min_x, max_x, granularity), np.linspace(min_y, max_y, granularity)
    X, Y = np.meshgrid(x, y)
    space = np.dstack((X, Y))

    # Plot the combined Gausians
    _, ax = plt.subplots(figsize=(11.5, 6.5), dpi=110)
    label_space_x = (max_x - min_x) / 100.0
    label_space_y = (max_y - min_y) / 100.0

    # Mark and label both means
    distributions = []
    devices = [(25, 25, [[10, 4], [4, 2]], 'Cam Phone'), 
               (40, 15, [[6, -2], [-2, 8]], 'Cam Laptop')]
    for dx, dy, cov, label in devices:
        _, _, device_distribution = plot_device(ax, dx, dy, cov, space, label_space_x, label_space_y, label)
        distributions.append(device_distribution)

    distribution = np.sum(distributions, axis=0)
    distribution /= distribution.max()

    heatmap = ax.imshow(distribution, extent=(min_x, max_x, min_y, max_y), origin='lower', cmap='plasma', alpha=0.7)
    plt.colorbar(heatmap, label='Probability Density')

    # Mark and label 3 WiFi Routers    
    routers = [([5, 5], 'WiFi 1'), 
               ([10, 35], 'WiFi 2'), 
               ([45, 10], 'WiFi 3')]
    for pos, label in routers:
        plot_router(ax, pos[0], pos[1], label_space_x, label_space_y, label)

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    plt.title('Device Location Estimation as 2D Gaussian Kernels')

    # Save the plot as an image
    # plt.savefig("simulations/simulate_static_wifi_2d.png", dpi=300, bbox_inches="tight")

    plt.show()

def simulate_kalman_filter_live_2d():
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np

    min_x, max_x, min_y, max_y = 0, 60, -5, 40
    granularity = 300
    x, y = np.linspace(min_x, max_x, granularity), np.linspace(min_y, max_y, granularity)
    X, Y = np.meshgrid(x, y)
    space = np.dstack((X, Y))

    # Initialize the Kalman filter
    x = 0.2
    y = 10.2
    v_x = 0.0
    v_y = 0.1
    a = 1.2
    real_x = 0.0
    real_y = 10.0
    real_v_x = 0.5
    real_v_y = 0.5

    kf = KalmanFilter2D(initial_x=x, initial_y=y, initial_v_x=v_x, initial_v_y=v_y, acceleration_variance=a)

    DT = 0.1
    NUM_STEPS = 1000
    MEAS_EVERY_STEPS = 10
    PATH_LOSS_EXPONENT = 3  # Typical values range from 2 to 4

    label_space_x = (max_x - min_x) / 100.0
    label_space_y = (max_y - min_y) / 100.0

    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=110)

    device_scatter, device_text, device_distribution = plot_device(ax, x, y, kf.cov[:2, :2], space, label_space_x, label_space_y, "Cam Phone")
    
    data_log = []

    router_scatters = []
    router_texts = []
    router_circles = []
    # Plot static WiFi routers
    routers = [([5, 5], 'WiFi 1'), 
               ([10, 35], 'WiFi 2'), 
               ([45, 10], 'WiFi 3')]
    for pos, label in routers:
        router_scatter, router_text = plot_router(ax, pos[0], pos[1], label_space_x, label_space_y, label)
        router_scatters.append(router_scatter)
        router_texts.append(router_text)
        router_circle = patches.Circle((pos[0], pos[1]), radius=0, color='red', fill=False)
        ax.add_patch(router_circle)
        router_circles.append(router_circle)

    heatmap = ax.imshow(device_distribution, extent=(min_x, max_x, min_y, max_y), origin='lower', cmap='plasma', alpha=0.7)
    plt.colorbar(heatmap, label='Probability Density')

    distances = {label: 0 for _, label in routers}

    def update(frame):
        nonlocal real_x, real_y, real_v_x, real_v_y
        
        # Simulate real motion
        if 250 < frame < 500:
            real_v_x *= 1.005
        elif frame == 500:
            real_v_y *= -1
        elif frame > 500:
            real_v_x *= 0.98
        
        real_x += DT * real_v_x
        real_y += DT * real_v_y

        # Kalman filter prediction and update
        kf.predict(dt=DT)
        if frame != 0 and frame % MEAS_EVERY_STEPS == 0:
            real_position = np.array([real_x, real_y])

            positions = [np.array(router[0]) for router in routers]
            noisy_distances = [math.hypot(*(real_position - router[0])) + np.random.default_rng().standard_normal() for router in routers]

            for circle, distance, router in zip(router_circles, noisy_distances, routers):
                circle.set_radius(distance)
                distances[router[1]] = distance

            positions = np.array(positions)
            noisy_distances = np.array(noisy_distances)

            # Constructing A and b for least squares Ax = b
            A = -2 * (positions[:-1] - positions[-1])
            b = noisy_distances[:-1]**2 - noisy_distances[-1]**2 + np.sum(positions[-1]**2) - np.sum(positions[:-1]**2, axis=1)
            
            # Least squares solution - considered scipy.optimize.least_squares but this is faster for a linear solution
            estimated_position = np.linalg.lstsq(A, b, rcond=None)[0]

            # Compute Jacobian
            J = np.array([
                [2 * (estimated_position[0] - x), 2 * (estimated_position[1] - y)]
                for x, y in positions
            ])

            # Measurement noise covariance (assuming small Gaussian noise on RSSI-derived distances)
            sigma_rssi = 10  # Estimated RSSI noise in dBm
            distance_noise = (np.log(10) / (10 * PATH_LOSS_EXPONENT)) * noisy_distances * sigma_rssi
            R = np.diag(distance_noise ** 2)

            J_inv = np.linalg.pinv(J.T @ J) @ J.T  # Pseudo-inverse of J for stability
            cov = J_inv @ R @ J_inv.T
            
            kf.update(meas_value=[
                estimated_position[0],
                estimated_position[1]
            ], meas_variance=cov * 10) # x10 so it's easier to see for the demo's sake

        # Update the device's scatter position
        device_scatter.set_offsets([[kf.mean[0], kf.mean[1]]])

        # Update the label position
        device_text.set_position((kf.mean[0] + label_space_x, kf.mean[1] + label_space_y))

        # Update the uncertainty distribution
        distribution = multivariate_normal(mean=[kf.mean[0], kf.mean[1]], cov=kf.cov[:2, :2]).pdf(space)
        distribution /= distribution.max()
        heatmap.set_array(distribution)
        
        # Log data
        log_entry = {"timestamp": frame, "x": kf.pos_x, "y": kf.pos_y, **distances}
        data_log.append(log_entry)

        return *router_scatters, *router_texts, device_scatter, device_text, *router_circles, heatmap

    ani = animation.FuncAnimation(fig, update, frames=NUM_STEPS, interval=DT, blit=False, repeat=False)

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Live Kalman Filter 2D Tracking')
    
    # Save as GIF
    # ani.save("simulations/simulate_kalman_filter_live_2d.gif", writer="pillow", fps=10)
    
    plt.show()

    # Save data to CSV
    df = pd.DataFrame(data_log)
    csv_label = "wifi_tracking_log_simulated.csv"
    df.to_csv(f"live_data/{csv_label}", index=False)
    print(f"Data saved to {csv_label}")
    