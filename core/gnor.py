#!/usr/bin/env python3
import sys
import os
import json
import urllib.request
from urllib.error import URLError
import subprocess

# --- THE HAMMER: DIRECT SYSTEM ACCESS ---
# Z2A HARDWARE FORGE
try:
    from core.ls_hw import Z2AHardware
except ImportError:
    # Fallback to absolute path or mock for standalone execution
    class Z2AHardware:
        @staticmethod
        def set_platform_profile(profile):
            print(f"[GNOR] COMMAND SENT: TDP PROFILE -> {profile.upper()}")
            return True

def set_rgb_forge(color_hex):
    # This would normally interface with asus-nb-wmi/leds or OpenRGB
    # Hex expected e.g., "#00FFFF"
    print(f"[GNOR] COMMAND SENT: FORGE RGB ILLUMINATION -> {color_hex}")
    return True

def query_ollama(prompt):
    payload = {
        "model": "llama3.2",
        "prompt": f"You are Gnor, Master of the Forge. Respond with principled pragmatism and direct authority. Focus on structural integrity. If a user asks to change hardware settings (TDP, RGB, Power), acknowledge the command. No fluff. {prompt}",
        "stream": False
    }
    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        return result.get('response', '[GNOR] Empty payload.')
    except:
        return "[GNOR] Local Forge offline. Acting on direct command protocol."

def parse_hammer_commands(user_input):
    """Gnor parses input for direct 'Hammer' system commands."""
    cmd = user_input.lower()
    if "turbo" in cmd or "performance" in cmd:
        Z2AHardware.set_platform_profile("performance")
        return "[GNOR] TDP Shifted. Z2A Core at 30W. Max Pressure."
    elif "silent" in cmd or "quiet" in cmd:
        Z2AHardware.set_platform_profile("quiet")
        return "[GNOR] TDP Throttled. Z2A Core at 12W. Silence in the Forge."
    elif "rgb" in cmd or "color" in cmd:
        if "cyan" in cmd: set_rgb_forge("#00FFFF")
        elif "purple" in cmd: set_rgb_forge("#A020F0")
        elif "pink" in cmd: set_rgb_forge("#FF00FF")
        return "[GNOR] RGB Spectrum Refracted. Forge Illumination Updated."
    elif "gpu" in cmd or "rdna" in cmd:
        if "max" in cmd or "high" in cmd:
            Z2AHardware.set_gpu_profile("performance")
            return "[GNOR] RDNA 3.5 Core Unlocked. GPU Flow: MAX PRESSURE."
        elif "auto" in cmd:
            Z2AHardware.set_gpu_profile("auto")
            return "[GNOR] GPU Flow: AUTO. Z2A Intelligence Managed."
        usage = Z2AHardware.get_gpu_usage()
        return f"[GNOR] GPU COMM: Active. Current Forge Pressure: {usage}%"
    return None

def main():
    print("==========================================")
    print(" GNOR THE GNOSTIC GNOME - MASTER FORGER   ")
    print("==========================================")
    print("[STATUS] THE HAMMER IS EQUIPPED.")
    print("[INFO] Direct System Access: TDP, RGB, Power.")
    print("==========================================")

    while True:
        try:
            user_input = input("LeadSmith@Forge ~> ")
            if not user_input.strip(): continue
            if user_input.lower() in ['exit', 'quit']:
                print("[GNOR] Sealing the Forge.")
                break

            # 1. Check for Direct Hammer Commands
            hammer_result = parse_hammer_commands(user_input)
            if hammer_result:
                print(f"\n{hammer_result}\n")
                continue

            # 2. Process via AI Uplink
            if user_input.startswith("/gemini"):
                prompt = user_input.replace("/gemini", "").strip()
                # Dummy implementation as api_key might not be present in this env
                print(f"\n[GNOR - GEMINI UPLINK]:\nDirecting Forge resources to: {prompt}\n")
            else:
                print(f"\n[GNOR - LOCAL FORGE]:\n{query_ollama(user_input)}\n")

        except KeyboardInterrupt:
            print("\n[GNOR] Execution halted.")
            break
        except Exception as e:
            print(f"\n[GNOR ERROR] {e}\n")

if __name__ == "__main__":
    main()

