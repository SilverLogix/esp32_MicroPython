# ---------- #

import gc
import socket
import utime
from machine import Pin

# Custom imports
import gfx
from board import STA
import debug
import ftptiny

# =============== Init Board =============== #
gc.enable()

btn0 = Pin(0, Pin.IN)   # Gpio 0  as button
btn1 = Pin(35, Pin.IN)  # Gpio 35 as button

led = Pin(2, Pin.OUT)

# noinspection PyArgumentList
machine.freq(240000000)
debug.pprint()
gc.collect()

# ============================================== #


# ---------- Definitions ---------- #

# def deep_sleep(ms):
# put the device to sleep for 10 seconds
# machine.deepsleep(ms)


# ------------------------------------- #


#             Nothing here              #


# ------------------------------------- #


# ---------- Boot up ---------- #
ifinfo = STA("routerNAME", "PASSWORD")
print("")

gfx.fill(gfx.RED)
utime.sleep_ms(50)
gfx.fill(gfx.YELLOW)
utime.sleep_ms(50)
gfx.fill(gfx.GREEN)
utime.sleep_ms(50)
gfx.fill(gfx.WHITE)

f1 = 'off'
ftp_check = 0
led_check = 1


def web_page():
    gc.collect()

    if led_check == 1:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    if ftp_check == 1:
        ftp_state = "ON"
    else:
        ftp_state = "OFF"

    # ---------- Webpage goes here ---------- #
    html = """
    <html>
      <head> 
      <title>ESP Web Server</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="icon" href="data:,">
        <style>
          html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
          body{background-color: black;}
          h1{color: #0F3376; padding: 2vh;}
          p{color: white; font-size: 1.2rem;}
          .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
          .button2{background-color: #4286f4;}
          .button3{background-color: #F286f4;}
          .button4{background-color: #9d2424;}
        </style>
      </head>
      <body> 
        <h1>ESP Web Server</h1> 
        <p>Backlight:  <strong>""" + gpio_state + """</strong></p>
        <p>FTP Server:  <strong>""" + ftp_state + """</strong></p>
        <p></p>
        <p><a href="/?led=on">  <button class="button button">ON</button>     </a></p>
        <p><a href="/?led=off"> <button class="button button2">OFF</button>   </a></p>
        <p><a href="/?ftp=on">  <button class="button button3">FTP</button>   </a></p>
        <p><a href="/?reset">   <button class="button button4">RESET</button> </a></p>
      </body>
    </html>
    """
    return html


# ---------- Init webpage vars ---------- #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# --------- RUN --------- #
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')

    ftp_on = request.find('/?ftp=on')

    reset = request.find('/?reset')

    # text
    if led_on == 6:
        print('LED ON')
        led_check = 1
        gfx.backlight(1)

    if led_off == 6:
        print('LED OFF')
        led_check = 0
        gfx.backlight(0)

    if ftp_on == 6:
        print('FTP ON')
        ftp_check = 1
        ftp = ftptiny.FtpTiny()  # create one
        ftp.start()  # start an ftp thread

    if reset == 6:
        machine.deepsleep(500)

    response = web_page()
    # noinspection PyTypeChecker
    conn.send('HTTP/1.1 200 OK\n')
    # noinspection PyTypeChecker
    conn.send('Content-Type: text/html\n')
    # noinspection PyTypeChecker
    conn.send('Connection: close\n\n')
    # noinspection PyTypeChecker
    conn.sendall(response)
    conn.close()
