import subprocess
import re
import logging
from datetime import datetime

# logging
logging.basicConfig(filename='/tmp/webcammonitor.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def run_script(status):
    script_path = "/Users/.../webcam_active_script.py"
    try:
        subprocess.run(["python3", script_path, status], check=True)
        logging.info(f"Script run with status: {status}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing the script: {e}")

def parse_log_line(line):
    match = re.search(r'"VDCAssistant_Power_State"\s*=\s*(\w+)', line)
    if match:
        return match.group(1)
    return None

def monitor_webcam():
    cmd = [
        "log", "stream",
        "--predicate", 'subsystem contains "com.apple.UVCExtension" and composedMessage contains "Post PowerLog"'
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    for line in process.stdout:
        power_state = parse_log_line(line)
        if power_state:
            if power_state == "On":
                logging.info("Webcam activated")
                run_script("active")
            elif power_state == "Off":
                logging.info("Webcam deactivated")
                run_script("inactive")

if __name__ == "__main__":
    logging.info("Mac-Webcam-Automation started")
    monitor_webcam()