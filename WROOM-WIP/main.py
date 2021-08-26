# ---------- #

from os import statvfs
import machine
import utime
from machine import PWM, Pin
import dht
import esp32
import gc
import uasyncio

# Custom imports
import gfx
import board as bd
import debug

gc.enable()


# =============== Init Variables =============== #
btn = Pin(0, Pin.IN)

stop_sync    = bool(False)
ScreenSelect = int(0)
temp, humi   = float(0.0), int(0)
alarm_0      = int(0)
wifi_on      = bool(False)


# ============================================== #


if wifi_on:
    gfx.gwifi()
    wifi = bd.STA("SSID", "PASS")
    utime.sleep_ms(200)


try:
    if wifi.active():
        machine.freq(160000000)
except:
    print("No WiFi")
    machine.freq(40000000)

debug.pprint()

gc.collect()


def deep_sleep(ms):
    # put the device to sleep for 10 seconds
    machine.deepsleep(ms)


def l_sleep(ms):
    machine.sleep(ms)


def sound(freq=1567.98):
    pwm0 = PWM(Pin(25))
    pwm0.freq(freq)
    pwm0.duty(512)


async def get_dht11(pin, calibration):  # get sensor info
    d = dht.DHT11(machine.Pin(pin, machine.Pin.PULL_UP))
    global temp, humi
    while True:
        await uasyncio.sleep(2)
        d.measure()
        temp = (d.temperature() - calibration)
        humi = d.humidity()
        await uasyncio.sleep(2)


# ========== Screens ========= #

# screen 0 ---------
def scralarm():
    gfx.text_long("Screen", "", "Alarm_1 = ", str(alarm_0), "", "", "", "")
    gfx.text("Blue", 0, 98, gfx.BLUE, gfx.BLACK)


# screen 1 ---------
def display_dht11():
    global temp, humi
    gfx.text("Sensor", 0, 0, gfx.YELLOW, gfx.BLACK)
    # Convert celsius to fahrenheit
    ctf = (temp * 9 / 5) + 32
    gfx.text_long("", "", "Temp = {0:0.1f}F".format(ctf), "Humidity = {0:0.0f}%".format(humi), "", "", "", "")


# screen 2 ---------
def info():  # Get and display Info # SCREEN 2

    ip = "Wifi Off"

    mfreq = str(machine.freq())
    raw = str(esp32.raw_temperature())

    gfx.text_long("Info", "", ip, "CPU temp = " + raw + "F", "", mfreq, "", "")
    gc.collect()


# screen 3 ---------
def dfree():  # Display remaining free space # SCREEN 3
    # am = str(alarmc1)

    bits = statvfs('/flash')
    # print(str(bits))
    blksize = bits[0]  # 4096
    blkfree = bits[3]  # 12
    freesize = blksize * blkfree  # 49152
    mbcalc = 1024 * 1024  # 1048576
    mbfree = freesize / mbcalc  # 0.046875
    freestr = str(mbfree)

    gfx.text_long("Space(MB)", "", "Curr: " + freestr, "", "Old:  " + "1.949219", "", "", "")
    gc.collect()


# screen 4 ---------
def draw_shapes():  # Test draw screen
    gfx.text_long("Screen 4", "", "", "", "", "", "", "")

    # gfx.text("Draw", 0, 0)  # Set some text
    # oled.fill_rect(15, 15, 44, 44, 1)
    # oled.rect(10, 10, 40, 40, 1)
    # oled.line(0,0,64,64,1)
    # oled.triangle(10, 10, 55, 20, 5, 40, 1)
    # oled.circle(64, 32, 10, 1)
    # oled.round_rect(20, 20, 30, 30, 3, 1)


# screen 5 ---------
def showlogo():
    gfx.text_long("Colors", "", "", "", "", "", "", "")

    gfx.text("    ",    0, 18,  gfx.BLACK,   gfx.BLACK)
    gfx.text("Red",     0, 34,  gfx.RED,     gfx.BLACK)
    gfx.text("Blue",    0, 50,  gfx.BLUE,    gfx.BLACK)
    gfx.text("White",   0, 66,  gfx.WHITE,   gfx.BLACK)
    gfx.text("Green",   0, 82,  gfx.GREEN,   gfx.BLACK)
    gfx.text("Magenta", 0, 98,  gfx.MAGENTA, gfx.BLACK)
    gfx.text("Cyan",    0, 114, gfx.CYAN,    gfx.BLACK)


# =========================== #


# ------------------------------------ #

def my_func(self):  # push button tests
    global ScreenSelect

    # utime.sleep_ms(5)
    ScreenSelect += 1
    print(ScreenSelect)
    gfx.wipe(gfx.BLACK)


# ----------- #


async def sleep_1sec():
    global alarm_0
    while True:
        alarm_0 += 1
        await uasyncio.sleep_ms(1000)


async def show_screens():
    global ScreenSelect

    while True:
        btn.irq(my_func, Pin.IRQ_RISING)

        # -------------------

        if ScreenSelect > 5:
            gfx.wipe(gfx.BLACK)
            gc.collect()
            ScreenSelect = 0

        if ScreenSelect == 0:
            scralarm()

        if ScreenSelect == 1:
            display_dht11()

        if ScreenSelect == 2:
            info()

        if ScreenSelect == 3:
            dfree()

        if ScreenSelect == 4:
            draw_shapes()

        if ScreenSelect == 5:
            showlogo()

        await uasyncio.sleep_ms(50)

# ------------------------------------- #


#             Nothing here              #


# ------------- Main Loop ------------- #

gfx.fill(gfx.BLACK)

loop = uasyncio.get_event_loop()

loop.create_task(show_screens())
loop.create_task(get_dht11(15, 1))
loop.create_task(sleep_1sec())

loop.run_forever()

# ------------------------------------ #
