import micropython
import gc
import machine
import debug
from TFTinit import *

# import webrepl


micropython.alloc_emergency_exception_buf(100)
print('Booting...')

tft_boot()

# DO NOT GO BELOW 80Mhz!!!  Will break wifi and complicate serial!
# machine.freq(240000000) # set the CPU frequency to 240 MHz
# machine.freq(160000000)  # set the CPU frequency to 160 MHz

# noinspection PyArgumentList
machine.freq(80000000)  # set the CPU frequency to 80 MHz

# webrepl.start(password="password")

debug.space_free()
debug.m_freq()
debug.raw_temp()
debug.showVoltage()

gc.collect()
