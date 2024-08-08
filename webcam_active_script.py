import sys
import socket
import json
import math
from dataclasses import dataclass
from typing import Dict, Tuple

#k_to_rgb and GoveeColor taken from https://github.com/wez/govee-py

def clamp(value: int, lower: int, upper: int) -> int:
    """Clamp a value to a specified range"""
    return max(min(value, upper), lower)


def k_to_rgb(kelvin: int) -> Tuple[int, int, int]:
    """Compute an rgb value corresponding to a color temperature in kelvin."""
    kelvin = clamp(kelvin, 1000, 40000)

    temperature = kelvin / 100.0

    if temperature <= 66:
        red = 255.0
    else:
        red = 329.698727446 * math.pow(temperature - 60, -0.1332047592)

    if temperature <= 66:
        green = 99.4708025861 * math.log(temperature) - 161.1195681661
    else:
        green = 288.1221695283 * math.pow(temperature - 60, -0.0755148492)

    if temperature >= 66:
        blue = 255.0
    elif temperature <= 19:
        blue = 0.0
    else:
        blue = 138.5177312231 * math.log(temperature - 10) - 305.0447927307

    return clamp(int(red), 0, 255), clamp(int(green), 0, 255), clamp(int(blue), 0, 255)


@dataclass
class GoveeColor:
    """Represents an sRGB color"""

    red: int = 0
    green: int = 0
    blue: int = 0

    def as_tuple(self) -> Tuple[int, int, int]:
        """Returns (r, g, b)"""
        return (self.red, self.green, self.blue)

    def as_json_object(self) -> Dict[str, int]:
        """Returns {"r":r, "g":b, "b":b}"""
        return {"r": self.red, "g": self.green, "b": self.blue}

    @staticmethod
    def from_kelvin(kelvin: int):
        """Computes the rgb equivalent to a color temperature specified in kelvin"""

        red, green, blue = k_to_rgb(kelvin)
        print(f"{kelvin} -> {red}, {green}, {blue}")

        return GoveeColor(
            red=red,
            green=green,
            blue=blue,
        )


def send_udp_json_message(ip, port, message):
    # Erstellen eines UDP-Sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # JSON-Nachricht erstellen
        json_message = json.dumps(message).encode('utf-8')
        print(json_message)
        # Nachricht an die angegebene IP und Port senden
        sock.sendto(json_message, (ip, port))
        print(f"Nachricht gesendet an {ip}:{port}")

    except Exception as e:
        print(f"Fehler beim Senden der Nachricht: {e}")

    finally:
        # Socket schließen
        sock.close()


def set_led_color(status_code):
    # Define IP and port for the LED strip
    ip = "192.168.50.88"
    port = 4003

    # Determine color based on status code
    if status_code == "active":
        color = GoveeColor(red=240, green=255, blue=240)  # White
    elif status_code == "inactive":
        color = GoveeColor(red=255, green=255, blue=0)  # Yellow
    else:
        print(f"Unbekannter Statuscode: {status_code}")
        return

    # Create the message to send
    colormessage = {
        "msg": {
            "cmd": "colorwc",
            "data": {
                "color": color.as_json_object(),
            },
        }
    }

    # Send the color setting message to the LED strip
    send_udp_json_message(ip, port, colormessage)    


def main():
    # Get the status code from the command line arguments
    status_code = sys.argv[1]

    # Print the status message
    print(f"Webcam ist jetzt aktiv. Statuscode: {status_code}")

    # Set the LED color based on the status code
    set_led_color(status_code)


if __name__ == "__main__":
    main()
