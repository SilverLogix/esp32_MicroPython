
# ---------- Connect to a router ---------- #
def STA(ssid: str, passw: str):
    import network

    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, passw)

    while not sta.isconnected():
        pass

    print('Connection successful')
    print(sta.ifconfig())
    return sta


# --------- Create a Hotspot ---------- #
def AP(ssid: str, maxc: int, on: bool):
    import network

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid)
    ap.config(max_clients=maxc)
    ap.active(on)

def wkill():
    import network

    network.WLAN(0).active(False)
    network.WLAN(1).active(False)
