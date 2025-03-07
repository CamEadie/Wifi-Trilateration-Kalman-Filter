# Wifi-Trilateration-Kalman-Filter
WiFi Trilateration using a Kalman Filter and potential ML enhancements

## Setup Virtual Environment
To setup a virtual environment and start using the code
* `python -m virtualenv --python=python3.11 venv`
* `"./venv/Scripts/activate.bat"` (Note VS Code may automatically activate the venv for you)
* `pip install -r requirements.txt`

## Update the Requirements
If you have installed new packages while the virtual environment is active, to update `requirements.txt`
* `pip freeze > requirements.txt`

## Run the Tests
* `python -m pytest .`

## Run in Linux
Requires Linux with access to WiFi network so bare-metal install (like booting from a USB) not WSL or Docker
* Setup the Linux machine to run with docker
  * `sudo apt update && sudo apt upgrade -y`
  * `sudo apt install -y iw git curl`
  * `curl -fsSL https://get.docker.com | sudo bash`
  * `sudo apt-add-repository universe`
  * `sudo apt install -y docker.io aircrack-ng`
* Set up monitor mode using `airmon-ng`
  * `iwconfig` to view the network interfaces - get the wireless one (starts with wl like `wlan0` or `wlp3s0`)
  * `sudo airmon-ng start <interface>` to start monitor mode
  * `iwconfig` to view the network interfaces again - there should be a new monitor mode network (like `wlan0mon` or `mon0`) - update `start_sniffing("mon0")` if the monitor interface is different
* (Alternative) set up monitor mode directly on the interface - but doesn't kill interfering services like `airmon-ng` does
  * `sudo ip link set <interface> down`
  * `sudo iw dev <interface> set type monitor`
  * `sudo ip link set <interface> up`
* Clone the code to the Linux machine
  * `git clone ...` (clone the repo to the machine from git)
  * `cd Wifi-Trilateration-Kalman-Filter` (enter the repo folder)
* Run the Dockerfile
  * `sudo docker build -t wifi-container .`
  * `sudo docker run --rm -i --network host --privileged wifi-container`
