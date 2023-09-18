#!/usr/bin/env bash
IP=192.168.1.168
reload_ip(){
	sudo ifconfig wlan0 down 0; sudo ifconfig wlan0 up; sudo dhclient wlan0
}
while :; do
	if ! ifconfig wlan0|grep -q "inet $IP "; then
		echo "Reloading IP"
	else
		echo "IP $IP OK"
	fi
	sleep 1
done
