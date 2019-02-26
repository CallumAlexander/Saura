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
    ser.port = 'COM4'
    print(' Port name confirmed as -COM4-')
    ser.open()
    print(' Port opening attempted...')
    time.sleep(0.2)
    print(' Port open successful : ' + str(ser.is_open))
    print(' -------------------')
    time.sleep(0.7)

    #'
    
    

 
    
    while step <= period:
        
        clear() # this line hear prevents the timer from building up lines of messages, only seems to work in cmd
        
        Title()
        
        print('-------------------------------------------------')
        print('--------------Saura Ground Control---------------')
        print('-------------------------------------------------')



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
            #print(currentline1.split(","))
            
            transfer = [0,0,0,0,0]
            transfer = currentline1.split(",")
            print(transfer)
         
            loc[0] = transfer[0]
            loc[1] = transfer[1]
            loc[2] = transfer[2]
            alt = transfer[3]
            temp = transfer[4]
            
            alt = float(alt)
            temp = float(temp)
  

            
        else:
            currentline2 = currentline2[15:]
            print(currentline2.split(","))
      
            transfer = [0,0,0,0]
            transfer = currentline2.split(",")
            print(transfer)
            
            loc[0] = transfer[0]
            loc[1] = transfer[1]
            loc[2] = transfer[2]
            alt = transfer[3]
            temp = transfer[4]
            
            alt = float(alt)
            temp = float(temp)


        #displaying coordinates
        print(' ')
        print(' ')
        print(' ')
        print(' Steps : ' + str(step) + ' out of ' + str(period))
        print(' ')
        print(' Co-ordinates - ' +  ''.join(str(i) for i in loc)
        )
        print(' ')
        print('------------------------------')
        
        #displaying temperature
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


   

   
        time.sleep(0.5)
        step += 1
   
        lastAlt = alt
        lastTemp = temp

     
        
        
        
def RecordingSetup():

    clear()
    Title()

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
    
    time.sleep(0.3)
    print(' ')
    print(' The system will record data for ' + period + ' seconds.')
    period = int(period)

    time.sleep(0.3)
    
    print(' Press y > enter to start recording.')
    print(' Press n > enter to terminate this task.  WARNING - Recording will begin instantly')
    start = input(' >>> ')
    
    time.sleep(0.3)
    
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

