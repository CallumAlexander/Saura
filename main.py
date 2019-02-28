# -*- coding: utf-8 -*-
# Property of Callum Alexander
# Instagram - @cal.zander
# Twitter - callum_alxndr
"""
@author: Callum
"""


'''
THIS CODE HAS NOT BEEN TESTED WITH THE COMS
USE AT YOUR OWN DISCRETION


'''
import serial
import os
import sys
#import pandas as pd
clear = lambda: os.system("cls")
import xlsxwriter
import numpy as np

import time
from graphics import Intro, Title



period = 0

loc = [0,0,0]
temp = 0
alt = 0
action = ''

def Control(action):
    action = input(' >>> ')
    
    if action == 'start':
        RecordingSetup()
    elif action == 'clear':
        clear()
        Title()
        Control(action)
    elif action == 'end':
        time.sleep(1)
        print(' Thank you for using Saura')
        time.sleep(1)
        print(' Saura is sponsored by Evolution Executive Search')
        time.sleep(3)
    elif action == 'credits':
        time.sleep(0.3)
        Credit()
    elif action =='home':
        time.sleep(0.3)
        Home()
    elif action == 'restart':
        time.sleep(0.3)
        print(' RESTARTING...')
        time.sleep(2)
        Restart()
    elif action == 'help':
        time.sleep(0.3)
        Help()
    else:
        clear()
        Title()
        print(' Invalid Command')
        print(' If you wish to exit the program, input "end"')
        print(' For more information on the available commands, input "help"')
        Control(action)
        


def StartDisplay(period, loc, temp, alt):

    
    #FOR TESTING
    global vals
    vals = np.zeros([period+1, 5])
    print(vals)
    loc=[0,0,0]
   # dataDifference = 0
    
    tempDiff = 0
    lastTemp = 0
    
    altDiff = 0
    lastAlt = 0
    
    step = 0
    #lastdata = 0
    #'
    ser = serial.Serial()
    print(' -------------------')
    print(' pyserial set up')
    ser.baudrate = 115200
    print(' Baudrate set to -115200-')
    ser.port = 'COM5'
    print(' Port name confirmed as -COM5-')
    ser.open()
    print(' Port opening attempted...')
    time.sleep(0.2)
    print(' Port open successful : ' + str(ser.is_open))
    print(' -------------------')
    time.sleep(0.7)

    #'
    
    

 
    
    while step <= period:
        

        tempDiff = temp - lastTemp
        altDiff = alt - lastAlt
        

         '''
        Data is read from the port
        Data is read in to the program in a binary form and therefore, must
        be converted to a string. This can be done by using a decode operator on
        the binary data type, while adding utf-8 decoding as a parameter.
        '''
        #-------------------------------------------
        currentline1 = ser.readline()
        currentline1 = currentline1.decode("utf-8")
        currentline2 = ser.readline()
        currentline2 = currentline2.decode("utf-8")
        #------------------------------------------

        clear() #this line hear prevents the timer from building up lines of messages, only seems to work in cmd
        
        Title()
        
        print('-------------------------------------------------')
        print('--------------Saura Ground Control---------------')
        print('-------------------------------------------------')

        
  
  '''
        Data is reciever from the communication port in every 2 lines.
        To ensure that data is not missed, a simple condition is used where the line 
        containing the data has a 2nd string index of 'e'.
        
        Data is preprocessed. First by splicing the first 14 characters from the
        front of the line.
        Then, a transfer array is initialised. A string split operation is performed
        that splits the data at commas and assigns it to each index in the transfer array.
        The final variables are then assigned the data from the transfer array.
        
        Alt and Temp are set to floating point variables.

'''
  
        if currentline1[1] == 'e':
            currentline1 = currentline1[15:]
            print(currentline1.split(","))
            
            transfer = [0,0,0,0,0]
            transfer = currentline1.split(",")
            print(transfer)
         
            loc[0] = transfer[0]
            loc[1] = transfer[1]
            loc[2] = transfer[2]
            alt = transfer[3]
            temp = transfer[4]
            
            alt = float(alt)
            #temp = float(temp)

            temp = temp[:-4]
            print(temp)
            temp = float(temp)
            print(temp)
            transfer[4] = temp
            
            for i in range(0,5):
                vals[step,i] = transfer[i]
            print(vals)
            '''
            print(loc[0])
            print(loc[1])   
            print(loc[2])
            print(alt)
            print(temp)
'''
            
        else:
            currentline2 = currentline2[15:]
            print(currentline2.split(","))
      
            transfer = [0,0,0,0,0]
            transfer = currentline2.split(",")
            print(transfer)
            
            loc[0] = transfer[0]
            loc[1] = transfer[1]
            loc[2] = transfer[2]
            alt = transfer[3]
            temp = transfer[4]
            
            alt = float(alt)
            #temp = float(temp)

            temp = temp[:-4]
            temp = float(temp)
            transfer[4] = temp
            
            for i in range(0,4):
                vals[step,i] = transfer[i]
            print(vals)
            
            '''
            print(loc[0])
            print(loc[1])
            print(loc[2])
            print(alt)
            print(temp)
     '''
        
        
        
        print(' ')
        print(' ')
        print(' ')
        print(' Time : ' + str(step) + ' seconds elapsed since takeoff')
        print(' ')
        print(' Co-ordinates - ' +  ''.join(str(i) for i in loc)
        )
        print(' ')

        print(' Temperature --- ' + str(round(temp)))
        if temp > lastTemp:
            print(' >>>')
        else:
            print(' <<<')
        print(' dif: ' + str(round(tempDiff, 1)))
        print('------------------------------')
        
        
        #Displaying altitude
        print('------------------------------')
        print(' Altitude --- ' + str(round(alt)))
        if alt > lastAlt:
            print(' >>>')
        else:
            print(' <<<')
        print(' dif: ' + str(round(altDiff, 1)))
        print('------------------------------')

        time.sleep(0.1)
        step += 1
   
    
        lastAlt = alt
        lastTemp = temp

    print("Finished reading, export? Y/N")
    export = input(' >>> ')
    if export == "y" or export == "Y":
        exporter(period)

    #print(' ')
    #print(period + ' has passed')

     
        
def exporter(period):
    global vals
    print ("Name the sheet to create and export to")
    sheet = input(' >>> ')
    
    workbook = xlsxwriter.Workbook(sheet + '.xlsx')
    worksheet = workbook.add_worksheet()
    #chart = workbook.add_chart({'type': 'scatter'})

    bold = workbook.add_format({'bold': 1})

    worksheet.write('B2', 'x', bold)
    worksheet.write('C2', 'y', bold)
    worksheet.write('D2', 'z', bold)
    worksheet.write('E2', 'altitude', bold)
    worksheet.write('F2', 'temp', bold)

    for i in range(0,period+1):
        for a in range(0,5):
            worksheet.write((i + 2), (a + 1), vals[i,a])
    
    '''chart.add_series({'categories': '=Sheet1!$B$3:$B$'+str(vals+2),
                      'values': '=Sheet1!$I$3:$I$'+str(vals+2),
                      'trendline': {
                            'type': 'linear',
                            'order': 1,
                        },})
    worksheet.insert_chart('A7', chart)
    '''

    workbook.close()

    print("Successfully Exported")
    Control(action)


def RecordingSetup():

    clear()
    Title()

    global period
    print(' ')
    print(' How many seconds would you like to record data for?, input "0" for instantaneous data.')
    period = input(' >>> ')

    status = period.isdigit()
 
    while status == False:
        print(' Invalid Input')
        print(' Please enter again')
        print(' ')
        print(' How many seconds would you like to record data for?, input "0" for instantaneous data.')
        period = input(' >>> ')
        status = period.isdigit()
    
    print(' ')
    print(' The system will record data for ' + period + ' seconds.')
    period = int(period)


    print(' Press y > enter to start recording.')
    print(' Press n > enter to terminate this task.  WARNING - Recording will begin instantly')
    start = input(' >>> ')
    

    
    if start == 'y' or start == 'Y':
        StartDisplay(period, loc, temp, alt)
    elif start == 'n' or start == 'N':
        time.sleep(1)
        print(' Terminating Procedure...')
        time.sleep(0.5)
        Home()
    else:
        print(' Invalid Command')
        time.sleep(1.35)
        print(' Restarting task...')
        time.sleep(1)
        clear()
        Title()
        RecordingSetup()
        
    Control(action)
    
    
def Credit():
    clear()
    Title()
    print(' ')
    print(' Developed by Callum Alexander')
    print(' Licensing: Currently unavailable')
    print(' ')
    print(' Saura is sponsored by Evolution Executive Search')
    print(' ')
    print(' Saura Team: ')
    print('      > Fraser Rennie -------- Project Manager')
    print('      > Bertie Whiteford ----- Mechanics')
    print('      > Suhit Amin ----------- Outreach & Finance ')
    print('      > Jamie Geddes --------- Mechanics & Design')
    print('      > Callum Alexander ----- Software')
    print('      > Ariana Johnson ------- Support')
    print(' ')
    Control(action)
    
def Home():
    
    clear()
    Title()
    
    print(" Welcome traveller")
    print(" This is the official Cansat Saura User Interface and Ground Control xx")
    print(" ")
    print(" This system is a command line interface")
    print(" To view the list of commands available for this system, please input 'help'.")
    print(' ')
    
    Control(action)
        
    
 
def Restart():
    clear()
    Intro()

    time.sleep(1.5)

    print(' ')
    Control(action)
    
def Help():
    clear()
    Title()
    
    print(' ')
    print(' start --- Begins recording data')
    print(' home ---- Returns to the home screen')
    print(' clear --- Clears the screen')
    print(' credits - Displays the credits')
    print(' restart - Restarts the system')
    print(' end ----- Quits the system')
    print(' help ---- Displays all the available commands')

    Control(action)
    
Intro()


print(' ')
Control(action)

