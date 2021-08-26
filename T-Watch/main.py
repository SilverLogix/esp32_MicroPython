from c_network import *
from html import *
from gfx import *

# from machine import lightsleep
import debug
import socket
import machine
import gc
import random
import utime
import _thread as thread
import gfx

# --------- Variables --------- #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# -------- Init main code ---------- #
# gfx.micrologo()

# STA('SSID', 'PASS')
# AP("ESP32-AP", 2, True)

# noinspection PyArgumentList
machine.freq(80000000)  # set the CPU frequency to 80 MHz

gc.collect()


# ---------- Create Objects --------- #

def scr_test():
    try:
        for rotation in range(4):
            tft.rotation(rotation)
            tft.fill(0)
            col_max = tft.width() - font.WIDTH * 6
            row_max = tft.height() - font.HEIGHT

            for _ in range(128):
                utime.sleep_ms(100)
                tft.text(font, "Hello!",
                         random.randint(0, col_max),
                         random.randint(0, row_max),
                         st.color565(
                             random.getrandbits(8),
                             random.getrandbits(8),
                             random.getrandbits(8)),
                         st.color565(
                             random.getrandbits(8),
                             random.getrandbits(8),
                             random.getrandbits(8))
                         )
    except KeyboardInterrupt:
        thread.exit()

tft.fill(st.BLACK)
alarm_0 = 0
def draw():
    while True:
        global alarm_0
        # gfx.triangle(43, 30, 40, 90, 80, 120, st.color565(200,200,200))

        ddd = debug.showVoltage()
        rrr = debug.raw_temp()
        fff = debug.m_freq()

        A = alarm_0 + 1


        gfx.text_long("Sensor", ddd, rrr, "", fff, "", "", A, st.WHITE, st.BLACK)
        utime.sleep_ms(1000)




# --------- Main Code ---------- #

# thread.start_new_thread(scr_test, ())
thread.start_new_thread(draw, ())



while True:

    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
        print('LED ON')
        led.value(1)
    if led_off == 6:
        print('LED OFF')
        led.value(0)
    response = WEB_PAGE

    # noinspection PyTypeChecker
    conn.send('HTTP/1.1 200 OK\n')
    # noinspection PyTypeChecker
    conn.send('Content-Type: text/html\n')
    # noinspection PyTypeChecker
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
