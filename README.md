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