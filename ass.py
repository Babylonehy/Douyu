#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:42:59 2018

@author: lixiang
"""
import codecs
import numpy
import random
import os

def danmutoass(dirt):
    dirthead='/Users/lixiang/iCollections/Programe/Github/douyudanmu/弹幕/'
    dirt=dirthead+dirt  
    delaytime=5
    global timestart
    global timeend
    global txt
    timestart=[]
    timeend=[]
    txt=[]
    with open(dirt, 'r') as f:  
        data = f.readlines()  #txt中所有字符串读入data  
    for line in data:  
        second = line.split('|')[0]        #将单个数据分隔开存好
        txt.append(line.split('|')[-1])
        timestart.append(timeformate(second))
        secondend=float(second)+delaytime
        timeend.append(timeformate(secondend))
        #print(timestart[-1]+' '+timeend[-1]+' '+txt[-1])
        
def addzero(time):
    
    if (time<10.0):
        strtime='0'+str(time)
        return strtime
    
def timeformate(second):
    second =float(second)
    h=int(second/3600)
    m=int((second-h*3600)/60)
    s=second-h*3600-m*60
    s = "%.2f" % s
    s=float(s)
    #s=addzero(s)
    #h=addzero(h)
    m=addzero(m)
    if (s<10.0):
        s='0'+str(s)
    strtime=str(h)+':'+str(m)+':'+str(s)
    return strtime

#暂时写入指定头部吧
def converttoass(dirtass):
     isExists=os.path.exists(dirtass)
     #print(isExists)
     if (isExists==True):
         os.remove(dirtass)
     output = open(dirtass, 'a+')
     fp = open('/Users/lixiang/iCollections/Programe/Github/douyudanmu/[Script Info].txt','r')  
     down=1000
     up=1200
     for line in fp:  
        output.write(line)
     output.write('\n')
     for i in range(0,len(txt)):
          x1=str(random.randint(down,up))
          y1=str(random.randint(20,300))
          x2=str(-10)
          y2=y1
          Dialogue='Dialogue: 0,'+timestart[i]+','+timeend[i]+',R2L,,20,20,2,,{\move('+x1+','+y1+','+x2+','+y2+')}'+txt[i]
          output.write(Dialogue)
    
    #追加弹幕内容
'''
    [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        Dialogue: 0,0:00:05.23,0:00:13.23,R2L,,20,20,2,,{\move(585,25,-25,25)}小新
        Dialogue: 0,0:00:07.33,0:00:15.33,R2L,,20,20,2,,{\move(610,25,-50,25)}多少集？
        Dialogue: 0,0:00:10.43,0:00:18.43,R2L,,20,20,2,,{\move(585,25,-25,25)}小葵
        Dialogue: 0,0:00:17.69,0:00:25.69,R2L,,20,20,2,,{\move(672.5,25,-112.5,25)}又是熟悉的配音啊！
        Dialogue: 0,0:00:23.69,0:00:31.69,R2L,,20,20,2,,{\move(647.5,25,-87.5,25)}还有小白，果然
        Dialogue: 0,0:00:23.75,0:00:31.75,R2L,,20,20,2,,{\move(597.5,50,-37.5,50)}第二季
        Dialogue: 0,0:00:27.13,0:00:35.13,R2L,,20,20,2,,{\move(660,25,-100,25)}第一次看时看哭啦
        
        \move(<x1>,<y1>,<x2>,<y2>[,<t1>,<t2>])
        提供字幕的移动效果。<x1>,<y1> 是开始点坐标，<x2>,<y2> 是结束点坐标。
        <t1> 和 <t2> 是相对于字幕显示时间的开始运动与结束运动的毫秒时间。

        在 <t1> 之前，字幕定位在 <x1>,<y1>。
        在 <t1> 与 <t2> 之间，字幕从 <x1>,<y1> 均速移动到 <x2>,<y2>。
        在 <t2> 之后，字幕定位在 <x2>,<y2>。
        当 <t1> 和 <t2> 没写或者都是 0 时，则在字幕的整段时间内均速移动。
        当一行中有多个 \pos 和 \move 时，以第一个为准。
        当 \move 和 Effect 效果同时存在时，结果比较迷。
        当一行中含有 \move 时会忽略字幕重叠冲突的检测。
    
'''
if __name__ == '__main__':
    room_id = input('请输入需要转码的房间号:')
    danmutoass(str(room_id)+'danmuass.txt')
    converttoass('/Users/lixiang/iCollections/Programe/Github/douyudanmu/弹幕/'+str(room_id)+'danmuass.ass')
    print('转换完成!')