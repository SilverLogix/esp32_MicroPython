"""
hello.py

    Writes "Hello!" in random colors at random locations on a
    LILYGO® TTGO T-Display.

    https://youtu.be/z41Du4GDMSY

"""
import gc
import random

import time
from machine import Pin, SPI
import st7789

import font


def main():
    tft = st7789.ST7789(
        SPI(1, baudrate=30000000, sck=Pin(18), mosi=Pin(19)),
        135,
        240,
        reset=Pin(23, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        dc=Pin(16, Pin.OUT),
        backlight=Pin(4, Pin.OUT),
        rotation=3)

    tft.init()
    tft.jpg('logo.jpg', 0, 0, 0)

    tft.text(
        font,
        " MICROPYTHON ",
        int(tft.width() / 2 - 105), int(tft.height() - 18),
        st7789.color565(255, 255, 255),
        st7789.color565(1, 1, 1)
    )

    time.sleep_ms(3000)
    gc.collect()

    while True:
        for rotation in range(4):
            tft.rotation(rotation)
            tft.fill(0)
            col_max = tft.width() - font.WIDTH * 6
            row_max = tft.height() - font.HEIGHT

            for _ in range(128):
                time.sleep_ms(100)
                tft.text(font, "Hello!",
                         random.randint(0, col_max),
                         random.randint(0, row_max),
                         st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8)),
                         st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8))
                         )


main()
