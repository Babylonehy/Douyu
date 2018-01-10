#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 00:11:14 2018
显示大ASCII艺术字体
@author: lixiang
"""

from pyfiglet import Figlet
from termcolor import colored

def fontconvert(strfont):
    font=strfont
    f = Figlet(font='stop')
    print (colored(f.renderText(font),'green',attrs=['bold']))

fontconvert('Douyu')
fontconvert('Danmu')
fontconvert('V 2.0')
