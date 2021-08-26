
# ---------- Connect to a router ---------- #
def STA(ssid, passw):
    import network
    st = network.WLAN(network.STA_IF)
    st.active(True)
    st.connect(ssid, passw)

    while not st.isconnected():
        pass

    print('Connection successful')
    print(st.ifconfig())


# --------- Create a Hotspot ---------- #
def AP(ssid, maxc, on):
    import network

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid)
    ap.config(max_clients=maxc)
    ap.active(on)
