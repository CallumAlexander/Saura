import serial
import os
import sys
#import pandas as pd
clear = lambda: os.system("cls")
import xlsxwriter
import numpy as np
import time
from graphics import Intro, Title
from tkinter import *
from tkinter import messagebox

root = Tk()
top = Frame(root)

comVar = ''
loc = [0,0,0]
temp = 0
pressure = 0
alt = 0
action = ''






def Connect():
    global ser
    comVar = entCOM.get()
    comVar = 'COM' + comVar
    print('Using Port ' + comVar)

    try:
        ser = serial.Serial()
        print(' -------------------')
        print(' pyserial set up')
        ser.baudrate = 115200
        print(' Baudrate set to -115200-')
        ser.port = comVar
        print(' Port name confirmed as -' + comVar + '-')
        ser.open()
        print(' Port opening attempted...')
        time.sleep(0.2)
        print(' Port open successful : ' + str(ser.is_open))
        print(' -------------------')
    except:
        messagebox.showinfo("Error", "Failed to Connect")
        return

    currentline1 = ser.readline()
    currentline1 = currentline1.decode("utf-8")
    currentline2 = ser.readline()
    currentline2 = currentline2.decode("utf-8")

    if currentline1[1] == "e":
        print('DATA RECEIVED 1')
        messagebox.showinfo("Success", "Connection Established")
    elif currentline2[1] == "e":
        print('DATA RECEIVED 2')
        messagebox.showinfo("Success", "Connection Established")
    else:
        print('NO DATA')
        print(currentline1)
        print(currentline2)
        messagebox.showinfo("Error", "NO DATA RECIEVED")
        return

    
    lblCOM.place_forget()
    entCOM.place_forget()
    btnConnect.place_forget()

    lblDur.place(x=20,y=50)
    entDur.place(x=150,y=50)
    btnRecord.place(x=20,y=100)








def Record():
    global ser
    global vals
    global period

    temp = 0
    alt = 0

    tempDiff = 0
    lastTemp = 0
    
    altDiff = 0
    lastAlt = 0

    period = int(entDur.get())
    print(period)
    
    vals = np.zeros([period + 1,7])
    print(vals)

    step = 0
    initTime = time.time()

    while step <= period:
        currentTime = time.time()
        tStamp = currentTime - initTime

        currentline1 = ser.readline()
        currentline1 = currentline1.decode("utf-8")
        currentline2 = ser.readline()
        currentline2 = currentline2.decode("utf-8")

        clear()

        if currentline1[1] == 'e':
            alt, temp, loc[:] = preprocess(currentline1, step, temp, alt,tStamp)
        else:
            alt, temp, loc[:] = preprocess(currentline2, step, temp, alt,tStamp)
        
        tempDiff = temp - lastTemp
        altDiff = alt - lastAlt
        
        print(' ')
        print(' ')
        print(' Time stamp : '+ str(tStamp))
        print(' ')
        print(' Readings : ' + str(step) + ' readings elapsed since takeoff')
        print(' ')
        print(' Co-ordinates - ' +  ''.join(str(i) for i in loc)
        )
        print(' ')

        print(' Temperature --- ' + str(temp))
        if temp > lastTemp:
            print(' >>>')
        else:
            print(' <<<')
        print(' dif: ' + str(round(tempDiff, 1)))
        print('------------------------------')
        
        
        #Displaying altitude
        print('------------------------------')
        print(' Altitude --- ' + str(round(alt, 2)))
        if alt > lastAlt:
            print(' >>>')
        else:
            print(' <<<')
        print(' dif: ' + str(round(altDiff, 1)))
        print('------------------------------')

        lastAlt = alt
        lastTemp = temp

        currentTime = 0
        step += 1
        time.sleep(0.5)

    lblDur.place_forget()
    entDur.place_forget()
    btnRecord.place_forget()

    lblExpo.place(x=20,y=50)
    entExpo.place(x=230,y=50)
    btnExport.place(x=20,y=100)
    btnRestart.place(x=20,y=150)
    btnEnd.place(x=20,y=200)




def preprocess(currentline, step, temp, alt,tStamp):
    currentline = currentline[15:]
    transfer = [0,0,0,0,0,0]
    loc = [0,0,0]
    loc[0], loc[1], loc[2], alt, temp = currentline.split(",")

    global vals

    #while True:
        #try:
            #loc[1] = transfer[1]
            #break
        #except IndexError:
            #print("Error - restarting, lol just proved the heisenbug but now I've captured it haha x")
            #StartDisplay(period, loc, temp, alt, comVar, pressure)
            
    
    alt = float(alt)
    #print(alt)

    temp = temp[:-3]
    temp = float(temp)

    transfer[0] = tStamp
    transfer[1] = loc[0]
    transfer[2] = loc[1]
    transfer[3] = loc[2]
    transfer[4] = alt
    transfer[5] = temp
    
    for i in range(0,6):
        vals[step,i] = transfer[i]
    print(vals)

    return alt, temp, loc[:]


def exporter():
    global period
    global vals
    sheet = entExpo.get()

    entExpo.place_forget()
    lblExpo.place_forget()
    btnExport.place_forget()
    btnRestart.place_forget()
    
    workbook = xlsxwriter.Workbook(sheet + '.xlsx')
    worksheet = workbook.add_worksheet()
    #chart = workbook.add_chart({'type': 'scatter'})

    bold = workbook.add_format({'bold': 1})
 
    worksheet.write('B2', 'x', bold)
    worksheet.write('C2', 'x', bold)
    worksheet.write('D2', 'y', bold)
    worksheet.write('E2', 'z', bold)
    worksheet.write('F2', 'altitude', bold)
    worksheet.write('G2', 'temp', bold)

    for i in range(0,period+1):
        for a in range(0,6):
            worksheet.write((i + 2), (a + 1), vals[i,a])
    
    '''chart.add_series({'categories': '=Sheet1!$B$3:$B$'+str(vals+2),
                      'values': '=Sheet1!$I$3:$I$'+str(vals+2),
                      'trendline': {
                            'type': 'linear',
                            'order': 1,
                        },})
    worksheet.insert_chart('A7', chart)
    '''

    btnRestart.place(x=20,y=50)
    btnEnd.place(x=20,y=100)

    messagebox.showinfo("Success", "Successfully exported to file " + sheet + ".xlsx")

    workbook.close()

def Restart():
    btnExport.place_forget()
    btnRestart.place_forget()
    btnEnd.place_forget()

    lblCOM.place(x=20,y=50)
    entCOM.place(x=150,y=50)
    btnConnect.place(x=20,y=100)

def finish():
    global ser
    ser.close()
    root.destroy()

#Intro()
global ser
ser = ''
period = 0

frame = Frame(root,width=600,height=600)
frame.pack()

#SETUP
lblCOM = Label(root,text="COM Port:" ,font = "Helvetica 16")
entCOM = Entry(root,width=10, font = "Helvetica 16")
lblT = Label(root,text="Duration(s):" ,font = "Helvetica 16")
entT = Entry(root,width=10, font = "Helvetica 16")
btnConnect = Button(root,text="Connect", font="Helvetica 16",command=Connect)

lblCOM.place(x=20,y=50)
entCOM.place(x=150,y=50)
#lblT.place(x=20,y=100)
#entT.place(x=150,y=100)
btnConnect.place(x=20,y=100)

lblDur = Label(root, text="Duration(s):", font="Helvetica 16")
entDur = Entry(root, width="10", font="Helvetica 16")
btnRecord = Button(root, text="Record", font="Helvetica 16",command=Record)

lblExpo = Label(root, text="Export to file name:", font="Helvetica 16")
entExpo = Entry(root, width="10", font="Helvetica 16")
btnExport = Button(root, text="Export", font="Helvetica 16",command=exporter)
btnRestart = Button(root, text="Restart", font="Helvetica 16",command=Restart)
btnEnd = Button(root, text="End", font="Helvetica 16",command=finish)


root.mainloop()