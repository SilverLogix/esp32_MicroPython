import gc
import machine
import network
import webrepl
machine.freq(80000000) 
ap=network.WLAN(network.AP_IF)
def hotspot(ssid,maxc,on):
 ap.config(essid=ssid)
 ap.config(max_clients=maxc)
 ap.active(on)
hotspot("ESP-AP",2,True)
network.WLAN(0).active(False)
network.WLAN(1).active(False)
gc.collect()
