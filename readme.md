# Mac Webcam Automation

This project automates actions based on the status of your Mac's webcam. It uses a combination of Python scripts and a launch daemon to monitor the webcam's power state and perform specified actions when the webcam is activated or deactivated.
I use this to switch the color of my background Govee LEDs to a white when the webcam is active and back to yellow when camera is off.

## Files

- `webcam_active_script.py`: Contains the logic for performing actions when the webcam is active or inactive. In this example uses the Govee local API to change the Color of the LED Stip.
- `webcam_monitor_service.py`: Monitors the webcam's power state and triggers the `webcam_active_script.py` with the appropriate status.
- `com.user.webcammonitor.plist`: A launch daemon configuration file to run `webcam_monitor_service.py` automatically on system startup.

## Setup

### Prerequisites

- Python 3.x must be installed on your system.
- Administrator privileges to configure and install the launch daemon.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/mac-webcam-automation.git
    cd mac-webcam-automation
    ```

2. **Adjust paths**:
    Replace all occurrences of `/Users/.../` in the scripts and the plist file with the actual paths on your system.

3. **Install the launch daemon**:
    Copy the plist file to the users `LaunchAgents` directory and load it.
    ```bash
    sudo cp com.user.webcammonitor.plist ~/Library/LaunchAgents
    sudo launchctl load ~/Library/LaunchAgents/com.user.webcammonitor.plist
    ```

### Configuration

- **webcam_active_script.py**:
    - This script is where you define the actions to be taken when the webcam is turned on or off. By default, it includes functions to send UDP messages and log the status. Customize these actions as per your requirements.
    
- **webcam_monitor_service.py**:
    - This script monitors the system logs for webcam power state changes and triggers the `webcam_active_script.py` with either `active` or `inactive` status.

### Usage

Once set up, the service will automatically start on system boot and monitor the webcam's status. It will execute the defined actions in `webcam_active_script.py` whenever the webcam is turned on or off.

### Logs

- Standard output and error logs are stored in `/tmp/webcammonitor.out.log` and `/tmp/webcammonitor.err.log` respectively. You can check these logs to debug and ensure the scripts are working as expected.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The `k_to_rgb` function and `GoveeColor` class are adapted from the [wez/govee-py](https://github.com/wez/govee-py) repository.
