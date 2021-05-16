from os import statvfs
from machine import Pin,I2C,ADC
import dht
import time
import ssd1306
import esp32
from boot import gc,ap,machine
from logo import showlogo
i2c=I2C(-1,scl=Pin(22),sda=Pin(21)) 
oled_width=int(128) 
oled_height=int(64) 
oled=ssd1306.SSD1306_I2C(oled_width,oled_height,i2c)
oled.fill(1)
oled.show()
time.sleep_ms(200)
oled.fill(0)
oled.text("Screen",38,0) 
oled.show() 
alarm2=0
def alarm_2(maxcount):
 global alarm2
 if alarm2!=maxcount:
  alarm2=alarm2-1
 if alarm2<=0:
  alarm2=maxcount
 return alarm2
f=int(0)
ScreenSelect=int(0)
a1max=4
alarm_1=int(a1max)
d=dht.DHT11(machine.Pin(4,machine.Pin.PULL_UP))
btn=Pin(0,Pin.IN)
led=Pin(2,Pin.OUT)
adc=ADC(Pin(35))
stop=bool(False)
def oled_pix():
 oled.pixel(70,4,1)
 oled.pixel(75,4,1)
 oled.pixel(80,4,1)
 oled.pixel(85,4,1)
 oled.pixel(90,3,1)
 oled.pixel(89,4,1)
 oled.pixel(90,5,1)
 oled.pixel(91,4,1)
def oled_text(otitle,oline1,oline2,oline3,oline4,oline5,onum):
 oled.fill(0)
 oled.text(otitle,0,0)
 oled.text(onum,90,0)
 oled.text(oline1,0,16)
 oled.text(oline2,0,26)
 oled.text(oline3,0,36)
 oled.text(oline4,0,46)
 oled.text(oline5,0,56)
 oled.show()
def temp(): 
 try:
  d.measure()
  t=d.temperature()
  h=d.humidity()
  fh=(t*9/5)+32-4 
  oled_text("Sensor","Temp = {0:0.1f}F".format(fh),"Humidity = {0:0.0f}%".format(h),"","","",".|...")
 except OSError as e:
  oled_text("Error","Failed to","read sensor","","","","2")
  return "Failed to read sensor."
def fail(): 
 oled.fill(0)
 oled.text("Draw",0,0) 
 oled.fill_rect(15,15,44,44,1)
 oled.show()
def info(): 
 if ap.active():
  ip=str(ap.ifconfig()[0])
 else:
  ip="Wifi Off"
 mfreq=str(machine.freq())
 raw=str(esp32.raw_temperature())
 print(ip)
 oled_text("Info",ip,"CPU temp = "+raw+"F","",mfreq,"","..|..")
 gc.collect()
def dfree(): 
 global stop
 am=str(alarm_1)
 bits=statvfs('/flash')
 blksize=bits[0] 
 blkfree=bits[3] 
 freesize=blksize*blkfree 
 mbcalc=1024*1024 
 mbfree=freesize/mbcalc 
 freestr=str(mbfree)
 oled_text("Space (MB)",freestr,"","","",am,"...|.")
 gc.collect()
def scralarm():
 var=str(adc.read())
 am=str(alarm_1)
 oled_text("Screen","Alarm_1 = "+am,var,"","","","|....")
def my_func(self): 
 global stop
 global ScreenSelect
 stop=False
 led.on()
 ScreenSelect+=1
 print(ScreenSelect)
 led.off()
while True:
 btn.irq(my_func,Pin.IRQ_RISING)
 alarm_1=alarm_1-1
 if alarm_1<=0:
  alarm_1=a1max
 if alarm_1==2:
  print("alarm_1")
 alarm_2(10)
 if alarm_2==1:
  print("alarm 2")
 if ScreenSelect>5:
  gc.collect()
  ScreenSelect=0
 if ScreenSelect==0:
  scralarm()
 if ScreenSelect==1 and alarm_1==1:
  temp()
 if ScreenSelect==2:
  info()
 if ScreenSelect==3:
  dfree()
 if ScreenSelect==4:
  fail()
 if ScreenSelect==5:
  showlogo()
 time.sleep_ms(500) 
