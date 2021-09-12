import threading
import time

import PySimpleGUI as Sg
import serial

choices = ('/dev/ttyUSB0', 'COM2', 'COM3', 'COM4')
combo = "/dev/ttyUSB0"
enter = "help()"
isconnected = False
ser = serial.Serial(str(combo), 115200)

Sg.theme('DarkGrey14')  # Add a little color to your windows

# All the stuff inside your window. This is the PSG magic code compactor...
tab1_layout = [
    [Sg.Text('', size=(12, 1))],
    [Sg.Text("Select port:"), Sg.Combo(choices, size=(36, len(choices)), key='-COMCHOICE-', enable_events=True),
     Sg.Button("Connect", key='-CONN-')],
    [Sg.Text("Enter:        "), Sg.InputText("", size=(38, 4), key='-ENTER-'), Sg.Button("  Send  ", key='-SEND-')],
    [Sg.Button("Test", key='-TEST-')],
    [Sg.Text('', size=(12, 1))],
    [Sg.Text('Console', size=(12, 1))],
    [Sg.Output(size=(60, 20), key='-OUTPUT-')],
]

tab2_layout = [
    [Sg.T('This is inside tab 2')],
    [Sg.In(key='in')]
]

layout = [
    [Sg.TabGroup([[Sg.Tab('Serial', tab1_layout), Sg.Tab('Files', tab2_layout)]])],
]


def runout():
    global ser
    global isconnected

    print("")
    print(">> trying to connect to port " + combo)
    time.sleep(0.05)
    answer = ser.readline()
    if answer != "":
        print("\n>> Connected!\n")
        isconnected = True

    data = []  # empty list to store the data
    for i in range(255):
        b = ser.readline()  # read a byte string
        string_n = b.decode()  # decode byte string into Unicode
        string = string_n.rstrip()  # remove \n and \r
        flt = string  # convert string to float
        print(flt)
        data.append(flt)  # add to the end of data list
        time.sleep(0.1)  # wait (sleep) 0.1 seconds

    ser.close()


def send_data():
    global ser
    ser.write(enter.encode())


# Create the Window
window = Sg.Window('Window Title', layout)

# Event Loop to process "events"
while True:
    event, values = window.read()
    combo = values['-COMCHOICE-']  # use the combo key
    enter = values['-ENTER-']
    # print(event, values)
    if event in (Sg.WIN_CLOSED, 'Cancel'):
        break

    if event == "-TEST-":
        msg = '\x03'

        ser.write(enter.encode())
        time.sleep(0.5)
        ser.readline()

    if event == "-CONN-":
        if not isconnected:
            x = threading.Thread(target=runout, daemon=True)
            x.start()
        else:
            print("\n>> Port already Opened!\n")

    if event == "-SEND-":
        msg = values['-ENTER-']  # use the combo key
        # msg = 'ZANE:1:00004:XX_X.X_XXXX_000XX:\r\n'
        ser.write(enter.encode())
        time.sleep(0.5)
        ser.readline()
        # print(msg)

window.close()
