# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 16:49:01 2019

@author: Callum
"""

"""
x
y
z
temp
alt
"""

import random

#coordinates will be stored in a 1x3 array (list)
loc = [0,0,0]
temp = 0
alt = 0


def GetCoordinates(loc):
    
    loc[0] = random.randint(1,51)
    loc[1] = random.randint(1,51)
    loc[2] = random.randint(1,51)
    
    return loc


def GetTemperature(temp):
    
    temp = random.uniform(5,16)
    return temp
    
    



def GetAltitude():    
    pass

