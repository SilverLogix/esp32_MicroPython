from os import statvfs
import machine
from machine import Pin, I2C, ADC, PWM
import dht
import time
import ssd1306
import esp32
# Custom imports
from boot import gc, ap
from logo import showlogo

# Init Screen --------------------------------------------------#
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))  # Set Pins
oled_width = int(128)  # Width of OLED
oled_height = int(64)  # Length of OLED
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(1)
oled.show()
time.sleep_ms(30)
oled.fill(0)
oled.text("Screen", 38, 0)  # Set some text
oled.show()  # Show the text
# ------------------------------------------------------------- #

alarm2 = 0


def alarm_2(maxcount):
    global alarm2

    if alarm2 != maxcount:
        alarm2 = alarm2 - 1

    if alarm2 <= 0:
        alarm2 = maxcount
    return alarm2


# Init basic variables
f = int(0)
ScreenSelect = int(0)

a1max = 2
alarm_1 = int(a1max)

# Init advanced variables
d = dht.DHT11(machine.Pin(4, machine.Pin.PULL_UP))

btn = Pin(0, Pin.IN)
led = Pin(2, Pin.OUT)
adc = ADC(Pin(35))
stop = bool(False)


def oled_pix():
    oled.pixel(70, 4, 1)
    oled.pixel(75, 4, 1)
    oled.pixel(80, 4, 1)
    oled.pixel(85, 4, 1)

    oled.pixel(90, 3, 1)
    oled.pixel(89, 4, 1)
    oled.pixel(90, 5, 1)
    oled.pixel(91, 4, 1)


# (Title, Line#1, Line#2, Line#3, Line#4, Line#5, Screen#)
def oled_text(otitle, oline1, oline2, oline3, oline4, oline5, onum):
    oled.fill(0)

    oled.text(otitle, 0, 0)
    oled.text(onum, 90, 0)

    oled.text(oline1, 0, 16)
    oled.text(oline2, 0, 26)
    oled.text(oline3, 0, 36)
    oled.text(oline4, 0, 46)
    oled.text(oline5, 0, 56)

    oled.show()


def deep_sleep():
    # pylint: disable=unexpected-arg
    # put the device to sleep for 10 seconds
    oled.contrast(0)
    machine.deepsleep(10000)


def sound():
    pwm0 = PWM(Pin(15))
    pwm0.freq(1567.98)
    pwm0.duty(512)          # set duty cycle


# Screens ---------------------------------------------------------------------------------------- #
def temp():  # Get and display temperature # SCREEN 1
    try:
        # Get sensor readings
        d.measure()
        t = d.temperature()
        h = d.humidity()

        # Convert celsius to fahrenheit
        fh = (t * 9 / 5) + 32 - 4  # -4 was calibration for my sensor

        # Print to screen
        oled_text("Sensor", "Temp = {0:0.1f}F".format(fh), "Humidity = {0:0.0f}%".format(h), "", "", "", ".|...")

    except OSError as e:
        oled_text("Error", "Failed to", "read sensor", "", "", "", "2")
        return "Failed to read sensor."


def fail():  # Test fail screen # SCREEN 4
    oled.fill(0)
    oled.text("Draw", 0, 0)  # Set some text
    #oled.fill_rect(15, 15, 44, 44, 1)
    # oled.rect(10, 10, 40, 40, 1)
    # oled.line(0,0,64,64,1)
    # oled.triangle(10, 10, 55, 20, 5, 40, 1)
    # oled.circle(64, 32, 10, 1)
    oled.round_rect(20,20,30,30,3,1)
    oled.show()


def info():  # Get and display Info # SCREEN 2
    if ap.active():
        ip = str(ap.ifconfig()[0])
    else:
        ip = "Wifi Off"

    mfreq = str(machine.freq())
    raw = str(esp32.raw_temperature())
    print(ip)

    oled_text("Info", ip, "CPU temp = " + raw + "F", "", mfreq, "", "..|..")
    gc.collect()


def dfree():  # Display remaining free space # SCREEN 3
    global stop
    am = str(alarm_1)

    bits = statvfs('/flash')
    # print(str(bits))
    blksize = bits[0]  # 4096
    blkfree = bits[3]  # 12
    freesize = blksize * blkfree  # 49152
    mbcalc = 1024 * 1024  # 1048576
    mbfree = freesize / mbcalc  # 0.046875
    freestr = str(mbfree)

    oled_text("Space(MB)", "curr: " + freestr, "", "Old:  " + "1.949219", "", am, "...|.")
    gc.collect()


def scralarm():
    var = str(adc.read())
    am = str(alarm_1)

    oled_text("Screen", "Alarm_1 = " + am, var, "", "", "", "|....")


# On Interupt button ------------------------------------------------------------------- #
def my_func(self):  # push button tests
    global stop
    global ScreenSelect

    stop = False
    led.on()
    ScreenSelect += 1
    print(ScreenSelect)
    led.off()

    # check if the device woke from a deep sleep
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')


# MAIN LOOP ---------------------------------------------------------------------------- #
while True:
    btn.irq(my_func, Pin.IRQ_RISING)

    alarm_1 = alarm_1 - 1
    if alarm_1 <= 0:
        alarm_1 = a1max

    if alarm_1 == 1:
        print("alarm_1")

    alarm_2(10)
    if alarm_2 == 1:
        print("alarm 2")

    if ScreenSelect > 5:
        gc.collect()
        ScreenSelect = 0

    if ScreenSelect == 0:
        scralarm()

    if ScreenSelect == 1 and alarm_1 == 1:
        temp()

    if ScreenSelect == 2:
        info()

    if ScreenSelect == 3:
        dfree()

    if ScreenSelect == 4:
        fail()

    if ScreenSelect == 5:
        showlogo()

    time.sleep_ms(500)  # For stability
