#!/bin/sh

# Try to prevent OTAs
if ! grep -q "fota.pintracview.com" /etc/hosts; then
	echo "127.0.1.1 fota.pintracview.com t9datafiles.s3.us-east-2.amazonaws.com t9-stg-api.pintracview.com" >> /etc/hosts
fi
if ! grep -q "fota.pintracview.com" /data/hosts; then
	echo "127.0.1.1 fota.pintracview.com t9datafiles.s3.us-east-2.amazonaws.com t9-stg-api.pintracview.com" >> /data/hosts
fi

# Set root pw back to old pass
echo -e "frk9x07\nfrk9x07" | passwd > /dev/null

# Setup SSH if it's not setup
if [ ! -f /etc/init.d/dropbear ]; then
	mv /data/configs/pwn/dropbear.init /etc/init.d/dropbear
	chmod +x /etc/init.d/dropbear
	ln -s /etc/init.d/dropbear /etc/rc0.d/K10dropbear
	ln -s /etc/init.d/dropbear /etc/rc1.d/K10dropbear
	ln -s /etc/init.d/dropbear /etc/rc2.d/S10dropbear
	ln -s /etc/init.d/dropbear /etc/rc3.d/S10dropbear
	ln -s /etc/init.d/dropbear /etc/rc4.d/S10dropbear
	ln -s /etc/init.d/dropbear /etc/rc5.d/S10dropbear
	ln -s /etc/init.d/dropbear /etc/rc6.d/K10dropbear

	mv /data/configs/pwn/dropbearmulti /usr/sbin/dropbearmulti
	chmod +x /usr/sbin/dropbearmulti
	ln -s /usr/sbin/dropbearmulti /usr/sbin/dropbear
	ln -s /usr/sbin/dropbearmulti /usr/sbin/dropbearconvert
	ln -s /usr/sbin/dropbearmulti /usr/sbin/dropbearkey
	ln -s /usr/sbin/dropbearmulti /usr/bin/dbclient
	ln -s /usr/sbin/dropbearmulti /usr/bin/scp
	ln -s /usr/sbin/dropbearmulti /usr/bin/ssh

	/etc/init.d/dropbear start
fi

# Spawn root telnet shell with no pass
/sbin/telnetd -l /bin/bash

# Kick off downgrade in the background if we have it
if [ -f /data/configs/pwn/downgrade.sh ]; then
	# Only run if it's not already running...
	if [ ! -f /tmp/.downgrade ]; then
		start-stop-daemon -S -b -n downgrade.sh -p /tmp/downgrade.pid -x /data/configs/pwn/downgrade.sh
	fi
fi
