import st7789 as st
from machine import Pin,SPI
from micropython import const
tft=st.ST7789(SPI(1,baudrate=30000000,sck=Pin(18),mosi=Pin(19)),135,240,reset=Pin(23,Pin.OUT),cs=Pin(5,Pin.OUT),dc=Pin(16,Pin.OUT),backlight=Pin(4,Pin.OUT),rotation=3)
tft.init()
ST77XX_DISPOFF=const(0x28)
ST77XX_DISPON=const(0x29)
BLACK=const(0x0000)
BLUE=const(0x001F)
RED=const(0xF800)
GREEN=const(0x07E0)
CYAN=const(0x07FF)
MAGENTA=const(0xF81F)
YELLOW=const(0xFFE0)
WHITE=const(0xFFFF)
def backlight(swt):
 global tft
 if swt==1:
  tft=st.ST7789(SPI(1,baudrate=30000000,sck=Pin(18),mosi=Pin(19)),135,240,reset=Pin(23,Pin.OUT),cs=Pin(5,Pin.OUT),dc=Pin(16,Pin.OUT),backlight=Pin(4,Pin.OUT),rotation=3)
 if swt==0:
  tft=st.ST7789(SPI(1,baudrate=30000000,sck=Pin(18),mosi=Pin(19)),135,240,reset=Pin(23,Pin.OUT),cs=Pin(5,Pin.OUT),dc=Pin(16,Pin.OUT),backlight=Pin(4,Pin.IN),rotation=3)
def fill(col):
 tft.fill(col)
def text(string:str,x:int,y:int,fg=WHITE,bg=BLACK):
 from HOLD import font
 tft.text(font, string, x, y, fg, bg)
def pixel(x,y,col):
 tft.pixel(x,y,col)
def scroll(dx,dy):
 tft.scroll(dx,dy)
def text_long(otitle,oline1,oline2,oline3,oline4,oline5,oline6,oline7,fg=WHITE,bg=BLACK):
 from HOLD import font
 tft.text(font, otitle, 0, 0, YELLOW, bg)
 tft.text(font, oline1, 0, 18, fg, bg)
 tft.text(font, oline2, 0, 34, fg, bg)
 tft.text(font, oline3, 0, 50, fg, bg)
 tft.text(font, oline4, 0, 66, fg, bg)
 tft.text(font, oline5, 0, 82, fg, bg)
 tft.text(font, oline6, 0, 98, fg, bg)
 tft.text(font, oline7, 0, 114, fg, bg)
def rect(x,y,w,h,col):
 tft.rect(x,y,w,h,col)
def fill_rect(x,y,w,h,col):
 tft.fill_rect(x,y,w,h,col)
def hline(x,y,w,col):
 tft.hline(x,y,w,col)
def vline(x,y,h,col):
 tft.vline(x,y,h,col)
def line(x1,y1,x2,y2,col):
 tft.line(x1,y1,x2,y2,col)
def triangle(x0,y0,x1,y1,x2,y2,col):
 tft.line(x0,y0,x1,y1,col)
 tft.line(x1,y1,x2,y2,col)
 tft.line(x2,y2,x0,y0,col)
def circle(x0,y0,radius,col):
 f=1-radius
 ddf_x=1
 ddf_y=-2*radius
 x=0
 y=radius
 tft.pixel(x0,y0+radius,col)
 tft.pixel(x0,y0-radius,col)
 tft.pixel(x0+radius,y0,col)
 tft.pixel(x0-radius,y0,col)
 while x<y:
  if f>=0:
   y-=1
   ddf_y+=2
   f+=ddf_y
  x+=1
  ddf_x+=2
  f+=ddf_x
  tft.pixel(x0+x,y0+y,col)
  tft.pixel(x0-x,y0+y,col)
  tft.pixel(x0+x,y0-y,col)
  tft.pixel(x0-x,y0-y,col)
  tft.pixel(x0+y,y0+x,col)
  tft.pixel(x0-y,y0+x,col)
  tft.pixel(x0+y,y0-x,col)
  tft.pixel(x0-y,y0-x,col)
def round_rect(x0,y0,width,height,radius,col):
 x0+=radius
 y0+=radius
 radius=int(min(radius,width/2,height/2))
 if radius:
  f=1-radius
  ddf_x=1
  ddf_y=-2*radius
  x=0
  y=radius
  tft.vline(x0-radius,y0,height-2*radius+1,col) 
  tft.vline(x0+width-radius,y0,height-2*radius+1,col) 
  tft.hline(x0,y0+height-radius+1,width-2*radius+1,col) 
  tft.hline(x0,y0-radius,width-2*radius+1,col) 
  while x<y:
   if f>=0:
    y-=1
    ddf_y+=2
    f+=ddf_y
   x+=1
   ddf_x+=2
   f+=ddf_x
   tft.pixel(x0-y,y0-x,col) 
   tft.pixel(x0-x,y0-y,col) 
   tft.pixel(x0+x+width-2*radius,y0-y,col) 
   tft.pixel(x0+y+width-2*radius,y0-x,col) 
   tft.pixel(x0+y+width-2*radius,y0+x+height-2*radius,col) 
   tft.pixel(x0+x+width-2*radius,y0+y+height-2*radius,col) 
   tft.pixel(x0-x,y0+y+height-2*radius,col) 
   tft.pixel(x0-y,y0+x+height-2*radius,col) 
def wipe(col):
 from HOLD import font
 tft.fill(col)
 tft.text(font, "                  ", 0, 0, col, col)
 tft.text(font, "                  ", 0, 18, col, col)
 tft.text(font, "                  ", 0, 34, col, col)
 tft.text(font, "                  ", 0, 50, col, col)
 tft.text(font, "                  ", 0, 66, col, col)
 tft.text(font, "                  ", 0, 82, col, col)
 tft.text(font, "                  ", 0, 98, col, col)
 tft.text(font, "                  ", 0, 114, col, col)
def boot(col=BLACK):
 from HOLD import font
 tft.fill(col)
 tft.text(font, "Boot", 0, tft.height() - 16, WHITE, 0)
def gwifi(col=BLACK):
 from HOLD import font
 tft.fill(col)
 tft.text(font, "WIFI", 0, tft.height() - 16, WHITE, 0)
def g_update(col=BLACK):
 from HOLD import font
 tft.fill(col)
 tft.text(font, "UPDATE", 0, tft.height() - 16, WHITE, 0)
def micrologo(col=BLACK):
 from HOLD import font
 tft.fill(col)
 tft.jpg('logo.jpg',0,0,1)
 tft.text(font, " MICROPYTHON ", int(tft.width() / 2 - 105), int(tft.height() - 18), WHITE, 0)