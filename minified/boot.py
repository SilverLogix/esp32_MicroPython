import gc
import machine
import network
m=True
I=False
z=gc.collect
K=machine.freq
E=network.AP_IF
L=network.WLAN
K(80000000)
ap=L(E)
def x(ssid,maxc,on):
 ap.config(essid=ssid)
 ap.config(max_clients=maxc)
 ap.active(on)
x("ESP-AP",2,m)
L(0).active(I)
L(1).active(I)
z()
