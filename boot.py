# This file is executed on every boot (including wake-boot from deepsleep)


# import esp
# esp.osdebug(None)

import gc

import machine
import network
import webrepl

# DO NOT GO BELOW 80Mhz!!!!!
# machine.freq(240000000) # set the CPU frequency to 240 MHz
machine.freq(160000000)  # set the CPU frequency to 160 MHz

alarm = [0, 0, 0, 0]
ap = network.WLAN(network.AP_IF)


def hotspot(ssid, maxc, on):
    ap.config(essid=ssid)
    ap.config(max_clients=maxc)
    ap.active(on)


webrepl.start(password="password")

hotspot("ESP-AP", 2, True)

gc.collect()
