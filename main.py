from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, TemplateSendMessage,ButtonsTemplate,URIAction,QuickReplyButton,QuickReply
)

import time
import math
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import random


from pytrends.request import TrendReq  #グーグルトレンドの情報取得
import pandas as pd  #データフレームで扱う
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import datetime
import codecs
#from datetime import date, datetime, timedelta
from datetime import datetime as dt
from io import BytesIO
import urllib
import os,io
import base64
import json
import urllib.request

import numpy as np
import boto3

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
aws_s3_bucket        = os.environ['AWS_BUCKET']

def download(day):
    url = 'https://trends.google.com/trends/api/dailytrends?geo=JP&ed={}'.format(day)
    title = 'trends{}.txt'.format(day)
    urllib.request.urlretrieve(url,"{0}".format(title))
    with open(title) as f:
    	data = f.read()
    data = data[5:]
    jsondata = json.loads(data.encode('utf-16be'))
    with open('trends{}.json'.format(day), 'w') as f:
    	json.dump(jsondata, f)

def tl_text(tl1):
    try:
        text1 = tl1[0]
    except:
        text1 = "なし"
    try:
        text2 = tl1[1]
    except:
        text2 = "なし"
    try:
        text3 = tl1[2]
    except:
        text3 = "なし"
    try:
        text4 = tl1[3]
    except:
        text4 = "なし"
    try:
        text5 = tl1[4]
    except:
        text5 = "なし"
    try:
        text6 = tl1[5]
    except:
        text6 = "なし"
    try:
        text7 = tl1[6]
    except:
        text7 = "なし"
    try:
        text8 = tl1[7]
    except:
        text8 = "なし"
    try:
        text9 = tl1[8]
    except:
        text9 = "なし"
    try:
        text10 = tl1[9]
    except:
        text10 = "なし"
    return text1, text2, text3, text4, text5, text6, text7, text8, text9, text10


def flex01(tl1,tl2,tl3,tl4,url):
    text,text2,text3,text4,text5,text6,text7,text8,text9,text10 = tl_text(tl1)
    text_2,text2_2,text3_2,text4_2,text5_2,text6_2,text7_2,text8_2,text9_2,text10_2 = tl_text(tl2)
    text_3,text2_3,text3_3,text4_3,text5_3,text6_3,text7_3,text8_3,text9_3,text10_3 = tl_text(tl3)
    text_4,text2_4,text3_4,text4_4,text5_4,text6_4,text7_4,text8_4,text9_4,text10_4 = tl_text(tl4)
    flex = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": url,
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "トレンドの変化",
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "表示期間",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "30日",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "トレンド情報",
            "weight": "bold",
            "color": "#ff7f50"
          },
          {
            "type": "text",
            "text": "関連キーワード",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "トップ",
            "size": "lg",
            "color": "#aaaaaa",
            "wrap": True
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
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
                    "text": text
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text5
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text6
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text7
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text8
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text9
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text10
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "Made by Retasu",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "@retasu_0141",
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "トレンド情報",
            "weight": "bold",
            "color": "#ff7f50"
          },
          {
            "type": "text",
            "text": "関連キーワード",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "急上昇",
            "size": "lg",
            "color": "#aaaaaa",
            "wrap": True
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
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
                    "text": text_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text2_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text3_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text4_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text5_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text6_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text7_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text8_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text9_2
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text10_2
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "Made by Retasu",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "@retasu_0141",
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "トレンド情報",
            "weight": "bold",
            "color": "#ff7f50"
          },
          {
            "type": "text",
            "text": "関連トピック",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "トップ",
            "size": "lg",
            "color": "#aaaaaa",
            "wrap": True
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
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
                    "text": text_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text2_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text3_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text4_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text5_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text6_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text7_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text8_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text9_3
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text10_3
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "Made by Retasu",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "@retasu_0141",
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "トレンド情報",
            "weight": "bold",
            "color": "#ff7f50"
          },
          {
            "type": "text",
            "text": "関連トピック",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "急上昇",
            "size": "lg",
            "color": "#aaaaaa",
            "wrap": True
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
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
                    "text": text_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text2_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text3_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text4_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text5_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text6_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text7_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text8_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text9_4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": text10_4
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "Made by Retasu",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "@retasu_0141",
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
  ]
}
    return flex


def flex02(T1,T2,T3,trendlist,trendlist_2,day):
    '''
    T1['articles'][0]['title']
    T1['articles'][0]['source']
    T1['articles'][0]['image']['newsUrl']
    T1['articles'][0]['image']['imageUrl']
    T1['articles'][0]['snippet']
    '''
    try:
        T1img = T1['articles'][0]['image']['imageUrl']
        T1url = T1['articles'][0]['image']['newsUrl']
    except:
        try:
            T1img = T1['articles'][1]['image']['imageUrl']
            T1url = T1['articles'][1]['image']['newsUrl']
        except:
            T1img = T1['articles'][2]['image']['imageUrl']
            T1url = T1['articles'][2]['image']['newsUrl']

    try:
        T2img = T2['articles'][0]['image']['imageUrl']
        T2url = T2['articles'][0]['image']['newsUrl']
    except:
        try:
            T2img = T2['articles'][1]['image']['imageUrl']
            T2url = T2['articles'][1]['image']['newsUrl']
        except:
            T2img = T2['articles'][2]['image']['imageUrl']
            T2url = T2['articles'][2]['image']['newsUrl']

    try:
        T3img = T3['articles'][0]['image']['imageUrl']
        T3url = T3['articles'][0]['image']['newsUrl']
    except:
        try:
            T3img = T3['articles'][1]['image']['imageUrl']
            T3url = T3['articles'][1]['image']['newsUrl']
        except:
            T3img = T3['articles'][2]['image']['imageUrl']
            T3url = T3['articles'][2]['image']['newsUrl']

    text,text2,text3,text4,text5,text6,text7,text8,text9,text10 = tl_text(trendlist[0:10:1])
    text_,text2_,text3_,text4_,text5_,text6_,text7_,text8_,text9_,text10_ = tl_text(trendlist[10:20:1])

    _text,_text2,_text3,_text4,_text5,_text6,_text7,_text8,_text9,_text10 = tl_text(trendlist_2[0:10:1])
    _text_,_text2_,_text3_,_text4_,_text5_,_text6_,_text7_,_text8_,_text9_,_text10_ = tl_text(trendlist_2[10:20:1])

    flex = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": day+"のトレンド",
            "weight": "bold",
            "color": "#ff7f50",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "トレンド一覧",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "2020-09-06",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "text",
                "text": "・1 "+text+text_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・2 "+text2+_text2,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・3 "+text3+_text3,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・4 "+text4+text4_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・5 "+text5+_text5,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・6 "+text6+_text6,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・7 "+text7+_text7,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・8 "+text8+_text8,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・9 "+text9+_text9,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・10 "+text10+_text10,
                "size": "md"
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "Made by Retasu",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "@retasu_0141",
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": day+"のトレンド",
            "weight": "bold",
            "color": "#ff7f50",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "トレンド一覧2",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "2020-09-06",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "text",
                "text": "・11 "+text_+_text_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・12 "+text2_+_text2_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・13 "+text3_+_text3_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・14 "+text4_+_text4_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・15 "+text5_+_text5_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・16 "+text6_+_text6_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・17 "+text7_+_text7_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・18 "+text8_+_text8_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・19 "+text9_+_text9_,
                "size": "md"
              },
              {
                "type": "text",
                "text": "・20 "+text10_+_text10_,
                "size": "md"
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "Made by Retasu",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
              },
              {
                "type": "text",
                "text": "@retasu_0141",
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "url": T1img
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": T1['articles'][0]['title'],
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": T1['articles'][0]['snippet'],
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0
                  }
                ],
                "spacing": "lg"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "記事を読む",
                      "uri": T1url
                    },
                    "position": "relative",
                    "height": "sm",
                    "style": "link"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xxl",
                "height": "40px"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": T1['articles'][0]['source'],
                "color": "#ffffff",
                "offsetStart": "7px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#4169e1",
            "offsetStart": "18px",
            "height": "25px",
            "width": "140px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "url": T2img
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": T2['articles'][0]['title'],
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": T2['articles'][0]['snippet'],
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0
                  }
                ],
                "spacing": "lg"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "記事を読む",
                      "uri": T2url
                    },
                    "position": "relative",
                    "height": "sm",
                    "style": "link"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xxl",
                "height": "40px"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": T2['articles'][0]['source'],
                "color": "#ffffff",
                "offsetStart": "7px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#4169e1",
            "offsetStart": "18px",
            "height": "25px",
            "width": "140px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "url": T3img
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": T3['articles'][0]['title'],
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": T3['articles'][0]['snippet'],
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0
                  }
                ],
                "spacing": "lg"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "記事を読む",
                      "uri": T3url
                    },
                    "position": "relative",
                    "height": "sm",
                    "style": "link"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xxl",
                "height": "40px"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": T3['articles'][0]['source'],
                "color": "#ffffff",
                "offsetStart": "7px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#4169e1",
            "offsetStart": "18px",
            "height": "25px",
            "width": "140px"
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
    return flex


@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_from = event.reply_token
    msg_text = event.message.text
    user_id = event.source.user_id
    if msg_text == '昨日のトレンド':

        today__ = datetime.date.today()
        yesterday__ = today__ - datetime.timedelta(1)
        yesterday_ = str(yesterday__)
        yesterday = yesterday_.replace('-', '')

        download(yesterday)

        JSON_FILE = 'trends{}.json'.format(yesterday)
        with open(JSON_FILE) as f:
            data = json.load(f)
    	#print(json.dumps(data,ensure_ascii=False, indent=2))
        kye1 = data['default']['trendingSearchesDays']
        kye2 = kye1[0]


        day = kye2['date']
        formattedDate = kye2['formattedDate']
        #トレンドは20個ある
        #print(len(kye2['trendingSearches']))
        #→20

        kye3 = kye2['trendingSearches']
        #トレンド1位
        T1 = kye3[0]
        T2 = kye3[1]
        T3 = kye3[2]
        #トレンドのタイトル
        T1title = T1['title']['query']
        #検索件数
        T1search = T1['formattedTraffic']
        #検索結果の関連(リスト) T1relatedQueries_list
        T1relatedQueries = T1['relatedQueries']
        T1relatedQueries_list = []
        for kye in T1relatedQueries:
        	T1relatedQueries_list.append(kye['query'])
        #記事
        #記事は6つある
        #print(len(T1['articles']))
        #→6
        #title = []
        #source = []
        #newsUrl = []
        #imageUrl = []
        #snippet = []
        #for kye in T1['articles']:
        #    title.append(kye['title'])
        #    source.append(kye['source'])
        #    newsUrl.append(kye['image']['newsUrl'])
        #    imageUrl.append(kye['image']['imageUrl'])
        #    snippet.append(kye['snippet'])
        #トレンドを全部とる
        trendlist = [] #トレンドリスト
        for kye in kye3:
        	trendlist.append(kye['title']['query'])
        #トレンドの検索回数を全部とる
        trendlist_2 = [] #検索回数リスト
        for kye in kye3:
        	trendlist_2.append(kye['formattedTraffic'])
        #トレンドの関連を全部とる
        trendlist_3 = []
        for kye in kye3:
        	hogelist = []
        	for kye2 in kye['relatedQueries']:
        		hogelist.append(kye2['query'])
        	trendlist_3.append(hogelist)
        numbers = list(range(1,20))

        text_list = []
        #'トレンド{number}位{1}。検索回数{2}。関連{3}。'
        for number,rank,search,Relation in zip(numbers,trendlist,trendlist_2,trendlist_3):
        	txt = 'トレンド{n}位{r}。検索回数{s}。関連{re}。'.format(n=number,r=rank,s=search,re=Relation)
        	text_list.append(txt)
        flex_ = flex02(T1,T2,T3,trendlist,trendlist_2,"昨日")
        flex = {"type": "flex","altText": msg_text,"contents":flex_}
        container_obj = FlexSendMessage.new_from_json_dict(flex)

        line_bot_api.reply_message(msg_from,messages=container_obj)
    if msg_text == '今日のトレンド':
        today__ = datetime.date.today()
        today_ = str(today__)
        today = today_.replace('-', '')

        download(today)

        JSON_FILE = 'trends{}.json'.format(today)
        with open(JSON_FILE) as f:
            data = json.load(f)
    	#print(json.dumps(data,ensure_ascii=False, indent=2))
        kye1 = data['default']['trendingSearchesDays']
        kye2 = kye1[0]


        day = kye2['date']
        formattedDate = kye2['formattedDate']
        #トレンドは20個ある
        #print(len(kye2['trendingSearches']))
        #→20

        kye3 = kye2['trendingSearches']
        #トレンド1位
        T1 = kye3[0]
        T2 = kye3[1]
        T3 = kye3[2]
        #トレンドのタイトル
        T1title = T1['title']['query']
        #検索件数
        T1search = T1['formattedTraffic']
        #検索結果の関連(リスト) T1relatedQueries_list
        T1relatedQueries = T1['relatedQueries']
        T1relatedQueries_list = []
        for kye in T1relatedQueries:
        	T1relatedQueries_list.append(kye['query'])
        #記事
        #記事は6つある
        #print(len(T1['articles']))
        #→6
        #title = []
        #source = []
        #newsUrl = []
        #imageUrl = []
        #snippet = []
        #for kye in T1['articles']:
        #    title.append(kye['title'])
        #    source.append(kye['source'])
        #    newsUrl.append(kye['image']['newsUrl'])
        #    imageUrl.append(kye['image']['imageUrl'])
        #    snippet.append(kye['snippet'])
        #トレンドを全部とる
        trendlist = [] #トレンドリスト
        for kye in kye3:
        	trendlist.append(kye['title']['query'])
        #トレンドの検索回数を全部とる
        trendlist_2 = [] #検索回数リスト
        for kye in kye3:
        	trendlist_2.append(kye['formattedTraffic'])
        #トレンドの関連を全部とる
        trendlist_3 = []
        for kye in kye3:
        	hogelist = []
        	for kye2 in kye['relatedQueries']:
        		hogelist.append(kye2['query'])
        	trendlist_3.append(hogelist)
        numbers = list(range(1,20))

        text_list = []
        #'トレンド{number}位{1}。検索回数{2}。関連{3}。'
        for number,rank,search,Relation in zip(numbers,trendlist,trendlist_2,trendlist_3):
        	txt = 'トレンド{n}位{r}。検索回数{s}。関連{re}。'.format(n=number,r=rank,s=search,re=Relation)
        	text_list.append(txt)
        flex_ = flex02(T1,T2,T3,trendlist,trendlist_2,"今日")
        flex = FlexSendMessage(alt_text="hoge", contents=flex_)
        #flex = {"type": "flex","altText": msg_text,"contents":flex_}
        #container_obj = FlexSendMessage.new_from_json_dict(flex)

        line_bot_api.reply_message(msg_from,messages=flex)

    else:
        plt.clf()
        #os.remove("static\photo\img.png")

        keyword = msg_text
        # 今日
        today = datetime.date.today()

        # 30日前
        day = today - datetime.timedelta(30)

        #print(day)

        dt_now = dt.now()

        dt_now_s = str(dt_now.microsecond)
        pytrends = TrendReq(hl='ja-JP', tz=360)
        #keyword=''
        kw_list = [keyword]
        pytrends.build_payload(kw_list, cat=0, timeframe=str(day)+' '+str(today), geo='JP', gprop='')
        df = pytrends.interest_over_time() #時系列データを取り出す
        df.to_csv(dt_now_s+".csv", encoding='cp932')
        #関連トピック
        df = pytrends.related_topics()
        #トップ
        try:
            text_ = df[keyword]['top'].loc[:,['topic_title']].head(10)
            tl1 = text_['topic_title']
        except:
            tl1=['なし']
        #上昇
        try:
            text2_ = df[keyword]['rising'].loc[:,['topic_title']].head(10)
            tl2 = text2_['topic_title']
        except:
            tl2=['なし']


        #関連キーワード
        df = pytrends.related_queries()
        #トップ
        try:
            text3_ = df[keyword]['top'].head(10)
            tl3 = text3_['query']
        except:
            tl3=['なし']
        #上昇
        try:
            text4_ = df[keyword]['rising'].head(10)
            tl4 = text4_['query']
        except:
            tl4=['なし']
        #print(keyword+'.csv')
        #print(tl1)
        #print(tl2)
        #print(tl3)
        #print(tl4)

        df = pd.read_csv(dt_now_s+'.csv',encoding='cp932')


        '''
        print(df)
        print(df.columns)
        print(df['date'])
        print(df[keyword])
        '''
        img = io.BytesIO()
        #グラフの作成
        fig = plt.figure()
        plt.figure(1)
        plt.plot(df['date'],df[keyword],marker="o")
        #グラフの軸
        plt.xlabel(df['date'].name)
        plt.ylabel(keyword)
        plt.xticks(rotation=60)
        file_name = dt_now_s + '.png'
        plt.savefig(file_name)
        s3_resource = boto3.resource('s3')
        s3_resource.Bucket(aws_s3_bucket).upload_file(file_name, file_name)
        s3_client = boto3.client('s3')
        s3_image_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params       = {'Bucket': aws_s3_bucket, 'Key': file_name},
            ExpiresIn    = 10,
            HttpMethod   = 'GET'
        )

        #s3_image_url

        #canvas = FigureCanvasAgg(fig)
        #canvas.print_png(buf)
        #data = buf.getvalue()

        #plt.savefig(img, format='png')
        #img.seek(0)

        #plot_url = base64.b64encode(img.getvalue()).decode()
        flex_ = flex01(tl3,tl4,tl1,tl2,s3_image_url)
        flex = {"type": "flex","altText": keyword + "のトレンド","contents":flex_}
        container_obj = FlexSendMessage.new_from_json_dict(flex)

        line_bot_api.reply_message(msg_from,messages=container_obj)




if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
