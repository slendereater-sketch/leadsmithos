import ctypes
from ctypes.wintypes import WORD, BYTE

# XInput Constants
XINPUT_GAMEPAD_DPAD_UP = 0x0001
XINPUT_GAMEPAD_DPAD_DOWN = 0x0002
XINPUT_GAMEPAD_START = 0x0010
XINPUT_GAMEPAD_BACK = 0x0020
XINPUT_GAMEPAD_A = 0x1000
XINPUT_GAMEPAD_B = 0x2000

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('wButtons', WORD),
        ('bLeftTrigger', BYTE),
        ('bRightTrigger', BYTE),
        ('sThumbLX', ctypes.c_short),
        ('sThumbLY', ctypes.c_short),
        ('sThumbRX', ctypes.c_short),
        ('sThumbRY', ctypes.c_short),
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ('dwPacketNumber', ctypes.c_ulong),
        ('Gamepad', XINPUT_GAMEPAD),
    ]

# Try to load XInput DLL (usually 1_4 on Windows 10/11)
try:
    xinput = ctypes.windll.xinput1_4
except OSError:
    try:
        xinput = ctypes.windll.xinput1_3
    except OSError:
        xinput = None

def get_gamepad_buttons(controller_id=0):
    if not xinput:
        return None
    state = XINPUT_STATE()
    res = xinput.XInputGetState(controller_id, ctypes.byref(state))
    if res == 0:
        return state.Gamepad.wButtons
    return None
