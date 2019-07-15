# -*- coding: UTF-8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2019-07-14 21:08:25

#游戏--------------------------------------------
import random
import time
import threading

Status = 0
Cards = []
Players = []
Count = 0
Num = 0
Turn = "▼"
MsgCache = "暂无公共消息"


class Player:
    def __init__(self, username, id):
        self.username = username
        self.id = id
        self.token = "="
        self.side = "红"
        self.status = "存活"
        self.inhand = []

    def Down(self):
        self.status = "死亡"

    def Up(self):
        self.status = "存活"


def GenCards():
    global Cards
    pool1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 12, 13]
    pool2 = [14, 14]
    pool = pool1 + pool1 + pool1 + pool1 + pool2
    fullpool = pool + pool + pool + pool
    random.shuffle(fullpool)
    for i in fullpool:
        Cards.append(i)


def GenPlayers():
    global Players
    PlayerNum = len(Players)
    sideNum = int(PlayerNum / 2)
    for i in range(PlayerNum):
        player = Players[i]
        player.side = "红"
    for i in range(sideNum):
        player = Players[i]
        player.side = "蓝"
    random.shuffle(Players)


def GiveCard(playerid):
    global Cards
    global Players
    global Count
    player = Players[int(playerid)]
    player.inhand.append(Cards[Count])
    Count = Count + 1


def StartGame():
    global Status
    global Turn
    global Players
    global MsgCache
    GenCards()
    GenPlayers()
    for i in range(5):
        for i in Players:
            GiveCard(i.id)
    Status = 1
    MsgCache = ""
    MsgCache = MsgCache + (Turn + "\n")
    Players[0].token = "*"
    for i in Players:
        MsgCache = MsgCache + (">>>  " + i.token + "  " + i.username + "  " +
                               i.id + "\n")
    MsgCache = MsgCache + ">>>  游戏开始"


def EndGame():
    global Status
    global Cards
    global Players
    global Count
    global Num
    global Turn
    global MsgCache
    Status = 0
    Cards = []
    Players = []
    Count = 0
    Num = 0
    Turn = "▼"
    MsgCache = "对局已结束请关闭窗口"


#服务--------------------------------------------
from flask import Flask, session, escape
app = Flask(__name__)


@app.route("/")
def HomePage():
    if "username" in session:
        return "欢迎连接服务器,已登录为:  %s" % escape(session["username"])
    return "欢迎连接服务器,您尚未登录"


@app.route("/msg")
def Msg():
    global MsgCache
    return MsgCache


@app.errorhandler(404)
def error404(e):
    return "指令错误"


@app.errorhandler(500)
def error500(e):
    return "服务器错误"


@app.route("/login/<username>")
def Login(username):
    global Players
    global MsgCache
    for i in Players:
        if username in i.username:
            return "有重名用户"
    if "username" in session:
        return "重复登录了嗷"
    if "id" in session:
        return "重复登录了嗷"
    session["username"] = username
    id = len(Players)
    session["id"] = str(id)
    Players.append(Player(username, str(id)))
    MsgCache = "新玩家 %s 登录" % username
    return "已登录为:  %s,ID: %s" % (username, str(id))


@app.route("/start")
def Start():
    global Status
    global MsgCache
    if Status == 0:
        StartGame()
        return "--------------------------------"
    else:
        return "已经有对局正在进行中"


@app.route("/end")
def End():
    global Status
    global MsgCache
    if Status == 1:
        EndGame()
        time.sleep(0.2)
        return "--------------------------------"
    else:
        return "没有对局正在进行中"


@app.route("/hand")
def Hand():
    global Players
    id = session["id"]
    for i in Players:
        if i.id == id:
            player = i
    side = player.side
    status = player.status
    hand = player.inhand
    return "你的阵营是:  " + str(side) + "  存活与否:  " + str(
        status) + "\n>>>  手牌:  " + str(hand)


@app.route("/put/<cardid>")
def Put(cardid):
    global Players
    global MsgCache
    id = session["id"]
    for i in Players:
        if i.id == id:
            player = i
    hand = player.inhand
    MsgCache = "玩家  " + player.username + "  丢出一张  " + str(
        hand[int(cardid) - 1])
    del hand[int(cardid) - 1]
    return "--------------------------------"


@app.route("/all/<playerid>")
def All(playerid):
    global Players
    global MsgCache
    id = session["id"]
    for i in Players:
        if i.id == id:
            player1 = i
    for i in Players:
        if i.id == playerid:
            player2 = i
    player1.inhand, player2.inhand = player2.inhand, player1.inhand
    MsgCache = "已交换玩家手牌:" + player1.username + "  " + player2.username
    return "--------------------------------"


@app.route("/+/<num>")
def Add(num):
    global Num
    global MsgCache
    Num = Num + int(num)
    MsgCache = "数字已变为:  " + str(Num)
    return "--------------------------------"


@app.route("/-/<num>")
def Less(num):
    global Num
    global MsgCache
    Num = Num - int(num)
    MsgCache = "数字已变为:  " + str(Num)
    return "--------------------------------"


@app.route("/=/<num>")
def Nto(num):
    global Num
    global MsgCache
    Num = int(num)
    MsgCache = "数字已变为:  " + str(Num)
    return "--------------------------------"


@app.route("/turn")
def CTurn():
    global Turn
    global Players
    global MsgCache
    if Turn == "▼":
        Turn = "▲"
    elif Turn == "▲":
        Turn = "▼"
    MsgCache = ""
    MsgCache = MsgCache + (Turn + "\n")
    for i in Players:
        MsgCache = MsgCache + (">>>  " + i.token + "  " + i.username + "  " +
                               i.id + "\n")
    MsgCache = MsgCache + ">>>  顺序转变"
    return "--------------------------------"


@app.route("/to/<playerid>")
def To(playerid):
    global Turn
    global Players
    global MsgCache
    print(Turn)
    for i in Players:
        if i.id == playerid:
            player = i
    for i in Players:
        i.token = "="
    player.token = "*"
    MsgCache = ""
    MsgCache = MsgCache + (Turn + "\n")
    for i in Players:
        MsgCache = MsgCache + (">>>  " + i.token + "  " + i.username + "  " +
                               i.id + "\n")
    MsgCache = MsgCache + ">>>  轮到*玩家进行"
    return "--------------------------------"


@app.route("/get/<target>")
def Get(target):
    global Players
    global MsgCache
    if target == "c":
        id = session["id"]
        for i in Players:
            if i.id == id:
                GiveCard(id)
                MsgCache = "玩家  " + i.username + "  获得一张牌"
    else:
        id = session["id"]
        for i in Players:
            if i.id == id:
                player1 = i
        for i in Players:
            if i.id == target:
                player2 = i
        card = player2.inhand[0]
        del player2.inhand[0]
        player1.inhand.append(card)
        MsgCache = "玩家 " + player1.username + " 获得一张牌"
    return "从牌组得到一张牌,请确认它是什么"


@app.route("/clean")
def Clean():
    global Players
    global MsgCache
    id = session["id"]
    for i in Players:
        if i.id == id:
            player = i
    player.inhand = []
    MsgCache = "玩家  " + player.username + "  丢弃了所有手牌"
    return "牌已全部丢弃"


@app.route("/down/<id>")
def Down(id):
    global Players
    global MsgCache
    for i in Players:
        if i.id == id:
            player = i
    player.Down()
    MsgCache = "玩家  " + player.username + "  已死亡"
    return "--------------------------------"


@app.route("/up/<id>")
def Up(id):
    global Players
    global MsgCache
    for i in Players:
        if i.id == id:
            player = i
    player.Up()
    MsgCache = "玩家  " + player.username + "  已复活"
    return "--------------------------------"


app.secret_key = 'WDNMDzTMDjiubaigeiA'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
