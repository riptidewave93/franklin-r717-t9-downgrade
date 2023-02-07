# franklin-r717-t9-downgrade

Python3 tool to generate a modified Configuration Dump for a Franklin Wireless R717 T9 (T-Mobile Branded). Used to either gain root, downgrade, or other, on firmware 2602.

## Usage

    ./pwn_t9.py your_config_dump.bin

## More Info

Please refer to https://snt.sh/2021/09/rooting-the-t-mobile-t9-franklin-wireless-r717-again/

## No internet instructions

If you don't have internet access (a working sim) on the hotspot, here's a way to get the firmware onto the device.

First, flash the root only image.

Wait for reboot. Connect to hotspot (or use usb to keep your home wifi internet going also, very recommended)

Telnet in with `telnet 192.168.0.1`. 
Change the root password to something you can remember with `passwd` command, since the change in the root script doesn't seem to work and we need it to ssh in.
Now you can SSH in, nice since thats better than telnet.
Now, back on your computer set up a tftp server on your computer. On arch that was just a matter of installing the starting the tftp-hpa package.
Download this file https://snt.sh/uploads/t9/T9_1311_ota_update_all_block_otas.zip and put it in /srv/tftp ( you may need to chmod the folder or do this as root)
Also take a copy of the downgrade_no_internet.sh script from this repo

Find out your computers IP that the hotspot gave you (ifconfig works on linux, ipconfig on windows)
From the hotspot shell, run `tftp tftp forrest@192.168.0.210 -l /cache/ota_update_all.zip -r ota_update_all.zip -g`
You may need to `touch /cache/ota_update_all.zip` first because tftp is really old and dumb and needs the file to  prexist I guess.
Do the same thing with my modified script.
Now just execute the script. You'll need to make it executable first with chmod +x downgrade_no_internet.sh

Piece of cake

