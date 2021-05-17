# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
# Advanced functions by Silverlogix
# Modified to actually work right by SilverLogix

import time

import framebuf
from micropython import const

# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xa4)
SET_NORM_INV = const(0xa6)
SET_DISP = const(0xae)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xa0)
SET_MUX_RATIO = const(0xa8)
SET_COM_OUT_DIR = const(0xc0)
SET_DISP_OFFSET = const(0xd3)
SET_COM_PIN_CFG = const(0xda)
SET_DISP_CLK_DIV = const(0xd5)
SET_PRECHARGE = const(0xd9)
SET_VCOM_DESEL = const(0xdb)
SET_CHARGE_PUMP = const(0x8d)

__version__ = "0.4"
__repo__ = "https://github.com/SilverLogix/esp32_MicroPython.git"


# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=undefined-variable
class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations (I2C needs an extra byte).
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
                SET_DISP | 0x00,  # off
                # address setting
                SET_MEM_ADDR, 0x00,  # horizontal
                # resolution and layout
                SET_DISP_START_LINE | 0x00,
                SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
                SET_MUX_RATIO, self.height - 1,
                SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
                SET_DISP_OFFSET, 0x00,
                SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
                # timing and driving scheme
                SET_DISP_CLK_DIV, 0x80,
                SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
                SET_VCOM_DESEL, 0x30,  # 0.83*Vcc
                # display
                SET_CONTRAST, 0xff,  # maximum
                SET_ENTIRE_ON,  # output follows RAM contents
                SET_NORM_INV,  # not inverted
                # charge pump
                SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
                SET_DISP | 0x01):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    # Screen Commands ------------------------------------------------------------------ #
    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)

    def text_long(self, otitle, oline1, oline2, oline3, oline4, oline5):
        self.framebuf.text(otitle, 0, 0)

        self.framebuf.text(oline1, 0, 16)
        self.framebuf.text(oline2, 0, 26)
        self.framebuf.text(oline3, 0, 36)
        self.framebuf.text(oline4, 0, 46)
        self.framebuf.text(oline5, 0, 56)

    def menu_pix(self, loc):
        opix = [125, 120, 115, 110, 105, 100]
        for x in opix:
            self.framebuf.pixel(x, 4, 1)

        if loc == 0:
            ll = 100
        if loc == 1:
            ll = 105
        if loc == 2:
            ll = 110
        if loc == 3:
            ll = 115
        if loc == 4:
            ll = 120
        if loc == 5:
            ll = 125
        if loc == 6:
            ll = 130

        self.framebuf.pixel(ll - 1, 4, 1)
        self.framebuf.pixel(ll + 1, 4, 1)
        self.framebuf.pixel(ll, 4 - 1, 1)
        self.framebuf.pixel(ll, 4 + 1, 1)

    def rect(self, x, y, w, h, col):
        self.framebuf.rect(x, y, w, h, col)

    def fill_rect(self, x, y, w, h, col):
        self.framebuf.fill_rect(x, y, w, h, col)

    def hline(self, x, y, w, col):
        self.framebuf.hline(x, y, w, col)

    def vline(self, x, y, h, col):
        self.framebuf.vline(x, y, h, col)

    def line(self, x1, y1, x2, y2, col):
        self.framebuf.line(x1, y1, x2, y2, col)

    def triangle(self, x0, y0, x1, y1, x2, y2, col):
        # Triangle drawing function.  Will draw a single pixel wide triangle
        # around the points (x0, y0), (x1, y1), and (x2, y2).
        self.framebuf.line(x0, y0, x1, y1, col)
        self.framebuf.line(x1, y1, x2, y2, col)
        self.framebuf.line(x2, y2, x0, y0, col)

    def circle(self, x0, y0, radius, col):
        # Circle drawing function.  Will draw a single pixel wide circle with
        # center at x0, y0 and the specified radius.
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        self.framebuf.pixel(x0, y0 + radius, col)
        self.framebuf.pixel(x0, y0 - radius, col)
        self.framebuf.pixel(x0 + radius, y0, col)
        self.framebuf.pixel(x0 - radius, y0, col)
        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            self.framebuf.pixel(x0 + x, y0 + y, col)
            self.framebuf.pixel(x0 - x, y0 + y, col)
            self.framebuf.pixel(x0 + x, y0 - y, col)
            self.framebuf.pixel(x0 - x, y0 - y, col)
            self.framebuf.pixel(x0 + y, y0 + x, col)
            self.framebuf.pixel(x0 - y, y0 + x, col)
            self.framebuf.pixel(x0 + y, y0 - x, col)
            self.framebuf.pixel(x0 - y, y0 - x, col)

    def round_rect(self, x0, y0, width, height, radius, col):
        """Rectangle with rounded corners drawing function.
        This works like a regular rect though! if radius = 0
        Will draw the outline of a rectangle with rounded corners with (x0,y0) at the top left"""
        # shift to correct for start point location
        x0 += radius
        y0 += radius

        # ensure that the radius will only ever half of the shortest side or less
        radius = int(min(radius, width / 2, height / 2))

        if radius:
            f = 1 - radius
            ddf_x = 1
            ddf_y = -2 * radius
            x = 0
            y = radius
            self.framebuf.vline(x0 - radius, y0, height - 2 * radius + 1, col)  # left
            self.framebuf.vline(x0 + width - radius, y0, height - 2 * radius + 1, col)  # right
            self.framebuf.hline(x0, y0 + height - radius + 1, width - 2 * radius + 1, col)  # bottom
            self.framebuf.hline(x0, y0 - radius, width - 2 * radius + 1, col)  # top
            while x < y:
                if f >= 0:
                    y -= 1
                    ddf_y += 2
                    f += ddf_y
                x += 1
                ddf_x += 2
                f += ddf_x
                # angle notations are based on the unit circle and in diection of being drawn

                # top left
                self.framebuf.pixel(x0 - y, y0 - x, col)  # 180 to 135
                self.framebuf.pixel(x0 - x, y0 - y, col)  # 90 to 135

                # top right
                self.framebuf.pixel(x0 + x + width - 2 * radius, y0 - y, col)  # 90 to 45
                self.framebuf.pixel(x0 + y + width - 2 * radius, y0 - x, col)  # 0 to 45

                # bottom right
                self.framebuf.pixel(x0 + y + width - 2 * radius, y0 + x + height - 2 * radius, col)  # 0 to 315
                self.framebuf.pixel(x0 + x + width - 2 * radius, y0 + y + height - 2 * radius, col)  # 270 to 315

                # bottom left
                self.framebuf.pixel(x0 - x, y0 + y + height - 2 * radius, col)  # 270 to 255
                self.framebuf.pixel(x0 - y, y0 + x + height - 2 * radius, col)  # 180 to 225


# ---------------------------------------------------------------------------------------------------#


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        # Blast out the frame buffer using a single I2C transaction to support
        # hardware I2C interfaces.
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        pass


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        self.buffer = bytearray((height // 8) * width)
        self.framebuf = framebuf.FrameBuffer1(self.buffer, width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.high()
        self.dc.low()
        self.cs.low()
        self.spi.write(bytearray([cmd]))
        self.cs.high()

    def write_framebuf(self):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.high()
        self.dc.high()
        self.cs.low()
        self.spi.write(self.buffer)
        self.cs.high()

    def poweron(self):
        self.res.high()
        time.sleep_ms(1)
        self.res.low()
        time.sleep_ms(10)
        self.res.high()
