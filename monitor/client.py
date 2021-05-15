import threading

import PySimpleGUI as sg
import time
import serial

choices = ('COM1', 'COM2', 'COM3', 'COM4')
combo = "COM1"
enter = "help()"
isconnected = False

sg.theme('DarkGrey14')  # Add a little color to your windows

# All the stuff inside your window. This is the PSG magic code compactor...
tab1_layout = [
    [sg.Text('', size=(12, 1))],
    [sg.Text("Select port:"),       sg.Combo(choices, size=(36, len(choices)), key='-COMCHOICE-', enable_events=True),  sg.Button("Connect",  key='-CONN-')],
    [sg.Text("Enter:        "),     sg.InputText("", size=(38, 4), key='-ENTER-'),                                      sg.Button("  Send  ", key='-SEND-')],
    [sg.Button("Test", key='-TEST-')],
    [sg.Text('', size=(12, 1))],
    [sg.Text('Console', size=(12, 1))],
    [sg.Output(size=(60, 20), key='-OUTPUT-')],
]

tab2_layout = [
    [sg.T('This is inside tab 2')],
    [sg.In(key='in')]
]


layout = [
    [sg.TabGroup([[sg.Tab('Serial', tab1_layout), sg.Tab('Files', tab2_layout)]])],
]

def runout():
    global isconnected, ser
    ser = serial.Serial(str(combo), 115200)

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
        flt = (string)  # convert string to float
        print(flt)
        data.append(flt)  # add to the end of data list
        time.sleep(0.1)  # wait (sleep) 0.1 seconds

    ser.close()


def sendData():
    global ser
    ser.write(enter.encode())



# Create the Window
window = sg.Window('Window Title', layout)

# Event Loop to process "events"
while True:
    event, values = window.read()
    combo = values['-COMCHOICE-']  # use the combo key
    enter = values['-ENTER-']
    #print(event, values)
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == "-TEST-":
        msg = '\x03'

        ser.write(msg.encode())
        time.sleep(0.5)
        ser.readline()

    if event == "-CONN-":
        if isconnected == False:
            x = threading.Thread(target=runout, daemon=True)
            x.start()
        else:
            print("\n>> Port already Opened!\n")

    if event == "-SEND-":
        msg = values['-ENTER-']  # use the combo key
        #msg = 'ZANE:1:00004:XX_X.X_XXXX_000XX:\r\n'
        ser.write(msg.encode())
        time.sleep(0.5)
        ser.readline()
        #print(msg)

window.close()
