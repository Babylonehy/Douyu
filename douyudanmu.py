#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 15:08:52 2017
斗鱼弹幕抓取
@author: lixiang
"""

import requests
import json

import multiprocessing
import socket
import time
import re

from threading import Thread

def room_info(room_id):
    url='http://open.douyucdn.cn/api/RoomApi/room/'+str(room_id)
    headers={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10=_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
            }
    print('------------房间信息获取中----------',)
    r = requests.get(url,headers=headers)
    html=r.content.decode('utf-8')
    roominfo=json.loads(html)
    if(roominfo['error']!=0):
        print('房间不存在!')
        return 1
    room_status=roominfo['data']['room_status']
    if(room_status!='1'):
        room_id=roominfo['data']['room_id']
        cate_name=roominfo['data']['cate_name']
        room_name=roominfo['data']['room_name']
        owner_name=roominfo['data']['owner_name']
        online=roominfo['data']['online']
        fans_num=roominfo['data']['fans_num']
        print('主播 '+str(owner_name)+' 未开播!',)
        print('房间名:'+str(room_name),
              '主播ID:'+str(owner_name),
              '游戏分类:'+str(cate_name),
              '在线人数:'+str(online),
              '关注人数:'+str(fans_num))
        return 1
    else:
        room_id=roominfo['data']['room_id']
        cate_name=roominfo['data']['cate_name']
        room_name=roominfo['data']['room_name']
        owner_name=roominfo['data']['owner_name']
        online=roominfo['data']['online']
        fans_num=roominfo['data']['fans_num']
        print('房间名:'+str(room_name),
              '主播ID:'+str(owner_name),
              '游戏分类:'+str(cate_name),
              '在线人数:'+str(online),
              '关注人数:'+str(fans_num))
        


'''
连接弹幕服务器

    弹幕服务器地址  端口
    danmu.douyutv.com:8061
    anmu.douyutv.com:8062
    danmu.douyutv.com:12601
    danmu.douyutv.com:12602
    第三方接入弹幕服务器列表
    IP 地址：openbarrage.douyutv.com
    端口：8601

'''
client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host='openbarrage.douyutv.com' 
Port=8601
client.connect((Host,Port))

def sendmsg(msgstr):
    msg=msgstr.encode('utf-8')
    data_length= len(msg)+8
    code=689
    msgHead = int.to_bytes(data_length, 4, 'little') + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)  #发送协议头
    client.send(msg)      #发送消息请求

def connectdanmuserver(room_id):
    if(room_info(room_id)==1):
         return 0
    print('------------弹幕服务器连接中----------',)
    msg = 'type@=loginreq/roomid@={}/\x00'.format(room_id)
    sendmsg(msg)
    join_room_msg = 'type@=joingroup/rid@={}/gid@=-9999/\x00'.format(room_id) #加入房间分组消息  
    sendmsg(join_room_msg)  
    pattern = re.compile(b'type@=chatmsg/.+?/nn@=(.+?)/txt@=(.+?)/.+?/level@=(.+?)/')
    while True:  
        data = client.recv(1024)  #这个data就是服务器向客户端发送的消息
        for nn, txt, level in pattern.findall(data):
            try:
                print("[lv.{}][{}]: {}".format(level.decode(), nn.decode(), txt.decode().strip()))
            except UnicodeDecodeError as e:
                # 斗鱼有些表情会引发unicode编码错误
                print(e)
    
def keeplive():
    while True:
        #msg='type@=keeplive/tick@={}/\x00'.format(int(time.time()))
        msg = 'type@=mrkl/\x00'
        sendmsg(msg)
        time.sleep(10)
   
if __name__ == '__main__':
    room_id = input('请输入房间号:')
    #room_id=687423
    #connectdanmuserver(room_id)
    t1 = Thread(target=connectdanmuserver,args=(room_id,))
    t2 = Thread(target=keeplive)
    t1.start()
    t2.start()   
    

