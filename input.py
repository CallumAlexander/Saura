# -*- coding: utf-8 -*-
# Property of Callum Alexander
# Instagram - @cal.zander
# Twitter - callum_alxndr
"""
@author: Callum
"""

import serial


ser = serial.Serial()
ser.baudrate = 115200

ser.port = 'COM4'

ser.open()
ser.is_open



step = 0

while True:

    step+= 1
    line = ser.readline()
    print(str(step))
    print(line) 

    
    
#print('')
#print('')
    
#print(str(step))


ser.close()




'''
with serial.Serial('COM4', 19200) as s:
	x = serial.read()          # read one byte
	s = serial.read(10)        # read up to ten bytes (timeout)
	line = serial.readline()   # read a '\n' terminated line

'''
