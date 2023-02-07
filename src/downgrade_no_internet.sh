#!/bin/sh
set -e

#OTA_FILE="https://snt.sh/uploads/t9/T9_891_ota_update_all_block_otas.zip"
#OTA_SUM="bfd67784c2a21afcdd8de3111cde14fa"
OTA_SUM="c20f5db25dfa3f5954ff0f9e233d42e4"

# Make sure we are not running yet...
if [ -f /tmp/.downgrade ]; then
	echo "Exiting, we are already running!"
	exit 0
fi

touch /tmp/.downgrade

mkdir -p /cache/rmagt

echo "Validating downgrade image"
md5sum /cache/ota_update_all.zip > /tmp/ota_downgrade.md5

if ! grep -q "${OTA_SUM}" /tmp/ota_downgrade.md5; then
	echo "ERROR, MD5 mismatch! Please retry the downgrade script later."
	exit 1
fi
echo "Downgrade image validated! Continuing with install!"

# Make the OTA system be OK with the abusive install method
mkdir -p /cache/recovery
echo "--update_package=/cache/ota_update_all.zip" > /cache/recovery/command
echo "--debug_no_reboot" >> /cache/recovery/command
mkdir -p /cache/sec
echo 1 > /cache/sec/download_verified
echo 1 > /cache/update_file_verified

# Delete our root tool
rm /data/configs/root.sh

# Make sure device resets on first boot after OTA
/usr/bin/set_reset_param.sh

# Reboot into recovery to install
/usr/bin/go_recovery.sh

# Self nuke
rm -rf /data/configs/pwn/
