# -*- coding: utf-8 -*-
# Property of Callum Alexander
# Instagram - @cal.zander
# Twitter - callum_alxndr
"""
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
    
    



def GetAltitude(alt):    
    
    tempRnd = random.randint(1,101)
    
    lower = random.randint(1, tempRnd)
    
    upper = random.randint(tempRnd + 5, 110)

    alt = round(random.uniform(lower, upper + 1), 3)
    
    return alt
    
    

