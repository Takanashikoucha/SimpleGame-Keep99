# -*- coding: UTF-8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2019-07-15 22:43:47
import threading
import time
import os

import requests

homepage = "http://127.0.0.1:5000"
help = '''可用指令:
            帮助: help
            登录: login/<用户名>
            开始: start
            结束: end
            看手牌: hand
            丢出牌: put/<牌的位置>
            与目标换手牌: all/<目标id>
            分数操作: + - =之后跟上/<对应数字>
            转向: turn
            轮到: to/<目标id>
            抽卡: get/<c或者目标id(c则为从卡组获得)>
            弃牌: clean
            标记玩家为死亡: down/<目标id>
            复活玩家" up/<目标id>
'''
MsgCache = ""


def StartUp():
    global s
    global homepage
    global help
    print(help)
    try:
        s = requests.Session()
        r = s.get(homepage)
        print(r.text)
    except:
        print("连接服务器失败,退出")
        time.sleep(1)
        os._exit(0)


def GetMsg():
    global s
    global homepage
    global MsgCache
    while True:
        try:
            r = s.get(homepage + "/msg")
            if r.text == "对局已结束请关闭窗口":
                os._exit(0)
            elif r.text != MsgCache:
                print(r.text + "\n>>>  ", end='')
            MsgCache = r.text
            time.sleep(0.3)
        except:
            print("连接服务器失败,退出")
            os._exit(0)


def Do(cmdpath):
    global s
    global homepage
    global help
    if cmdpath == "":
        cmdpath = "hand"
        try:
            url = homepage + "/" + cmdpath
            r = s.get(url)
            print(">>>  " + r.text)
        except:
            print(">>>  发生错误")
    elif cmdpath == "help":
        print(help)
    else:
        try:
            url = homepage + "/" + cmdpath
            r = s.get(url)
            print(">>>  " + r.text)
        except:
            print(">>>  发生错误")


if __name__ == "__main__":
    StartUp()
    msg = threading.Thread(target=GetMsg)
    msg.setDaemon(True)
    msg.start()
    while True:
        cmd = input(">>>  ")
        Do(cmd)
