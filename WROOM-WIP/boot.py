import micropython
import machine
from machine import Pin
import gfx
# from utime import sleep_ms

# noinspection PyArgumentList
machine.freq(240000000)  # Anything below 80Mhz will break WiFi
micropython.alloc_emergency_exception_buf(100)

print(str('Booting...'))
btn = Pin(35, Pin.IN)  # Gpio 35 as button
UPDATE = bool(False)

gfx.boot()  # Show boot logo

if btn.value() == 0:  # Hold down btn for update mode
    import update
    UPDATE = True
    update.init_update()

if UPDATE:  # If update mode active, do NOT load main.py
    quit()
