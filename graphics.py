# -*- coding: utf-8 -*-
# Property of Callum Alexander
# Instagram - @cal.zander
# Twitter - callum_alxndr
"""
@author: Callum
"""

import os
import sys
clear = lambda: os.system("cls")

import time

def Intro():
    
    clear()
    
    delay = 0.15
    
    print("   _____                       ")
    time.sleep(delay)
    print("  / ____|                      ")
    time.sleep(delay)
    print(" | (___   __ _ _   _ _ __ __ _ ")
    time.sleep(delay)
    print("  \___ \ / _` | | | | '__/ _` |")
    time.sleep(delay)
    print("  ____) | (_| | |_| | | | (_| |")
    time.sleep(delay)
    print(" |_____/ \__,_|\__,_|_|  \__,_|")
    time.sleep(delay)
    print("                               ")
    time.sleep(1)
    print(" Welcome traveller")
    print(" This is the official Cansat Saura User Interface and Ground Control xx")
    print(" This system is a command line interface")
    print(" To view the list of commands available for this system, please input 'help'.")
    
    
'''
This subprogram below is used to display the Saura Logo

'''
    
def Title():
    print("   _____                       ")
    print("  / ____|                      ")
    print(" | (___   __ _ _   _ _ __ __ _ ")
    print("  \___ \ / _` | | | | '__/ _` |")
    print("  ____) | (_| | |_| | | | (_| |")
    print(" |_____/ \__,_|\__,_|_|  \__,_|")
    print("                               ")
    

    
    
#--meme notes for developers--
#time.sleep is the bane of frasers existance 

#any linter errors or messages that you see concerning the intro sub are irrelevent, just ignore them