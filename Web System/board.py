
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


# ---------- Connect to a router with a static IP ---------- #
def SSSTA(ssid: str, passw: str, static: str, routerip: str):
    import network

    sssta = network.WLAN(network.STA_IF)
    sssta.ifconfig((static, "255.255.255.0", routerip, routerip))
    sssta.active(True)
    sssta.connect(ssid, passw)

    while not sssta.isconnected():
        pass

    print('Connection successful')
    print(sssta.ifconfig())
    return sssta


# --------- Create a Hotspot ---------- #
def AP(ssid: str, maxc: int, pswd: int):
    import network

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid)
    ap.config(max_clients=maxc)
    ap.config(password=pswd)
    ap.active(True)


def Wkill(cmd: bool):
    import network

    network.WLAN(0).active(cmd)
    network.WLAN(1).active(cmd)
