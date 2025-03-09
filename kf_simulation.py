import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
    routers = [(5, 5, 'WiFi 1'), 
               (10, 35, 'WiFi 2'), 
               (45, 10, 'WiFi 3')]
    for rx, ry, label in routers:
        plot_router(ax, rx, ry, label_space_x, label_space_y, label)   

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
    meas_variance = np.array([[0.5, 0.05], [0.05, 0.5]])

    kf = KalmanFilter2D(initial_x=x, initial_y=y, initial_v_x=v_x, initial_v_y=v_y, acceleration_variance=a)

    DT = 0.1
    NUM_STEPS = 1000
    MEAS_EVERY_STEPS = 10

    label_space_x = (max_x - min_x) / 100.0
    label_space_y = (max_y - min_y) / 100.0

    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=110)

    device_scatter, device_text, device_distribution = plot_device(ax, x, y, kf.cov[:2, :2], space, label_space_x, label_space_y, "Cam Phone")
    
    router_scatters = []
    router_texts = []
    # Plot static WiFi routers
    routers = [(5, 5, 'WiFi 1'), 
               (10, 35, 'WiFi 2'), 
               (45, 10, 'WiFi 3')]
    for rx, ry, label in routers:
        router_scatter, router_text = plot_router(ax, rx, ry, label_space_x, label_space_y, label)
        router_scatters.append(router_scatter)
        router_texts.append(router_text)

    heatmap = ax.imshow(device_distribution, extent=(min_x, max_x, min_y, max_y), origin='lower', cmap='plasma', alpha=0.7)
    plt.colorbar(heatmap, label='Probability Density')

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
            kf.update(meas_value=[
                real_x + np.random.default_rng().standard_normal() * np.sqrt(meas_variance[0, 0]),
                real_y + np.random.default_rng().standard_normal() * np.sqrt(meas_variance[1, 1])
            ], meas_variance=meas_variance)

        
        # Update the device's scatter position
        device_scatter.set_offsets([[kf.mean[0], kf.mean[1]]])

        # Update the label position
        device_text.set_position((kf.mean[0] + label_space_x, kf.mean[1] + label_space_y))

        # Update the uncertainty distribution
        distribution = multivariate_normal(mean=[kf.mean[0], kf.mean[1]], cov=kf.cov[:2, :2]).pdf(space)
        distribution /= distribution.max()
        heatmap.set_array(distribution)

        return *router_scatters, *router_texts, device_scatter, device_text, heatmap

    # DT * 100 instead of DT * 1000 so we cover the 100s of motion in 10s of animation
    ani = animation.FuncAnimation(fig, update, frames=NUM_STEPS, interval=DT * 100, blit=True)

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Live Kalman Filter 2D Tracking')
    
    # Save as GIF
    # ani.save("simulations/simulate_kalman_filter_live_2d.gif", writer="pillow", fps=10)

    plt.show()
