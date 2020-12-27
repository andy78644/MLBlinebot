from transitions.extensions import GraphMachine
#from flask import Flask, jsonify, request, abort, send_file
from linebot import LineBotApi, WebhookParser
from linebot.models import *
from mlblinebot.utils import send_text_message, send_image_url, send_video_url, send_news_carousel, send_template_message, send_image_carousel, send_button_message, send_button_carousel, showGames, yesterGames, push_message, scrapeBoxscore, searchplayer, searchteam, showstanding, statleader, showschedule, showmeme, shownews, searchgame
import statsapi
import mlblinebot.message_template as message_template
import os
from django.conf import settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
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


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        #self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    def is_going_to_lobby(self, event):
        text = event.message.text
        return True
    def is_going_to_menu(self, event):
        text = event.message.text
        return text == "lobby"
    def is_going_to_teamstats(self, event):
        text = event.message.text
        return text.lower() == "戰績表" 
    def is_going_to_dateGame(self, event):
        text = event.message.text
        return text.lower() == "日期選擇"
    def is_going_to_GameChoose(self, event):
        text = event.message.text
        print(event.message.text)
        return text == "比賽查詢"
    def is_going_to_leaguechoose(self, event):
        text =event.message.text
        return text.lower() == "選擇聯盟"
    def is_going_to_datestats(self, event):
        text = event.message.text
        print("check")
        return True
    def is_going_to_todayGame(self, event):
        text = event.message.text
        return text == "即時比數"
    def is_going_to_watchGame(self, event):
        text = event.message.text
        return text.lower() == "watch game"
    def is_going_to_national(self, event):
        text = event.message.text
        return text.lower() == "國聯"
    def is_going_to_amarican(self, event):
        text = event.message.text
        return text == "美聯"
    def is_going_to_show_fsm_pic(self, event):
        text = event.message.text
        return text == "fsm結構圖"
    def on_enter_lobby(self, event):
        #userid = event.source.user_id
        #send_button_carousel(userid)
        reply_token = event.reply_token
        message = message_template.main_menu
        message_to_reply = FlexSendMessage("開啟主選單", message)
        #line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        print(line_bot_api)
        line_bot_api.reply_message(reply_token, message_to_reply)
    def on_enter_menu(self, event):
        #userid = event.source.user_id
        #send_button_carousel(userid)
        reply_token = event.reply_token
        message = message_template.main_menu
        message_to_reply = FlexSendMessage("開啟主選單", message)
        #line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        print(line_bot_api)
        line_bot_api.reply_message(reply_token, message_to_reply)
    '''
    def on_enter_gamechoose(self, event):
        #userid = event.source.user_id
        #send_button_carousel(userid)
        reply_token = event.reply_token
        message = message_template.main_menu
        message_to_reply = FlexSendMessage("開啟主選單", message)
        #line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        print(line_bot_api)
        line_bot_api.reply_message(reply_token, message_to_reply)
    '''
    def on_enter_GameChoose(self, event):
        print("hello4")
        reply_token = event.reply_token
        message = message_template.game_menu
        print("hello")
        message_to_reply = FlexSendMessage("選擇賽況", message)
        #line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        print(line_bot_api)
        line_bot_api.reply_message(reply_token, message_to_reply)
    def on_enter_dateGame(self, event):
        #userid = event.source.user_id
        #send_button_carousel(userid)
        print("hello3")
        reply_token = event.reply_token
        message_to_reply = send_text_message(event.reply_token, "請輸入日期(ex:09/30/2020)")
        #line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        #print(line_bot_api)
        #line_bot_api.reply_message(reply_token, message_to_reply)
    def on_enter_show_fsm_pic(self, event):
        reply_token = event.reply_token
        message = message_template.show_pic
        message["contents"][0]["hero"]["url"] = "https://i.imgur.com/sDT8I14.png"
        message["contents"][0]["footer"]["contents"][0]["action"]["uri"] = "https://i.imgur.com/sDT8I14.png"
        message_to_reply = FlexSendMessage("fsm結構圖", message)
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        #print("abc")
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()
    def on_enter_national(self, event):
        reply_token = event.reply_token
        message = message_template.stats_message
        #message = message_template.league_menu
        stats = {
            "type": "text",
            "text":statsapi.standings(leagueId=104),
            "wrap" : True,
        }
        message["body"]["contents"].append(stats)
        message_to_reply = FlexSendMessage("戰績表", message)
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.reply_message(reply_token, message_to_reply)
    def on_enter_datestats(self, event):
        print("I'm entering todayGame")
        reply_token = event.reply_token
        set_date = event.message.text
        games = statsapi.schedule(date = set_date)
        #games = statsapi.schedule()
        message = []
        #for game in games:
        #    message.append(game)
        #value_now =
        print(message)
        message = message_template.now_table
        print(games)
        message["body"]["contents"][0]["contents"][0]["contents"][0]["text"] = set_date+"賽程"
        if games==[]:
            #print(message["body"]["contents"][0]["contents"][0]["contents"])
            if(len(message["body"]["contents"][0]["contents"][0]["contents"])==1):
                data = {
                    "type": "text",
                    "text": f"本日無比賽",
                    "wrap": True,
                }
                message["body"]["contents"][0]["contents"][0]["contents"].append(data)
        for game in games:
            home = game['home_name']
            away = game['away_name']
            home_score = game['home_score']
            away_score = game['away_score']
            data = {
                "type": "text",
                "text": f"{home}({home_score}) vs\n{away}({away_score})\n",
                "wrap": True,
            }
            message["body"]["contents"][0]["contents"][0]["contents"].append(data)
        message_to_reply = FlexSendMessage("賽程", message)
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        print("abc")
        line_bot_api.reply_message(reply_token, message_to_reply)
        print("ggggggggggg")
        self.go_back()
    def on_enter_todayGame(self, event):
        print("I'm entering todayGame")
        reply_token = event.reply_token
        #games = statsapi.schedule(date = "09/15/2020")
        games = statsapi.schedule()
        message = []
        #for game in games:
        #    message.append(game)
        #value_now =
        print(message)
        message = message_template.now_table
        print(games)
        if games==[]:
            #print(message["body"]["contents"][0]["contents"][0]["contents"])
            if(len(message["body"]["contents"][0]["contents"][0]["contents"])==1):
                data = {
                    "type": "text",
                    "text": f"今日無比賽",
                    "wrap": True,
                }
                message["body"]["contents"][0]["contents"][0]["contents"].append(data)
        for game in games:
            home = game['home_name']
            away = game['away_name']
            home_score = game['home_score']
            away_score = game['away_score']
            data = {
                "type": "text",
                "text": f"{home}({home_score}) vs\n{away}({away_score})\n",
                "wrap": True,
            }
            message["body"]["contents"][0]["contents"][0]["contents"].append(data)
        message_to_reply = FlexSendMessage("賽程", message)
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        print("abc")
        line_bot_api.reply_message(reply_token, message_to_reply)
        print("ggggggggggg")
        self.go_back()
    def on_enter_testing(self, event):
        print("I'm entering testing")
        # reply_token = event.reply_token
        userid = event.source.user_id

        url1 = 'https://pbs.twimg.com/media/ELFOUvGVAAA3-Tx.jpg'
        title = 'title'
        uptext = 'uptext'
        labels = ['yes', 'no']
        texts = ['yes', 'no']
        send_button_message(userid, url1, title, uptext, labels, texts)
        # send_news_carousel(userid, urls, labels, urls)
        # send_image_map(userid)
        self.go_back(event)
    def on_enter_leaguechoose(self, event):
        reply_token = event.reply_token
        message = message_template.league_menu
        message_to_reply = FlexSendMessage("聯盟對戰", message)
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        #print(line_bot_api)
        line_bot_api.reply_message(reply_token, message_to_reply)
        #self.go_back()
    '''
    def on_enter_national(self, event):
        reply_token = event.reply_token
        message = message_template.stats_message
        #message = message_template.league_menu
        stats = {
            "type": "text",
            "text":statsapi.standings(leagueId=104),
            "wrap" : True,
            "size" : "sm",
        }
        message["body"]["contents"].append(stats)
        message_to_reply = FlexSendMessage("戰績表", message)
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.reply_message(reply_token, message_to_reply)
    '''
    def on_enter_national(self,event):
        reply_token = event.reply_token
        data = statsapi.standings_data(leagueId=104)
        content = [
            {
                "type": "text",
                "text": "戰績",
                "weight": "bold",
                "size": "lg",
                "margin": "lg",
                "align": "center"
             },
        ]
        message = message_template.stats2_message
        for i in data:
            stats_head = {
             "type": "text",
             "text": data[i]['div_name'],
            }
            content.append(stats_head)
            stats_body = {
                "type": "box",
                "layout": "horizontal",
                "align" : "start",
                "contents": [
                ],
                "paddingAll": "0px",
            }
            print(i)
            key = []
            for j in data[i]['teams'][0]:
                key.append(j)
            tmp = key[0]
            key[0]=key[1]
            key[1]=tmp
            tmp = key[8]
            key[8] = key[7]
            key[7] = key[6]
            key[6] = key[5]
            key[5] = tmp
            print(key)
            for j in key:
                flex = 1
                align = "end"
                index = {"div_rank":"rank","name":"team","w":"W","l":"L","gb":"GB","wc_rank":"WC_RANK","wc_gb":"WC_GB","elim_num":"(E)","wc_elim_num":"(E)"}
                if j == "name":
                    flex = 4
                    align = "center"
                if j == "wc_rank" or j == "wc_gb":
                    flex = 2
                if j == "team_id":
                    continue
                tmp = {
                     "type": "box",
                     "layout": "vertical",
                     "contents": [
                     ],
                     "flex" : flex
                }
                tmp_data = {
                    "type": "text",
                    "text": index[j],
                    "align" : align,
                    "size": "sm",
                    "flex": flex,
                }
                tmp["contents"].append(tmp_data)
                for k in data[i]['teams']:
                    tmp_data = {
                        "type": "text",
                        "text": str(k[j]),
                        "align" : "end",
                        "size": "sm",
                        "flex": flex,
                    }
                    tmp["contents"].append(tmp_data)
                    #print(type(k[j]))
                stats_body["contents"].append(tmp)
            
            content.append(stats_body)
        stats2 = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "",
                    "wrap": True,
                  },
                  {
                    "type": "text",
                    "text": "ab",

                  },

                ]
              }
            ]
        }
        message["body"]["contents"] = content
        message_to_reply = FlexSendMessage("戰績表", message) 
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.reply_message(reply_token, message_to_reply)
    '''
    def on_enter_amarican(self, event):
        reply_token = event.reply_token
        message = message_template.stats_message
        #message = message_template.league_menu
        stats = {
            "type": "text",
            "text":statsapi.standings(leagueId=103),
            "wrap" : True,
            "size" : "sm",
        }
        message["body"]["contents"].append(stats)
        
        message_to_reply = FlexSendMessage("戰績表", message) 
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.reply_message(reply_token, message_to_reply)
    '''
    def on_enter_amarican(self,event):
        reply_token = event.reply_token
        data = statsapi.standings_data(leagueId=103)
        content = [
            {
                "type": "text",
                "text": "戰績",
                "weight": "bold",
                "size": "lg",
                "margin": "lg",
                "align": "center"
             },
        ]
        message = message_template.stats2_message
        for i in data:
            stats_head = {
             "type": "text",
             "text": data[i]['div_name'],
            }
            content.append(stats_head)
            stats_body = {
                "type": "box",
                "layout": "horizontal",
                "align" : "start",
                "contents": [
                ],
                "paddingAll": "0px",
            }
            print(i)
            key = []
            for j in data[i]['teams'][0]:
                key.append(j)
            tmp = key[0]
            key[0]=key[1]
            key[1]=tmp
            tmp = key[8]
            key[8] = key[7]
            key[7] = key[6]
            key[6] = key[5]
            key[5] = tmp
            print(key)
            for j in key:
                flex = 1
                align = "end"
                index = {"div_rank":"rank","name":"team","w":"W","l":"L","gb":"GB","wc_rank":"WC_RANK","wc_gb":"WC_GB","elim_num":"(E)","wc_elim_num":"(E)"}
                if j == "name":
                    flex = 4
                    align = "center"
                if j == "wc_rank" or j == "wc_gb":
                    flex = 2
                if j == "team_id":
                    continue
                tmp = {
                     "type": "box",
                     "layout": "vertical",
                     "contents": [
                     ],
                     "flex" : flex
                }
                tmp_data = {
                    "type": "text",
                    "text": index[j],
                    "align" : align,
                    "size": "sm",
                    "flex": flex,
                }
                tmp["contents"].append(tmp_data)
                for k in data[i]['teams']:
                    tmp_data = {
                        "type": "text",
                        "text": str(k[j]),
                        "align" : "end",
                        "size": "sm",
                        "flex": flex,
                    }
                    tmp["contents"].append(tmp_data)
                    #print(type(k[j]))
                stats_body["contents"].append(tmp)
            
            content.append(stats_body)
        stats2 = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "",
                    "wrap": True,
                  },
                  {
                    "type": "text",
                    "text": "ab",

                  },

                ]
              }
            ]
        }
        message["body"]["contents"] = content
        message_to_reply = FlexSendMessage("戰績表", message) 
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.reply_message(reply_token, message_to_reply)
           
    '''
    
    def on_enter_searchplayer(self, event):
        print("I'm entering searchplayer")
        reply_token = event.reply_token
        userid = event.source.user_id

        lbj = 'https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fpeopledotcom.files.wordpress.com%2F2019%2F10%2Flebron-james.jpg&w=400&c=sc&poi=face&q=85'
        luka = 'https://www.talkbasket.net/wp-content/uploads/2019/11/THUMBNAIL_043-3.webp'
        freak = 'https://scd.infomigrants.net/media/resize/my_image_medium/4c1a91cf3cd1e4ec2f373a7e520e84b118a0f638.jpeg'
        harden = 'https://sportshub.cbsistatic.com/i/r/2019/10/07/3db9fcb5-5c81-46e1-ae16-fbb0f75b7e99/thumbnail/770x433/a0dfdaa544a8a4899f58aaada49772fd/james-harden.jpg'
        ad = 'https://specials-images.forbesimg.com/imageserve/1189030491/960x0.jpg?fit=scale'
        urls = [lbj, luka, freak, harden, ad]
        labels = ['LeBron James', 'Luka Doncic', 'Giannis', 'James Harden', 'A.D.']
        texts = ['LeBron James', 'Luka Dončić', 'Giannis Antetokounmpo', 'James Harden', 'Anthony Davis']
        send_image_carousel(userid, urls, labels, texts)

        msg = "Press on the \"GOATS\" above or enter a player name"
        push_message(userid, msg)
    '''
    def on_enter_watchGame(self, event):
        print("I'm entering watchGame")

        reply_token = event.reply_token
        userid = event.source.user_id
        
        img = 'https://images-na.ssl-images-amazon.com/images/I/61G5S99JAAL.jpg'
        title = 'Watch game scores'
        uptext = 'Which day would you like to watch?'
        labels = ['Game today', 'Game yesterday', 'Enter a date']
        texts = ['today game', 'yesterday game', 'search game']
        send_button_message(userid, img, title, uptext, labels, texts)

        # result = "Watch today game or yesterday game or search a date?\n"
        # result += "(today game / yesterday game / search game)"
        # push_message(userid, result)


   
