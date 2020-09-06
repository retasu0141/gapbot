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
            "text": "hogeのトレンド情報",
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
            "text": "hogeのトレンド情報",
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
            "text": "hogeのトレンド情報",
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
            "text": "hogeのトレンド情報",
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
    if msg_text == 'ゲーム実況':
        #items = {'items': [{'type': 'action','action': {'type': 'message','label': '貯める','text': '貯める'}},{'type': 'action','action': {'type': 'message','label': '使う','text': '使う'}}]}
        #line_bot_api.reply_message(msg_from,TextSendMessage(text='まずは貯めるのか使うのかを教えてね！',quick_reply=items))
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
            tl2==['なし']


        #関連キーワード
        df = pytrends.related_queries()
        #トップ
        try:
            text3_ = df[keyword]['top'].head(10)
            tl3 = text3_['query']
        except:
            tl3==['なし']
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
        flex_ = flex01(tl1,tl2,tl3,tl4,s3_image_url)
        flex = {"type": "flex","altText": "flex message","contents":flex_}
        container_obj = FlexSendMessage.new_from_json_dict(flex)

        line_bot_api.reply_message(msg_from,messages=container_obj)

        #plt.savefig("static\photo\img.png")
        #plt.close()
        #fig.savefig("static\img.png")
        #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "img.png")

        #グラフ表示
        #plt.show()
        #return '<img src="data:image/png;base64,{}">'.format(plot_url)
        #return render_template('choice.html',text=text,text2=text2,text3=text3,text4=text4,img="data:image/png;base64,{}".format(plot_url))
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
            tl2==['なし']


        #関連キーワード
        df = pytrends.related_queries()
        #トップ
        try:
            text3_ = df[keyword]['top'].head(10)
            tl3 = text3_['query']
        except:
            tl3==['なし']
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
        flex_ = flex01(tl1,tl2,tl3,tl4,s3_image_url)
        flex = {"type": "flex","altText": "flex message","contents":flex_}
        container_obj = FlexSendMessage.new_from_json_dict(flex)

        line_bot_api.reply_message(msg_from,messages=container_obj)




if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
