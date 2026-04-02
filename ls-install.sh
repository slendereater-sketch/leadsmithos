#!/bin/bash
# ==========================================================
# LEADSMITH OS: Z2A MASTER INSTALLER (ROG ALLY Z2 EXTREME)
# ==========================================================
# This script automates Z2A-specific drivers, 120Hz VRR, 
# and Forge Dashboard integration for Arch Linux.
# ==========================================================

echo "=========================================="
echo "   IGNITING THE LEADSMITH Z2A FORGE       "
echo "=========================================="

# 0. BASE DEPENDENCIES & PRIVILEGES
if [ "$EUID" -ne 0 ]; then
    echo "[!] ERROR: THIS FORGE REQUIRES ROOT ACCESS. RUN WITH SUDO."
    exit 1
fi

echo "[âš™] REINFORCING BASE SYSTEM (GIT, PYTHON, DEVEL)..."
pacman -Sy --needed --noconfirm git base-devel python python-pip python-setuptools
echo "[âœ“] BASE REINFORCEMENTS COMPLETE."

# 1. CORE HARDWARE DRIVERS (ROG ALLY Z2A)
echo "[âš™] OPTIMIZING KERNEL FOR Z2A ARCHITECTURE..."
# Add the asus-linux repository for specialized handheld kernels
if ! grep -q "g14" /etc/pacman.conf; then
    echo -e "\n[g14]\nServer = https://arch.asus-linux.org" >> /etc/pacman.conf
    pacman-key --recv-keys 8F654886F17D497FEFE3DB448B15A6B0E9A3D5D9
    pacman-key --lsign-key 8F654886F17D497FEFE3DB448B15A6B0E9A3D5D9
fi

pacman -Sy --noconfirm linux-g14 linux-g14-headers asusctl rog-control-center
echo "[âœ“] Z2A MASTER KERNEL & ASUSCTL INSTALLED."

# 2. TOUCHSCREEN & GAMEPAD MAPPING
echo "[âš™] SYNCHRONIZING Z2A TOUCH & XINPUT..."
pacman -S --noconfirm xf86-input-libinput evtest python-evdev python-pyusb
# Enable the gamepad as a mouse/desktop controller fallback
systemctl enable --now supergfxctl

# 3. 120Hz VRR & GRAPHICS (RDNA 3.5)
echo "[âš›] CALIBRATING 120Hz VRR PANEL..."
pacman -S --noconfirm mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon libva-mesa-driver
# Create the 120Hz Xorg/Wayland override
mkdir -p /etc/X11/xorg.conf.d/
cat <<EOF > /etc/X11/xorg.conf.d/20-amdgpu.conf
Section "Device"
     Identifier "AMD"
     Driver "amdgpu"
     Option "VariableRefresh" "true"
     Option "TearFree" "true"
EndSection
EOF

# 4. LEADSMITH OS DASHBOARD DEPLOYMENT
echo "[âš’] FORGING LEADSMITH DASHBOARD (120 FPS)..."
mkdir -p ~/LeadSmithOS/{bin,sdk,core,apps,assets,config}
cp -r ./* ~/LeadSmithOS/
chmod +x ~/LeadSmithOS/ls-boot.sh
chmod +x ~/LeadSmithOS/core/gnor.py

# Create Autostart Entry for Dashboard
mkdir -p ~/.config/autostart
cat <<EOF > ~/.config/autostart/leadsmith.desktop
[Desktop Entry]
Type=Application
Exec=$HOME/LeadSmithOS/ls-boot.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=LeadSmith OS Dashboard
Comment=Ignite the Forge on Startup
EOF

# Configure GDM Auto-login (Requires Root)
if [ "$EUID" -eq 0 ]; then
    echo "[âš™] CONFIGURING GDM AUTO-LOGIN..."
    mkdir -p /etc/gdm/
    cat <<EOF > /etc/gdm/custom.conf
[daemon]
AutomaticLoginEnable=True
AutomaticLogin=leadsmith
EOF
fi

# Add to Autostart (assuming a WM like Sway or Hyprland)
if [ -f ~/.bashrc ]; then
    echo "alias gnor='python3 ~/LeadSmithOS/core/gnor.py'" >> ~/.bashrc
    echo "alias forge='bash ~/LeadSmithOS/ls-boot.sh'" >> ~/.bashrc
fi

# 5. GNOR AI UPLINK SETUP
echo "[âš™] LINKING GNOR AI CORE (THE HAMMER)..."
pip install textual rich psutil pygame --quiet

echo "=========================================="
echo "   Z2A FORGE READY. REBOOT TO IGNITE.     "
echo "=========================================="
