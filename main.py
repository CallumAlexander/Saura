# -*- coding: utf-8 -*-
# Property of Callum Alexander
# Instagram - @cal.zander
# Twitter - callum_alxndr
"""
@author: Callum
"""
import serial
import os
import sys
#import pandas as pd
clear = lambda: os.system("cls")

import time
import random
from getData_Test import GetCoordinates, GetTemperature, GetAltitude
from graphics import Intro, Title



lower = 1
upper = lower + 5
data = 0

period = 0

loc = [0,0,0]
temp = 0
alt = 0
action = ''



def Control(action):
    action = input(' >>> ')
    
    if action == 'start':
        time.sleep(0.75)
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
        time.sleep(1)
        Credit()
    #elif action == 'status':
        #time.sleep(1)
        #print(status)
    elif action =='home':
        time.sleep(0.5)
        Home()
    elif action == 'restart':
        time.sleep(1)
        print(' RESTARTING...')
        time.sleep(2)
        Restart()
    elif action == 'help':
        time.sleep(1)
        Help()
    else:
        clear()
        Title()
        print(' Invalid Command')
        print(' If you wish to exit the program, input "end"')
        print(' For more information on the available commands, input "help"')
        Control(action)
        
    


def GenerateData(lower, upper, data):
    
    tempRnd = random.randint(1,101)
    
    lower = random.randint(1, tempRnd)
    
    upper = random.randint(tempRnd + 5, 110)

    data = round(random.uniform(lower, upper + 1), 3)
    
    return data


def StartDisplay(period, data, lower, upper, loc, temp, alt):
    
    dataDifference = 0
    
    tempDiff = 0
    lastTemp = 0
    
    altDiff = 0
    lastAlt = 0
    
    step = 0
    lastdata = 0
    while step <= period:
        
        clear() # this line hear prevents the timer from building up lines of messages, only seems to work in cmd
        
        Title()
        
        print('-------------------------------------------------')
        print('--------------Saura Ground Control---------------')
        print('-------------------------------------------------')

        
        data = GenerateData(lower, upper, data)
        loc = GetCoordinates(loc)
        temp = GetTemperature(temp)
        alt = GetAltitude(alt)
        

        dataDifference = data - lastdata
        tempDiff = temp - lastTemp
        altDiff = alt - lastAlt
        
        
        print(' Time : ' + str(step) + ' seconds elapsed since takeoff')
        print(' ')
        print(' Co-ordinates - ' +  ''.join(str(i) for i in loc))
        print(' ')
        
        print('------------------------------')
        print(' Data --- ' + str(data))
        if data > lastdata:
            print(' >>>')
        else:
            print(' <<<')
        print(' dif: ' + str(round(dataDifference, 1)))
        print('------------------------------')
        
        print('------------------------------')
        print(' Temperature --- ' + str(round(temp)))
        if temp > lastTemp:
            print(' >>>')
        else:
            print(' <<<')
        print(' dif: ' + str(round(tempDiff, 1)))
        print('------------------------------')
        
        print('------------------------------')
        print(' Altitude --- ' + str(round(alt)))
        if alt > lastAlt:
            print(' >>>')
        else:
            print(' <<<')
        print(' dif: ' + str(round(altDiff, 1)))
        print('------------------------------')


   
        lower += 3
        upper += 3
   
        time.sleep(1)
        step += 1
   
        lastdata = data


    #print(' ')
    #print(period + ' has passed')
     
        
        
        
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
    
    time.sleep(2)
    print(' ')
    print(' The system will record data for ' + period + ' seconds.')
    period = int(period)

    time.sleep(3)
    
    print(' Press y > enter to start recording.')
    print(' Press n > enter to terminate this task.  WARNING - Recording will begin instantly')
    start = input(' >>> ')
    
    time.sleep(0.5)
    
    if start == 'y' or start == 'Y':
        StartDisplay(period, data,lower,upper, loc, temp, alt)
    elif start == 'n' or start == 'N':
        time.sleep(1.1)
        print(' Terminating Procedure...')
        time.sleep(1.9)
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

ser = serial.Serial()
print(' -------------------')
print(' pyserial set up')
time.sleep(0.4)
ser.baudrate = 115200
print(' Baudrate set to -115200-')
time.sleep(0.4)
ser.port = 'COM4'
print(' Port name confirmed as -COM4-')
time.sleep(0.4)
ser.open()
print(' Port opening attempted...')
time.sleep(2)
print(' Port open successful : ' + str(ser.is_open))
print(' -------------------')
time.sleep(0.7)
print(" This system is a command line interface")
print(" To view the list of commands available for this system, please input 'help'.")
time.sleep(3)

print(' ')
Control(action)

