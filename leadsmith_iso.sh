#!/bin/bash
# ==========================================================
# LEADSMITH Z2A: LIVE ISO ENTRYPOINT (NO KEYBOARD)
# ==========================================================
# This script is the first thing that runs on the ISO.
# It launches the Touch-Friendly Python Igniter.
# ==========================================================

echo "[âš’] INITIATING LEADSMITH Z2A FORGE..."

# 1. MOUNT WINDOWS PARTITION (REACH-BACK)
# On ROG Ally, NVMe0n1p3 is usually the Windows C: drive.
# We will search for LeadSmithOS_Final on all NTFS partitions.
echo "[âš™] SCANNING FOR STAGED FILES ON WINDOWS (REACH-BACK)..."
mkdir -p /mnt/win_stage
for part in $(lsblk -p -n -l -o NAME,FSTYPE | grep ntfs | awk '{print $1}'); do
    mount -o ro "$part" /mnt/win_stage 2>/dev/null
    if [ -d "/mnt/win_stage/LeadSmithOS_Final" ]; then
        if [ -f "/mnt/win_stage/LeadSmithOS_Final/FORGE_LIVE_MEDIA.flag" ]; then
            echo "[âœ“] FORGE LIVE MEDIA FOUND ON $part"
        else
            echo "[âœ“] STAGED FILES FOUND ON $part"
        fi
        # Copy files to a writable location in the ISO environment
        mkdir -p /tmp/LeadSmithOS
        cp -r /mnt/win_stage/LeadSmithOS_Final/* /tmp/LeadSmithOS/
        umount /mnt/win_stage
        BASE_DIR="/tmp/LeadSmithOS"
        break
    fi
    umount /mnt/win_stage 2>/dev/null
done

if [ -f "$BASE_DIR/leadsmith_igniter.py" ]; then
    echo "[âš’] IGNITING FORGE FROM STAGED FILES..."
    python3 "$BASE_DIR/leadsmith_igniter.py"
else
    echo "[!] NO STAGED FILES FOUND. FALLBACK TO ISO ROOT."
    # Fallback to standard path if staged files not found
    BASE_DIR="/run/archiso/bootmnt/LeadSmithOS_Final"
    if [ ! -d "$BASE_DIR" ]; then BASE_DIR="/run/archiso/bootmnt"; fi
    python3 "$BASE_DIR/leadsmith_igniter.py"
fi
