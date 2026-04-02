import os
import subprocess

class Z2ASettings:
    BACKLIGHT_PATH = "/sys/class/backlight/amdgpu_bl0/"

    @staticmethod
    def get_brightness():
        try:
            with open(Z2ASettings.BACKLIGHT_PATH + "brightness", "r") as f:
                current = int(f.read().strip())
            with open(Z2ASettings.BACKLIGHT_PATH + "max_brightness", "r") as f:
                maximum = int(f.read().strip())
            return int((current / maximum) * 100)
        except: return 0

    @staticmethod
    def set_brightness(percent):
        try:
            with open(Z2ASettings.BACKLIGHT_PATH + "max_brightness", "r") as f:
                maximum = int(f.read().strip())
            new_val = int((percent / 100) * maximum)
            os.system(f"echo {new_val} | sudo tee {Z2ASettings.BACKLIGHT_PATH}brightness")
            return True
        except: return False

    @staticmethod
    def get_wifi_status():
        try:
            res = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], encoding='utf-8')
            for line in res.split('
'):
                if line.startswith("yes:"): return line.split(':')[1]
            return "DISCONNECTED"
        except: return "OFFLINE"

