# -*- coding: UTF-8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2019-07-16 16:25:19
import threading
import time
import tkinter

import requests

homepage = "http://47.107.104.4:5000"
MsgCache = ""
msg = ""


def Insertlog(log):
    Log.insert(tkinter.END, log + "\n\n")
    Log.update()
    Log.see(tkinter.END)


def StartUp():
    global s
    global homepage
    try:
        s = requests.Session()
        r = s.get(homepage)
        Insertlog(r.text)
    except:
        Insertlog("连接服务器失败,退出")


def GetMsg():
    global s
    global homepage
    global MsgCache
    while True:
        try:
            r = s.get(homepage + "/msg")
            if r.text == "对局已结束请关闭窗口":
                time.sleep(2)
                StartUp()
            elif r.text != MsgCache:
                Insertlog(r.text)
            MsgCache = r.text
            time.sleep(0.1)
        except:
            Insertlog("连接消息服务器失败")


def GetHand():
    global s
    global homepage
    global msg
    while True:
        r = s.get(homepage + "/hand")
        msg = r.text
        Msg.config(text=msg)
        Msg.update()
        time.sleep(0.1)


def Login():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/login/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Start():
    global s
    global homepage
    global MsgCache
    try:
        r = s.get(homepage + "/start")
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def End():
    global s
    global homepage
    global MsgCache
    try:
        r = s.get(homepage + "/end")
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Put():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/put/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Get():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    if v[0] != "-":
        v = "c"
    else:
        v = v[1:]
    try:
        r = s.get(homepage + "/get/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def All():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/all/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Turn():
    global s
    global homepage
    global MsgCache
    try:
        r = s.get(homepage + "/turn")
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def To():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/to/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Eq():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/=/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Clean():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/clean/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Down():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/down/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


def Up():
    global s
    global homepage
    global MsgCache
    v = Enter.get()
    try:
        r = s.get(homepage + "/up/" + v)
        Insertlog(r.text)
    except:
        Insertlog("怕是有病病")


#界面与函数绑定

##根窗口
root = tkinter.Tk()
root.geometry("330x440+300+300")
root.resizable(False, False)
root.title("Keep99")

##部件
Log = tkinter.Text(root, width=45, height=10, font=("", 9, ""))
Msg = tkinter.Label(root, width=45, height=6, text=msg, justify="left")
Enter = tkinter.Entry(root, width=45)
B_Login = tkinter.Button(root, width=10, text="登录", command=Login)
B_Start = tkinter.Button(root, width=10, text="开始", command=Start)
B_End = tkinter.Button(root, width=10, text="结束", command=End)
B_Put = tkinter.Button(root, width=10, text="丢出", command=Put)
B_get = tkinter.Button(root, width=10, text="抽卡", command=Get)
B_All = tkinter.Button(root, width=10, text="交换", command=All)
B_Turn = tkinter.Button(root, width=10, text="转向", command=Turn)
B_To = tkinter.Button(root, width=10, text="轮到", command=To)
B_Eq = tkinter.Button(root, width=10, text="变为", command=Eq)
B_Clean = tkinter.Button(root, width=10, text="弃牌", command=Clean)
B_Down = tkinter.Button(root, width=10, text="死亡", command=Down)
B_Up = tkinter.Button(root, width=10, text="复活", command=Up)

##布局
Log.grid(row=0, column=0, padx=5, pady=5, columnspan=6)
Msg.grid(row=1, column=0, padx=5, pady=5, columnspan=6)
Enter.grid(row=2, column=0, padx=5, pady=5, columnspan=6)
B_Login.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
B_Start.grid(row=3, column=2, padx=5, pady=5, columnspan=2)
B_End.grid(row=3, column=4, padx=5, pady=5, columnspan=2)
B_Put.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
B_get.grid(row=4, column=2, padx=5, pady=5, columnspan=2)
B_All.grid(row=4, column=4, padx=5, pady=5, columnspan=2)
B_Turn.grid(row=5, column=0, padx=5, pady=5, columnspan=2)
B_To.grid(row=5, column=2, padx=5, pady=5, columnspan=2)
B_Eq.grid(row=5, column=4, padx=5, pady=5, columnspan=2)
B_Clean.grid(row=6, column=0, padx=5, pady=5, columnspan=2)
B_Down.grid(row=6, column=2, padx=5, pady=5, columnspan=2)
B_Up.grid(row=6, column=4, padx=5, pady=5, columnspan=2)

#主循环
if __name__ == "__main__":
    StartUp()
    msg = threading.Thread(target=GetMsg)
    msg.setDaemon(True)
    msg.start()
    hand = threading.Thread(target=GetHand)
    hand.setDaemon(True)
    hand.start()
    root.mainloop()
