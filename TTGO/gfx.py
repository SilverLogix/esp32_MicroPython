from machine import Pin, SPI
import st7789 as st
import font

# noinspection PyArgumentList
tft = st.ST7789(
    SPI(1, baudrate=30000000, sck=Pin(18), mosi=Pin(19)),
    135, 240,
    reset=Pin(23, Pin.OUT),
    cs=Pin(5, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=Pin(4, Pin.OUT),
    rotation=3)
tft.init()


def boot():
    tft.fill(st.RED)
    tft.text(font, "Boot", 0, tft.height() - 16, st.WHITE, 0)  # Boot text on screen


def gwifi():
    tft.fill(st.BLUE)
    tft.text(font, "WIFI", 0, tft.height() - 16, st.WHITE, 0)  # Boot text on screen


def micrologo():
    tft.fill(0)
    tft.jpg('logo.jpg', 0, 0, 1)
    tft.text(
        font,
        " MICROPYTHON ",
        int(tft.width() / 2 - 105), int(tft.height() - 18),
        st.color565(255, 255, 255),
        st.color565(1, 1, 1)
    )


def text_long(otitle, oline1, oline2, oline3, oline4, oline5, oline6, oline7, fg, bg):
    tft.text(font, otitle, 0, 0, st.YELLOW, bg)

    tft.text(font, oline1, 0, 18, fg, bg)
    tft.text(font, oline2, 0, 34, fg, bg)
    tft.text(font, oline3, 0, 50, fg, bg)
    tft.text(font, oline4, 0, 66, fg, bg)
    tft.text(font, oline5, 0, 82, fg, bg)
    tft.text(font, oline6, 0, 98, fg, bg)
    tft.text(font, oline7, 0, 114, fg, bg)


def triangle(x0, y0, x1, y1, x2, y2, col):
    # Triangle drawing function.  Will draw a single pixel wide triangle
    # around the points (x0, y0), (x1, y1), and (x2, y2).
    tft.line(x0, y0, x1, y1, col)
    tft.line(x1, y1, x2, y2, col)
    tft.line(x2, y2, x0, y0, col)


def wipe(col):
    tft.fill(col)
    tft.text(font, "                ", 0, 0,   col, col)

    tft.text(font, "                ", 0, 18,  col, col)
    tft.text(font, "                ", 0, 34,  col, col)
    tft.text(font, "                ", 0, 50,  col, col)
    tft.text(font, "                ", 0, 66,  col, col)
    tft.text(font, "                ", 0, 82,  col, col)
    tft.text(font, "                ", 0, 98,  col, col)
    tft.text(font, "                ", 0, 114, col, col)
