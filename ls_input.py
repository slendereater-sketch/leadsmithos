import os
import platform
import ctypes

# Standardize Constants for the Forge
XINPUT_GAMEPAD_A = 0x1000 if os.name == 'nt' else 304
XINPUT_GAMEPAD_B = 0x2000 if os.name == 'nt' else 305
XINPUT_GAMEPAD_START = 0x0010 if os.name == 'nt' else 315
XINPUT_GAMEPAD_DPAD_UP = 0x0001 if os.name == 'nt' else 16
XINPUT_GAMEPAD_DPAD_DOWN = 0x0002 if os.name == 'nt' else 16

_state = None

class LinuxGamepad:
    def __init__(self):
        import evdev
        from evdev import ecodes
        import threading
        self.buttons = 0
        self.device = None
        
        # Search for handheld controllers
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if any(name in device.name for name in ["Microsoft X-Box 360 pad", "Handheld", "Controller"]):
                self.device = device
                break
        
        if self.device:
            threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        from evdev import ecodes
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 1: self.buttons |= event.code
                elif event.value == 0: self.buttons &= ~event.code

class WindowsGamepad:
    def __init__(self):
        from ctypes.wintypes import WORD, BYTE, DWORD
        class XINPUT_GAMEPAD(ctypes.Structure):
            _fields_ = [('wButtons', WORD), ('bLeftTrigger', BYTE), ('bRightTrigger', BYTE),
                        ('sThumbLX', ctypes.c_short), ('sThumbLY', ctypes.c_short),
                        ('sThumbRX', ctypes.c_short), ('sThumbRY', ctypes.c_short)]
        class XINPUT_STATE(ctypes.Structure):
            _fields_ = [('dwPacketNumber', DWORD), ('Gamepad', XINPUT_GAMEPAD)]
        self.XINPUT_STATE = XINPUT_STATE
        try:
            self.xinput = ctypes.windll.xinput1_4
        except:
            self.xinput = ctypes.windll.xinput1_3

    def get_buttons(self):
        state = self.XINPUT_STATE()
        if self.xinput.XInputGetState(0, ctypes.byref(state)) == 0:
            return state.Gamepad.wButtons
        return 0

def get_gamepad_buttons():
    global _state
    if _state is None:
        if os.name == 'nt':
            _state = WindowsGamepad()
        else:
            try:
                _state = LinuxGamepad()
            except ImportError:
                return 0
    
    if os.name == 'nt':
        return _state.get_buttons()
    return _state.buttons
