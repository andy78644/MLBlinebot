
main_menu = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/2bTSlEQ.jpg",
        "size": "full",
        "aspectMode": "fit",
        "aspectRatio": "1.25:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "即時比數",
              "text": "即時比數"
            },
            "height": "md",
            "color": "#ff9900",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/N1idZ4G.jpg",
        "size": "full",
        "aspectMode": "fit",
        "aspectRatio": "1.25:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "隊伍戰績",
              "text": "選擇聯盟"
            },
            "height": "md",
            "color": "#ff6666",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/irKr7hy.png",
        "size": "full",
        "aspectMode": "fit",
        "aspectRatio": "1.25:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "fsm結構圖",
              "text": "fsm結構圖"
            },
            "height": "md",
            "color": "#ff66b3",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    },
  ]
}

now_table = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "今日賽程\n",
                "size": "lg",
                "margin": "lg",
                "color": "#555555",
                "align": "center",
                "wrap": True,

              },
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "action": {
          "type": "message",
          "label": "返回主選單",
          "text": "lobby"
        }
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}
league_menu = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "聯盟選擇",
            "weight": "bold",
            "align": "center",
            "size": "lg"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "美聯",
              "text": "美聯"
            },
            "height": "md",
            "color": "#00ff80",
            "style": "primary"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "國聯",
              "text": "國聯"
            },
            "height": "md",
            "color": "#00cc66",
            "style": "primary"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "返回主選單",
              "text": "lobby"
            },
            "height": "md",
            "color": "#00994d",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    }
  ]
}


stats_message = {
  "type": "bubble",
  "size": "giga",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "功能介紹",
        "weight": "bold",
        "size": "lg",
        "margin": "lg",
        "align": "center"
      },
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "action": {
          "type": "message",
          "label": "返回主選單",
          "text": "lobby"
        }
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}


show_pic = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/bwXOyBi.png",
        "aspectMode": "fit",
        "size": "full",
        "aspectRatio": "2:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "前往網頁看圖片",
              "uri": "https://i.imgur.com/bwXOyBi.png"
            },
            "height": "md",
            "color": "#5cd65c",
            "style": "primary"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "返回主選單",
              "text": "lobby"
            },
            "height": "md",
            "color": "#00cc66",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    }
  ]
}