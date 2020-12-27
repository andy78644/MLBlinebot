from django.shortcuts import render
import pyimgur
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files import File
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
#from linebot.models import MessageEvent, TextSendMessage
from linebot.models import *
import statsapi
from mlblinebot.fsm import TocMachine
from mlblinebot.utils import send_text_message, send_image_url
import time
from PIL import Image
import PIL

import mlblinebot.message_template

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

TEAM_MAP = {
    "AZ": "Arizona Diamondbacks",
    "ATL": "Atlanta Braves",
    "BAL": "Baltimore Orioles",
    "BOS": "Boston Red Sox",
    "CHC": "Chicago Cubs",
    "CWS": "Chicago White Sox",
    "CIN": "Cincinnati Reds",
    "COL": "Colorado Rockies",
    "CLE": "Cleveland Indians",
    "DET": "Detroit Tigers",
    "HOU": "Houston Astros",
    "KC": "Kansas City Royals",
    "LAA": "Los Angeles Angels",
    "LAD": "Los Angeles Dodgers",
    "MIA": "Miami Marlins",
    "MIL": "Milwaukee Brewers",
    "MIN": "Minnesota Twins",
    "NYM": "New York Mets",
    "NYY": "New York Yankees",
    "OAK": "Oakland Athletics",
    "PHI": "Philadelphia Phillies",
    "PIT": "Pittsburgh Pirates",
    "SD": "San Diego Padres",
    "SF": "San Francisco Giants",
    "SEA": "Seattle Mariners",
    "STL": "St. Louis Cardinals",
    "TB": "Tampa Bay Rays",
    "TEX": "Texas Rangers",
    "TOR": "Toronto Blue Jays",
    "WSH": "Washington Nationals"
}

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        #print(type(request))
        message = []
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                
                print(event)
                '''
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                    #TextSendMessage(text=event.message)
                )
                '''
                team_name = event.message.text
                handle_message(event, team_name)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
# Create your views here.
def handle_message(event, get_name):
    print(get_name)
    try:
        team_name = TEAM_MAP[get_name]
    except:
        error_message = TextSendMessage(text = f"{get_name} is not found")
        line_bot_api.reply_message(
            event.reply_token,
            error_message,
        )
        return
    games = statsapi.schedule(date = "09/15/2020")
    #print(games)
    for game in games:
        message = TextSendMessage(text = game['summary'])
        line_bot_api.reply_message(
            event.reply_token,
            message,
        )
    return

machine = {}
'''
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"
'''
@csrf_exempt
#@app.route("/webhook", methods=["POST"])
def webhook_handler(request):
    if request.method == 'POST':
        #print(type(request))
        message = []
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        #signature = request.headers["X-Line-Signature"]
        # get request body as text
        #body = request.get_data(as_text=True)
        #app.logger.info(f"Request body: {body}")

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        '''
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                
                print(event)
                
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                    #TextSendMessage(text=event.message)
                )
                
                #team_name = event.message.text
                #handle_message(event, team_name)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
        # if event is MessageEvent and message is TextMessage, then echo text
        '''
        print('abc')
        for event in events:
            if event.source.user_id not in machine:
                print(event.source.user_id)
                machine[event.source.user_id] = TocMachine(
                    #states=["user", "testing", "searchplayer", "watchGame", "todayGame", "yesterGame", "showplayer", "lobby", "gameBoxscore", "showBoxscore", "searchteam", "showteam", "showstanding", "statleader", "showschedule", "showmeme", "shownews", "searchgame", "showsearchgame"],
                    states=["user", "lobby", "GameChoose","dateGame", "datestats","todayGame", "leaguechoose", "national", "amarican", "show_fsm_pic"],
                    transitions=[
                        {
                            "trigger": "advance",
                            "source": "user",
                            "dest": "lobby",
                            "conditions": "is_going_to_lobby",
                        },
                        {
                            "trigger": "advance",
                            "source": "lobby",
                            "dest": "show_fsm_pic",
                            "conditions": "is_going_to_show_fsm_pic",
                        },
                        {
                            "trigger": "advance",
                            "source": "lobby",
                            "dest": "GameChoose",
                            "conditions": "is_going_to_GameChoose",
                        },
                        {
                            "trigger": "advance",
                            "source": "GameChoose",
                            "dest": "lobby",
                            "conditions": "is_going_to_menu",
                        },
                        {
                            "trigger": "advance",
                            "source": "GameChoose",
                            "dest": "todayGame",
                            "conditions": "is_going_to_todayGame",
                        },
                        {
                            "trigger": "advance",
                            "source": "GameChoose",
                            "dest": "dateGame",
                            "conditions": "is_going_to_dateGame",
                        },
                        {
                            "trigger": "advance",
                            "source": "dateGame",
                            "dest": "lobby",
                            "conditions": "is_going_to_menu",
                        },
                        {
                            "trigger": "advance",
                            "source": "dateGame",
                            "dest": "datestats",
                            "conditions": "is_going_to_datestats",
                        },
                        {
                            "trigger": "advance",
                            "source": "datestats",
                            "dest": "lobby",
                            "conditions": "is_going_to_menu",
                        },
                        {
                            "trigger": "advance",
                            "source": "lobby",
                            "dest": "leaguechoose",
                            "conditions": "is_going_to_leaguechoose",
                        },
                        {
                            "trigger": "advance",
                            "source": "leaguechoose",
                            "dest": "lobby",
                            "conditions": "is_going_to_menu",
                        },
                        {
                            "trigger": "advance",
                            "source": "leaguechoose",
                            "dest": "national",
                            "conditions": "is_going_to_national",
                        },
                        {
                            "trigger": "advance",
                            "source": "national",
                            "dest": "lobby",
                            "conditions": "is_going_to_menu",
                        },
                        {
                            "trigger": "advance",
                            "source": "leaguechoose",
                            "dest": "amarican",
                            "conditions": "is_going_to_amarican",
                        },
                        {
                            "trigger": "advance",
                            "source": "amarican",
                            "dest": "lobby",
                            "conditions": "is_going_to_menu",
                        },
                        {
                            "trigger": "advance",
                            "source": ["todayGame"],
                            "dest": "lobby",
                            "conditions": "is_going_to_menu",
                        },
                        {"trigger": "go_back", "source": ["datestats", "todayGame", "leaguechoose", "show_fsm_pic", "lobby", "dateGame","GameChoose"], "dest": "user"},
                    ],
                    initial="user",
                    auto_transitions=False,
                    show_conditions=True,
                    )
            #print("hello")
            #print(isValidDate("9/30/2020"))
            #print("hello")
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue
            if not isinstance(event.message.text, str):
                continue
            if machine[event.source.user_id].state == 'dateGame':
                res = isValidDate(event.message.text)
                if res == False:
                    send_text_message(event.reply_token, "請輸入正確日期格式(mm/dd/yyyy)")
                    print("請輸入正確的日期格式(mm/dd/yyyy)")
                    continue
            # print(f"\nFSM STATE: {machine.state}")
            # print(f"REQUEST BODY: \n{body}")
            #print(event)
            if event.message.text == "fsm結構圖":
                link = show_fsm(event)
                print(link)
                #try:
                #    response = machine[event.source.user_id].advance(event)
                #except:
                #    response = machine[event.source.user_id].advance(event, link)
                #print("dfe")
                #print(machine[event.source.user_id].state) 
            print(machine[event.source.user_id].state)
            response = machine[event.source.user_id].advance(event)
            print(response)
            print(machine[event.source.user_id].state)
            if response == False:
                send_text_message(event.reply_token, "Invalid command, try againi\n請隨意輸入已回到主選單")
                print(event.message.text)
                machine[event.source.user_id].go_back()
                print(machine[event.source.user_id].state)
                #send_text_message(event.reply_token, "請隨意輸入以回到主選單")
                #response = machine[event.source.user_id].advance(event)
                #print(response)
            print('dddddd')
        #return "OK"
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

#@app.route("/show-fsm", methods=["GET"])
def show_fsm(event):
     machine[event.source.user_id].get_graph().draw("fsm.png", prog="dot", format="png")
     #print(settings.STATIC_ROOT)
     CLIENT_ID = "20b51ca78c975e9"
     CLIENT_SECRET = "b6fe2a673a273dabaa027120e1de3e4bc54651a0"
     PATH = "fsm.png"
     im = pyimgur.Imgur(CLIENT_ID)
     uploaded_image = im.upload_image(PATH, title="upload")
     return uploaded_image.link
     #url = settings.STATIC_ROOT+'/image'
     #im1 = Image.open("image/")
     #im1 = im1.save("fsm.png")
def isValidDate(date):
    try:
        print(date)
        print(time.strptime(date, "%m/%d/%Y"))
        return True
    except:
        return False

