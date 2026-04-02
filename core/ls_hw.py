import os

class Z2AHardware:
    ASUS_PATH = "/sys/devices/platform/asus-nb-wmi/"
    HWMON_PATH = "/sys/class/hwmon/"

    @staticmethod
    def get_platform_profile():
        try:
            with open(Z2AHardware.ASUS_PATH + "platform_profile", "r") as f:
                return f.read().strip().upper()
        except: return "UNKNOWN"

    @staticmethod
    def get_fan_rpm():
        try:
            for hwmon in os.listdir(Z2AHardware.HWMON_PATH):
                name_path = os.path.join(Z2AHardware.HWMON_PATH, hwmon, "name")
                with open(name_path, "r") as f:
                    if "asus" in f.read():
                        rpm_path = os.path.join(Z2AHardware.HWMON_PATH, hwmon, "fan1_input")
                        with open(rpm_path, "r") as rpm_f: return rpm_f.read().strip()
        except: return "0"
        return "0"

    @staticmethod
    def get_battery_wattage():
        try:
            with open("/sys/class/power_supply/BAT0/power_now", "r") as f:
                uw = int(f.read().strip())
                return f"{uw / 1_000_000:.2f}W"
        except: return "0.00W"


    @staticmethod
    def set_platform_profile(profile):
        # profile: 'quiet', 'balanced', 'performance'
        try:
            profile_path = Z2AHardware.ASUS_PATH + "platform_profile"
            if os.path.exists(profile_path):
                with open(profile_path, "w") as f:
                    f.write(profile)
                return True
        except: return False
        return False

    @staticmethod
    def get_gpu_usage():
        # RDNA 3.5 / amdgpu usage percentage
        try:
            # Common path for primary GPU in Arch Linux handhelds
            gpu_path = "/sys/class/drm/card0/device/gpu_busy_percent"
            if os.path.exists(gpu_path):
                with open(gpu_path, "r") as f:
                    return int(f.read().strip())
        except: return 0
        return 0

    @staticmethod
    def set_gpu_profile(level):
        # level: 'auto', 'low', 'high', 'manual'
        # Communicates with PowerPlay via sysfs
        try:
            pp_path = "/sys/class/drm/card0/device/power_dpm_force_performance_level"
            if os.path.exists(pp_path):
                with open(pp_path, "w") as f:
                    f.write(level)
                return True
        except: return False
        return False
