# -*- coding: utf-8 -*-
# Property of Callum Alexander
# Instagram - @cal.zander
# Twitter - callum_alxndr
# contact - callumalexander.personal@gmail.com
#       reference @Saura - Cansat

"""
---   Quick notes for future developers   ---

* Multiline strings and comments are used synonymously


"""



"""
@author: Callum
"""

#--- Imports
import serial
import os
import sys
#import pandas as pd
clear = lambda: os.system("cls")
import xlsxwriter
import numpy as np
import time

import time
from graphics import Intro, Title
#----------------

#--- var init -------
period = 0
comVar = ''
loc = [0,0,0]
loc[1] = 0
temp = 0
alt = 0
action = ''
#------------------

def Control(action):
    action = input(' >>> $control  ')
    
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
        


def StartDisplay(period, loc, temp, alt, comVar):

    
    #FOR TESTING
    #fraser wrote this testing code here, not callum
    global vals
    vals = np.zeros([period+1, 5])
    print(vals)
    loc=[0,0,0]
    
    tempDiff = 0
    lastTemp = 0
    
    altDiff = 0
    lastAlt = 0
    
    step = 0
    
    initTime = time.time()
    currentTime = time.time()
    
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
    time.sleep(0.7)

 
    while step <= period:
        
        currentTime = time.time()
        
        tStamp = currentTime - initTime
        
        
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
            alt, temp, loc[:] = preprocess(currentline1, step, temp, alt)
        else:
            alt, temp, loc[:] = preprocess(currentline2, step, temp, alt )
        
        
        tempDiff = temp - lastTemp
        altDiff = alt - lastAlt
        

        #--- DISPLAYING DATA ------------

        print(' ')
        print(' ')
        print('Time stamp : '+ round(tStamp))
        print(' ')
        print(' Readings : ' + str(step) + ' readings elapsed since takeoff')
        print(' ')
        print(' Co-ordinates - ' +  ''.join(str(i) for i in loc)
        )
        print(' ')

        print(' Temperature --- ' + str(round(temp, 2)))
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

        
        step += 1

        # -------------------------------------------------
   
    
    ser.close()
    print('Port ' + comVar + ' closed')
    print("Finished reading, export? Y/N")
    
    export = input(' >>> $exporter  ')
    if export == "y" or export == "Y":
        exporter(period)

    #print(' ')
    #print(period + ' has passed')

     
        
def exporter(period):

    #this is fraser's cool exporter procedure
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
    period = input(' >>> $SetUp ')

    status = period.isdigit() # ignore any linter messages here troops xx
 
    while status == False:
        print(' Invalid Input')
        print(' Please enter again')
        print(' ')
        print(' How many readings would you like to record?, input "0" for instantaneous data.')
        period = input(' >>> $SetUp ')
        status = period.isdigit()
    
    print(' Please enter the name of the port that you wish to use.')
    print(' Typical port names include COM4 , COM5 ')
    comVar = input(' >>> $SetUp ')
    comVar = comVar.upper()
    print(' Using port ' + comVar)
    
    print(' ')
    print(' The system will record ' + period + ' readings.')
    period = int(period)


    print(' Press y > enter to start recording.')
    print(' Press n > enter to terminate this task.  WARNING - Recording will begin instantly')
    start = input(' >>> $SetUp ')
    

    
    if start == 'y' or start == 'Y':
        StartDisplay(period, loc, temp, alt, comVar)
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
    print(' Developed by Callum Alexander & Fraser Rennie')
    print(' Licensing: Awaiting Licensing')
    print(' ')
    print(' Saura is sponsored by Evolution Executive Search')
    print(' ')
    print(' Saura Team: ')
    print('      > Fraser Rennie -------- Project Manager')
    print('      > Bertie Whiteford ----- Mechanics')
    print('      > Suhit Amin ----------- Outreach & Finance ')
    print('      > Callum Alexander ----- Software')
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
 
def preprocess(currentline, step, temp, alt):
            currentline = currentline[15:]
            loc[1] = ''
            transfer = [0,0,0,0,0]
            transfer = currentline.split(",")

            loc[0] = transfer[0]

            '''         
            --- Note below ---
                Index out of range error kept being thrown upon this specific assignment.
                This try statement will restart the data collection and display when the error is thrown.
            '''
            while True:
                try:
                    loc[1] = transfer[1]
                    break
                except IndexError:
                    print("Error - restarting, lol just proved the heisenbug but now I've captured it haha x")
                    StartDisplay(period, loc, temp, alt, comVar)
                    
            loc[2] = transfer[2]
            alt = transfer[3]
            temp = transfer[4]
            
            alt = float(alt)
            print(alt)

            temp = temp[:-4]
            temp = float(temp)
            transfer[4] = temp
            
            for i in range(0,5):
                vals[step,i] = transfer[i]
            print(vals)

            return alt, temp, loc[:]
    

Intro()



print(' ')
Control(action)



#--meme notes for developers--
#greyhound is class
#there is a heisenbug somewhere in this code, fraser is the problem it exists xxxxx
#I don't know if my linter works :3
#oh wait...
#it does
#...just not well lol