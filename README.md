# LeadSmith OS: Z2A Forge Edition 🛠️🔥

**LeadSmith OS** is a specialized, zero-touch Arch Linux environment custom-built for the **ROG Ally Z2 Extreme (Z2A)**. It is designed to maximize handheld performance with 120Hz VRR support, RDNA 3.5 optimizations, and a custom dashboard for seamless gaming and system management.

---

## 🚀 Key Features

*   **Z2A Optimized Kernel:** Pre-configured with the `linux-g14` kernel for native ROG Ally hardware support.
*   **120Hz VRR Display:** Automated calibration for variable refresh rate and tear-free gaming on the internal panel.
*   **LeadSmith Forge Dashboard:** A high-performance (120 FPS) dashboard for launching apps and monitoring system health.
*   **GNOR AI Core:** Integrated AI uplink ("The Hammer") for intelligent system management and automation.
*   **Zero-Touch Interaction:** Optimized for touchscreen and gamepad navigation with GDM auto-login and autostart capabilities.
*   **Handheld Tools:** Built-in support for `asusctl`, `rog-control-center`, and `supergfxctl`.

---

## 🛠️ Installation

LeadSmith OS is designed to be installed on top of a base **Arch Linux** installation.

### 1. Prerequisites
*   A ROG Ally Z2 Extreme device.
*   A fresh installation of Arch Linux (with network access).
*   Git installed: `sudo pacman -S git`

### 2. Ignite the Forge
Run the following commands in your terminal to deploy the LeadSmith environment:

```bash
# 1. Clone the Forge
git clone https://github.com/slendereater-sketch/LeadSmithOS.git
cd LeadSmithOS

# 2. Make the installer executable
chmod +x ls-install.sh

# 3. Run the Master Installer (requires sudo)
sudo ./ls-install.sh
```

### 3. Finalize
Once the script completes, **reboot your device**. It will automatically boot into the LeadSmith Dashboard.

---

## 🧩 Project Structure

*   `/core`: The heart of the OS, including the GNOR AI core and hardware mapping.
*   `/apps`: Pre-bundled applications and visualizers (e.g., AgilityFlow).
*   `/sdk`: Development tools for extending LeadSmith OS features.
*   `ls-install.sh`: The master deployment script.

---

## ⚖️ License
This project is part of the LeadSmith OS Core. All rights reserved. Ignite the Forge.
