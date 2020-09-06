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

from datetime import datetime as dt
from pytrends.request import TrendReq  #グーグルトレンドの情報取得
import pandas as pd  #データフレームで扱う
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import datetime
import codecs
from datetime import date, datetime, timedelta
from io import BytesIO
import urllib
import os,io
import base64
import json
import urllib.request

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
    global set_
    global stoptime
    global stoppoint
    msg_from = event.reply_token
    msg_text = event.message.text
    user_id = event.source.user_id
    if msg_text == 'ゲーム実況':
        plt.clf()
        #os.remove("static\photo\img.png")

        keyword = request.form['name']
        # 今日
        today = date.today()

        # 30日前
        day = today - timedelta(30)

        #print(day)

        dt_now = datetime.now()

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
            text__ = text_['topic_title']
            _text = '\n・'.join(text__)
            text = _text.replace('Name: topic_title, dtype: object', '')
        except:
            text = 'なし'
        #上昇
        try:
            text2_ = df[keyword]['rising'].loc[:,['topic_title']].head(10)
            text2__ = text2_['topic_title']
            _text2 = '\n・'.join(text2__)
            text2 = _text2.replace('Name: topic_title, dtype: object', '')
        except:
            text2 = 'なし'


        #関連キーワード
        df = pytrends.related_queries()
        #トップ
        try:
            text3_ = df[keyword]['top'].head(10)
            text3__ = text3_['query']
            _text3 = '\n・'.join(text3__)
            text3 = _text3.replace('Name: query, dtype: object', '')
        except:
            text3 = 'なし'
        #上昇
        try:
            text4_ = df[keyword]['rising'].head(10)
            text4__ = text4_['query']
            _text4 = '\n・'.join(text4__)
            text4 = _text4.replace('Name: query, dtype: object', '')
        except:
            text4 = 'なし'

        #print(keyword+'.csv')

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

        #canvas = FigureCanvasAgg(fig)
        #canvas.print_png(buf)
        #data = buf.getvalue()

        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        line_bot_api.reply_message = (msg_from,TextSendMessage(text=text))

        #plt.savefig("static\photo\img.png")
        #plt.close()
        #fig.savefig("static\img.png")
        #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "img.png")

        #グラフ表示
        #plt.show()
        #return '<img src="data:image/png;base64,{}">'.format(plot_url)
        return render_template('choice.html',text=text,text2=text2,text3=text3,text4=text4,img="data:image/png;base64,{}".format(plot_url))

    if msg_text == '設定する':
        items = {'items': [{'type': 'action','action': {'type': 'message','label': '貯める','text': '貯める'}},{'type': 'action','action': {'type': 'message','label': '使う','text': '使う'}}]}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずは貯めるのか使うのかを教えてね！',quick_reply=items))
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting_[user_id]['ID'] = user_id
        Time[user_id] = {'count':0,'pointcount_1':0,'pointcount_2':0,'pointcount2_1':0,'pointcount2_2':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        set_ = 2

        stoptime = 0

        stoppoint = 0
        setting2[user_id]['setting1'] = True


    if msg_text == '貯める' and setting2[user_id]['setting1'] == True and user_id == setting_[user_id]['ID']:
        setting_[user_id]['use'] = False
        setting2[user_id]['setting1'] = False
        setting2[user_id]['setting2'] = True
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！貯めるに設定したよ！\n次は行う人の名前を教えてね！(ニックネーム可)'))


    if msg_text == '使う' and setting2[user_id]['setting1'] == True and user_id == setting_[user_id]['ID']:
        setting_[user_id]['use'] = True
        setting2[user_id]['setting1'] = False
        setting2[user_id]['setting2'] = True
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！使うに設定したよ！\n次は行う人の名前を教えてね！(ニックネーム可)'))


    '''if setting2[user_id]['setting2'] == True and user_id == setting_[user_id]['ID']:
        print('ok')
        setting2[user_id]['setting2'] = False
        setting2[user_id]['setting3'] = True
        name = msg_text
        setting_[user_id]['name'] = name
        point = namecheck(user_id,name)
        setting_[user_id]['point'] = point
        items = {'items': [{'type': 'action','action': {'type': 'message','label': '10ポイント','text': '10'}},{'type': 'action','action': {'type': 'message','label': '20ポイント','text': '20'}},{'type': 'action','action': {'type': 'message','label': '50ポイント','text': '50'}},{'type': 'action','action': {'type': 'message','label': '100ポイント','text': '100'}}]}
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に取得するポイント数を設定してね！'.format(point),quick_reply=items))
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に消費するポイント数を設定してね！'.format(point),quick_reply=items))'''


    if setting2[user_id]['setting3'] == True and user_id == setting_[user_id]['ID']:
        setting2[user_id]['setting3'] = False
        setting2[user_id]['setting4'] = True
        str_timepoint = msg_text
        timepoint = int(str_timepoint)
        setting_[user_id]['timepoint'] = timepoint
        items = {'items': [{'type': 'action','action': {'type': 'message','label': '1分','text': '1'}},{'type': 'action','action': {'type': 'message','label': '5分','text': '5'}},{'type': 'action','action': {'type': 'message','label': '10分','text': '10'}},{'type': 'action','action': {'type': 'message','label': '30分','text': '30'}},{'type': 'action','action': {'type': 'message','label': '1時間','text': '60'}}]}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{}ポイントに設定できたよ！\n最後に、何分行うか設定してね！'.format(timepoint),quick_reply=items))


    if setting2[user_id]['setting4'] == True and user_id == setting_[user_id]['ID'] and ('' in msg_text):
        setting2[user_id]['setting4'] = False
        str_time = msg_text
        int_time = int(str_time)
        setting_[user_id]['time'] = int_time
        items = {'items': [{'type': 'action','action': {'type': 'message','label': 'スタート','text': 'スタート'}}]}
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{_time}分に設定できたよ！\n設定項目\n貯めるか使うか : 貯める\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの獲得ポイント : {timepoint}\n行う時間 : {time_}\n始める場合は スタート と言ってね'.format(_time=int_time,name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time']),quick_reply=items))
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{_time}分に設定できたよ！\n設定項目\n貯めるか使うか : 使う\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの消費ポイント : {timepoint}\n行う時間 : {time_}\n始める場合は スタート と言ってね'.format(_time=int_time,name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time']),quick_reply=items))

    if '設定確認' in msg_text:
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='設定項目\n貯めるか使うか : 貯める\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの獲得ポイント : {timepoint}\n行う時間 : {time_}'.format(name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time'])))
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='設定項目\n貯めるか使うか : 使う\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの消費ポイント : {timepoint}\n行う時間 : {time_}'.format(name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time'])))

    if 'スタート' == msg_text:
        s_point = round(setting_[user_id]['timepoint']/60,2)
        if set_ == 1 or set_ == 2:
            set_ = 1
            secs = setting_[user_id]['time']*60
            s.start()
            executer = ThreadPoolExecutor(1)
            executer.submit(count, secs, user_id)
            if setting_[user_id]['use'] == False:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
            if setting_[user_id]['use'] == True:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount2, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
       	elif set_ == 0:
            set_ = 1
            secs = setting_[user_id]['time']*60-stoptime
            s.restart()
            executer = ThreadPoolExecutor(1)
            executer.submit(count, secs, user_id)
            if setting_[user_id]['use'] == False:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
            if setting_[user_id]['use'] == True:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount2, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
        items = {'items': [{'type': 'action','action': {'type': 'message','label': 'ストップする','text': 'ストップ'}},{'type': 'action','action': {'type': 'message','label': '進行状況を見る','text': '確認'}}]}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='スタートしたよ！\n一時停止したいときは ストップ と言ってね！\n確認 で進行状況が確認できるよ！'))


    if 'ストップ' == msg_text:
        items = {'items': [{'type': 'action','action': {'type': 'message','label': 'スタート','text': 'スタート'}}]}
        if set_ == 1:
        	t1 = s.stop()
        	set_ = 0
        	stoptime = math.floor(t1)
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='スタート で再スタートできるよ！\n残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount_1'],pointcount_2=Time[user_id]['pointcount_2']),quick_reply=items))
            setting_[user_id]['point2'] = Time[user_id]['pointcount_1']
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='スタート で再スタートできるよ！\n残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount2_1'],pointcount_2=Time[user_id]['pointcount2_2']),quick_reply=items))
            setting_[user_id]['point2'] = Time[user_id]['pointcount2_1']

    if '確認' == msg_text:
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount_1'],pointcount_2=Time[user_id]['pointcount_2'])))
            setting_[user_id]['point2'] = Time[user_id]['pointcount_1']
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount2_1'],pointcount_2=Time[user_id]['pointcount2_2'])))
            setting_[user_id]['point2'] = Time[user_id]['pointcount2_1']


    if 'ポイント追加' == msg_text:
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずはやったひとの名前を教えてね！'))
        setting2[user_id]['setting9'] = True
        pdate[user_id] = {'save': True,'date': '','point':'','name':''}


    if 'ポイント削除' == msg_text:
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずはやったひとの名前を教えてね！'))
        setting2[user_id]['setting10'] = True
        pdate[user_id] = {'save': False,'date': '','point':'','name':''}

    if setting2[user_id]['setting9'] == True or setting2[user_id]['setting10'] == True:
        date = msg_text
        if setting2[user_id]['setting9'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}さんがしたんだね！\n\n次はやったことを教えてね！'.format(date=date)))
            pdate[user_id]['name'] = date
            setting2[user_id]['setting9'] = False
            setting2[user_id]['setting5'] = True
        if setting2[user_id]['setting10'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}さんがしたんだね！\n\n次はやったことを教えてね！'.format(date=date)))
            pdate[user_id]['name'] = date
            setting2[user_id]['setting10'] = False
            setting2[user_id]['setting6'] = True


    if setting2[user_id]['setting5'] == True or setting2[user_id]['setting6'] == True:
        date = msg_text
        items = {'items': [{'type': 'action','action': {'type': 'message','label': '5ポイント','text': '5'}},{'type': 'action','action': {'type': 'message','label': '10ポイント','text': '10'}},{'type': 'action','action': {'type': 'message','label': '20ポイント','text': '20'}},{'type': 'action','action': {'type': 'message','label': '50ポイント','text': '50'}}]}
        if setting2[user_id]['setting5'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたんだね！\n\n次は追加するポイントを教えてね！'.format(date=date),quick_reply=items))
            pdate[user_id]['date'] = date
            setting2[user_id]['setting5'] = False
            setting2[user_id]['setting7'] = True
        if setting2[user_id]['setting6'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたんだね！\n\n次は削除するポイントを教えてね！'.format(date=date),quick_reply=items))
            pdate[user_id]['date'] = date
            setting2[user_id]['setting6'] = False
            setting2[user_id]['setting8'] = True

    if setting2[user_id]['setting7'] == True or setting2[user_id]['setting8'] == True:
        point = msg_text
        items = {'items': [{'type': 'action','action': {'type': 'message','label': '今までの記録を確認する','text': '記録確認'}}]}
        if setting2[user_id]['setting7'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたから{point}追加されたよ！\n\n今までの記録は  記録確認  で見れるよ！'.format(date=pdate[user_id]['date'],point=point),quick_reply=items))
            pdate[user_id]['point'] = point
            setting2[user_id]['setting7'] = False
            seve2(user_id,int(point))
            seve3(user_id)
        if setting2[user_id]['setting8'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたから{point}削除したよ！\n\n今までの記録は  記録確認  で見れるよ！'.format(date=pdate[user_id]['date'],point=point),quick_reply=items))
            setting2[user_id]['setting8'] = False
            int_point = int(point)
            point2 = -int_point
            pdate[user_id]['point'] = str(point2)
            seve2(user_id,point2)
            seve3(user_id)


    if '記録確認' == msg_text:
        line_bot_api.reply_message(msg_from,TextSendMessage(text='確認したい人の名前を教えてね！\n[打ち方]　確認:"名前"\n例: たろうくんの場合  確認:たろう'))


    if '確認:' in msg_text:
        name = msg_text.replace("確認:","")
        d = pointcheck(user_id,name)
        list2 = []
        for t in d:
            str_datetime = t[1].strftime('%Y-%m-%d %H:%M:%S')
            list2.append([t[0],str_datetime])
        list3 = []
        for t in list2:
            list3.append(' : '.join(t))
        date_str = '\n\n'.join(list3)
        line_bot_api.reply_message(msg_from,TextSendMessage(text='[今までの記録]\n{date_str}\n今の合計ポイント : {point}'.format(date_str=date_str,point=namecheck(user_id,name))))

    else:
        if setting2[user_id]['setting2'] == True and user_id == setting_[user_id]['ID']:
            print('ok')
            setting2[user_id]['setting2'] = False
            setting2[user_id]['setting3'] = True
            name = msg_text
            setting_[user_id]['name'] = name
            point = namecheck(user_id,name)
            setting_[user_id]['point'] = point
            items = {'items': [{'type': 'action','action': {'type': 'message','label': '10ポイント','text': '10'}},{'type': 'action','action': {'type': 'message','label': '20ポイント','text': '20'}},{'type': 'action','action': {'type': 'message','label': '50ポイント','text': '50'}},{'type': 'action','action': {'type': 'message','label': '100ポイント','text': '100'}}]}
            if setting_[user_id]['use'] == False:
                line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に取得するポイント数を設定してね！'.format(point),quick_reply=items))
            if setting_[user_id]['use'] == True:
                line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に消費するポイント数を設定してね！'.format(point),quick_reply=items))




if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
