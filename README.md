# Wifi-Trilateration-Kalman-Filter
WiFi Trilateration using a Kalman Filter and potential ML enhancements

## Development

### Set up Virtual Environment
To set up a virtual environment and start using the code
* `python -m virtualenv --python=python3.11 venv`
* `"./venv/Scripts/activate.bat"` (Note VS Code may automatically activate the venv for you)
* `pip install -r requirements.txt`

### Update the Requirements
If you have installed new packages while the virtual environment is active, to update `requirements.txt`
* `pip freeze > requirements.txt`

### Run the Tests
* `python -m pytest .`

## Run in Linux
For the docker image to have access to the WiFi network interface it needs to be run inside a Linux bare-metal install (like booting from a USB) not WSL or Docker on Windows
* Set up the Linux machine to run with docker
  * `sudo apt update`
  * `sudo apt install -y iw git curl`
  * `sudo apt-add-repository universe`
  * `curl -fsSL https://get.docker.com | sudo bash`
  * `sudo apt install -y docker.io aircrack-ng`
* Set up monitor mode using `airmon-ng`
  * `iwconfig` to view the network interfaces - get the wireless one (starts with wl like `wlan0` or `wlp3s0`)
  * `sudo airmon-ng start <interface>` to start monitor mode
  * `iwconfig` to view the network interfaces again - there should be a new monitor mode network (like `wlan0mon` or `mon0`) - update `start_sniffing("mon0")` if the monitor interface is different
  * `sudo iw dev <monitor-interface> set monitor none`
* (Alternative) set up monitor mode directly on the interface - but doesn't kill interfering services like `airmon-ng` does
  * `sudo ip link set <interface> down`
  * `sudo iw dev <interface> set type monitor`
  * `sudo iw dev <interface> set monitor none`
  * `sudo ip link set <interface> up`
* Clone the code to the Linux machine
  * `ssh-keygen -t ed25519 -C "<comment to identify the SSH key>"`
  * Add the SSH .pub key to Git
  * `git clone ...` (clone the repo to the machine from git)
  * `cd Wifi-Trilateration-Kalman-Filter` (enter the repo folder)
* Run the Dockerfile
  * `sudo docker build -t wifi-container .`
  * `sudo docker run --rm -i --network host --privileged wifi-container`

## Design

### Kalman Filter
I wrote and tested the Kalman Filter base, 1D and 2D implementations myself to make sure I fully understand the workings of the code - however using something like the [filterpy Kalman Filter](https://filterpy.readthedocs.io/en/latest/kalman/KalmanFilter.html) would probably make sense as a more generic filter with a more performant implementation.

#### Kalman Filter Simulations
Some simulated data to ensure the predictions (red) track the true position and velocity (blue) and uncertainty increases with subsequent predictions but decreases when we update the state with a new noisy measurement (every 10 time steps).

1D Simulation                                                     | 2D Simulation
:----------------------------------------------------------------:|:-----------------------------------------------------------------:
![1D Simulation Image](simulations/simulate_kalman_filter_1d.png) | ![2D Simulation Image](simulations/simulate_kalman_filter_2d.png)

### WiFi Sniffer
The wifi sniffer initially looks up the Wifi interfaces (could also periodically) using `iw dev <interface> scan` and then uses [scapy](https://scapy.net/) to sniff network traffic (just Beacon frames for now) to get the RSSI signal strength from each Access Point periodically.

#### WiFi Simulations
A static WiFi simulation to demonstrate the concept

![WiFi Static Simulation Image](simulations/simulate_static_wifi_2d.png)

A dynamic WiFi simulation to demonstrate the behaviour of the 2D Kalman Filter with the same inputs used in the simulation above when applied to this scenario

![WiFi Dynamic Simulation GIF](simulations/simulate_kalman_filter_live_2d.gif)

### Live Data
When running live data is captured as a CSV so that it can be played back as an animation for visualisation later. A realistic implementation of this might have multiple sniffers calling a centralised server to update positions which could be visualised live if preferred.

<!--
TODO
![WiFi Live Real Data Playback GIF](simulations/playback_live_real_data_2d.gif)
-->