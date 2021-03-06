from machine import Pin, PWM
import time
from notes import *

mario = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0, G6, 0, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0, C7, D7, B6, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0, C7, D7, B6, 0, 0]

pwm0 = PWM(Pin(15))

for i in mario:
    pwm0.freq(int(i))
    pwm0.duty(512)          # set duty cycle
    print(i)
    time.sleep(0.20)
else:
    pwm0.deinit()