from os import statvfs
from machine import Pin, I2C, ADC
import dht
import time
import ssd1306
import esp32
# Custom imports
from boot import gc, ap, machine
from logo import showlogo

# Init Screen --------------------------------------------------#
i2c = I2C(-1, scl=Pin(22), sda=Pin(21)) 	# Set Pins
oled_width = int(128) 						# Width of OLED
oled_height = int(64) 						# Length of OLED
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(1)
oled.show()
time.sleep(0.2)
oled.fill(0)
oled.text("Screen", 38, 0) 					# Set some text
oled.show() 								# Show the text
# ------------------------------------------------------------- #


# Init basic variables
f = int(0)
ScreenSelect = int(0)

a1max = 99
alarm_1 = int(a1max)

# Init advanced variables
d = dht.DHT11(machine.Pin(4, machine.Pin.PULL_UP))

btn = Pin(0, Pin.IN)
led = Pin(2, Pin.OUT)
adc = ADC(Pin(35))

def oled_pix():
	oled.pixel(70, 4, 1)
	oled.pixel(75, 4, 1)
	oled.pixel(80, 4, 1)
	oled.pixel(85, 4, 1)

	oled.pixel(90, 3, 1)
	oled.pixel(89, 4, 1)
	oled.pixel(90, 5, 1)
	oled.pixel(91, 4, 1)




def oled_text(otitle, oline1, oline2, oline3, oline4, oline5, onum):  # (Title, Line#1, Line#2, Line#3, Line#4, Line#5, Screen#)
	oled.fill(0)

	oled.text(otitle, 0, 0)
	oled.text(onum, 90, 0)

	oled.text(oline1, 0, 16)
	oled.text(oline2, 0, 26)
	oled.text(oline3, 0, 36)
	oled.text(oline4, 0, 46)
	oled.text(oline5, 0, 56)


	oled.show()


def fill():  # Fill screen on/off
	global f
	if f == 0:
		oled.fill(1)
		oled.show()
		f = 1
	elif f == 1:
		oled.fill(0)
		oled.show()
		f = 0
	gc.collect()


# Screens ---------------------------------------------------------------------------------------- #
def temp():  # Get and display temperature # SCREEN 1
	try:
		# Get sensor readings
		d.measure()
		t = d.temperature()
		h = d.humidity()

		# Convert celsius to fahrenheit
		fh = (t * 9/5) + 32 - 4  # -4 was calibration for my sensor

		# Print to screen
		oled_text("Sensor", "Temp = {0:0.1f}F".format(fh), "Humidity = {0:0.0f}%".format(h), "", "", "", ".|...")

		time.sleep(1.0)

	except OSError as e:
		oled_text("Error", "Failed to", "read sensor", "", "", "", "2")
		return "Failed to read sensor."


def fail():  # Test fail screen # SCREEN 4
	oled_text("Test Error", "Failed to", "read something?", "", "", "01100101011101", "....|")


def info():  # Get and display Info # SCREEN 2
	mfreq = str(machine.freq())
	ip = str(ap.ifconfig()[0])
	raw = str(esp32.raw_temperature())

	oled_text("Info", ip, "CPU temp = " + raw + "F", "", mfreq, "", "..|..")
	gc.collect()


def dfree():  # Display remaining free space # SCREEN 3
	bits = statvfs('/flash')
	# print(str(bits))
	blksize = bits[0]  # 4096
	blkfree = bits[3]  # 12
	freesize = blksize * blkfree  # 49152
	mbcalc = 1024 * 1024  # 1048576
	mbfree = freesize / mbcalc  # 0.046875
	freestr = str(mbfree)

	oled_text("Space (MB)", freestr, "", "", "", "", "...|.")
	gc.collect()


def scralarm():
	var = str(adc.read())
	am = str(alarm_1)

	oled_text("Screen", "Alarm_1 = " + am, var, "", "", "", "|....")


# On Interupt button ------------------------------------------------------------------- #
def my_func(self):  # push button tests
	led.on()
	global ScreenSelect
	ScreenSelect += 1
	print(ScreenSelect)
	led.off()


# MAIN LOOP ---------------------------------------------------------------------------- #
while True:
	btn.irq(my_func, Pin.IRQ_RISING)
	# print(alarm_1)

	alarm_1 = alarm_1 - 1
	if alarm_1 <= 0:
		alarm_1 = a1max

	if ScreenSelect > 5:
		gc.collect()
		ScreenSelect = 0

	if ScreenSelect == 0:
		scralarm()

	if ScreenSelect == 1:
		temp()

	if ScreenSelect == 2:
		info()

	if ScreenSelect == 3:
		dfree()

	if ScreenSelect == 4:
		fail()

	if ScreenSelect == 5:
		showlogo()

	time.sleep(0.01)  # For stability
