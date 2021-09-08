# ----------- #

import os
import board as bd
import gfx
import webrepl
from ftp import *
import uasyncio


gc.enable()
gc.collect()

webrepl.start(password="password")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
# uftpd.start

gfx.gwifi(gfx.YELLOW)
ifinfo = bd.STA("NETGEAR90", "curlyearth685")
gfx.g_update(gfx.YELLOW)
pip = str(ifinfo.ifconfig()[0])
gfx.text(pip, 1, 1, gfx.BLACK, gfx.YELLOW)

something = 0
ftpserver()

async def init_update():

    HTML = """

<form action="/?upload" method="post" enctype="multipart/form-data">
<input type="file" name="upload" />
<input type="submit" /></form>


    """

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(4096).decode()
        request = str(request)

        print("")
        # print(request)

        if something == 1:
            print('open')
            f = open('test.bin', 'w')
            print('write')
            f.write(request)
            print('done')
            gc.collect()

            print(os.listdir())

            print(f.read())

        response = HTML

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

        await uasyncio.sleep_ms(500)


loop = uasyncio.get_event_loop()

loop.create_task(init_update())
loop.create_task(init_update())

loop.run_forever()