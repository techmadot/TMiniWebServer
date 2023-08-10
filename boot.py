# boot.py -- run on boot-up
import network
import os
import sys

# Replace the following with your WIFI Credentials
SSID = "YOUR_SSID"
SSID_PASSWORD = "YOUR_SSID_PASSWORD"
try:
    with open('laninfo.txt', 'rt') as f:
        info = f.readlines()

        SSID = info[0]
        SSID_PASSWORD = info[1]
except:
    print("Failed LAN Configuration.")
    sys.exit()


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()
