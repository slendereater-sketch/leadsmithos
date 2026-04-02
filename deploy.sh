#!/bin/bash
echo "DEPLOYING LEADSMITH OS..."
mkdir -p ~/LeadSmithOS/{bin,sdk,core,apps,assets,config}
cp ls_dash.py ~/LeadSmithOS/
cp ls-boot.sh ~/LeadSmithOS/
cp xinput_bridge.py ~/LeadSmithOS/
cp sdk/ls-sdk.py ~/LeadSmithOS/sdk/
cp core/* ~/LeadSmithOS/core/
chmod +x ~/LeadSmithOS/ls-boot.sh
if ! grep -q "ls-boot.sh" ~/.bashrc; then
    echo "bash ~/LeadSmithOS/ls-boot.sh" >> ~/.bashrc
fi
echo "DONE. Restart terminal."
