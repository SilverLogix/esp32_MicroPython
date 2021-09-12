# ----------- #

import gc

import webrepl

import board as bd
from HOLD import ftptiny

gc.enable()
gc.collect()


def init_update():
    print("")
    print("UPDATE MODE")
    print("")

    webrepl.start(password="password")

    ifinfo = bd.STA("NETGEAR90", "curlyearth685")

    print("")
    print("")

    ftp = ftptiny.FtpTiny()  # create one
    ftp.start()  # start an ftp thread