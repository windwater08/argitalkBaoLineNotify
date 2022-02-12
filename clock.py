from apscheduler.schedulers.blocking import BlockingScheduler
#import datetime
import urllib
import urllib.request
from datetime import datetime,timezone,timedelta
import requests
import json
import time
import math
import threading
from flask import Flask

sqllimit = "12960"
#sqllimitint = int("12960")
#sqllimit = "2"

DataDict = {}
DataDict["field"] = ["南庄農場","富良田農場"]
DataDict["token"] = ["ZTe5KnneRuHVnY1Nx7BcejgaD55Fd2sCmOypAdbA0NW","U1LK4sv4fpcjsnSIqqSlO2GPlnyVvTo9Rz9BTQXZpax"]
DataDict["url"] = ["https://sql.iottalk.tw/api/demo/datas/NanM21?limit="+sqllimit+"&token=4ce2db7c-ce27-43fe-b99b-e52d09c15c1f",
                  "https://dash1.iottalk.tw/demo/datas/FuLiangTian_M2?limit="+sqllimit+"&token=FuLiangTian_M2"]
DataDict["Ovum"] = [1,0]

sched = BlockingScheduler()

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    print(r.status_code)    
    return r.status_code

def lineNotifyJob():
    for i in range(0, len(DataDict["field"])):
        token = DataDict["token"][i];
        # 你要傳送的訊息內容
        #response = requests.get("https://sdsql.iottalk.tw/demo/datas/bao1?limit="+sqllimit+"&token=bao1")
        #response = requests.get("https://sql.iottalk.tw/api/demo/datas/NanM21?limit="+sqllimit+"&token=4ce2db7c-ce27-43fe-b99b-e52d09c15c1f")
        response = requests.get(DataDict["url"][i])
        #print(response.json())
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        messagejson= json.dumps(response.json())
        messagejson= response.json()
        """
        message="提醒您當前" + DataDict["field"][i] + "感測資訊如下： \n"
        for key in messagejson:
            
            if key == "Ovum-O":
                continue
            if key == "Spore-O":
                continue
            if len(messagejson[key]) ==0:
                continue
            message= (message + "時間: " + messagejson[key][0][0] + 
            ", 項目: " + key + 
            ", 數值: " + str(messagejson[key][0][1]) + ", \n")
        
        lineNotifyMessage(token, message)
        
        time.sleep(5)
        """
        message="提醒您當前" + DataDict["field"][i] + "， \n"
        for key in messagejson:
            totalvaluemean =0.0
            if DataDict["Ovum"][i] == 1:
                if key == "Ovum-O":
                    if len(messagejson[key]) == 0:
                        continue
                    for value in messagejson[key]:
                        totalvaluemean = totalvaluemean + value[1]
                    totalvaluemean = totalvaluemean/int(sqllimit)
                    #print(totalvaluemean)
                    if(totalvaluemean < 80.0):
                        message= (message + "蟲害可能發生率 (%): " + '%.4f'%totalvaluemean + ", \n")
                    else:
                        message= (message + "蟲害可能發生率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意, \n")
                if key == "Spore-O":
                    if len(messagejson[key]) == 0:
                        continue
                    for value in messagejson[key]:
                        totalvaluemean = totalvaluemean + value[1]
                    totalvaluemean = totalvaluemean/int(sqllimit)
                    #print(totalvaluemean)
                    if(totalvaluemean < 80.0):
                        message= (message + "病害可能發生率 (%): " + '%.4f'%totalvaluemean + ", \n")
                    else:
                        message= (message + "病害可能發生率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意。 \n")
            elif DataDict["Ovum"][i] == 0:
                if key == "Temperature-O":
                    if len(messagejson["Temperature-O"]) != int(sqllimit):
                        continue
                    if len(messagejson["Humidity-O"]) != int(sqllimit):
                        continue
                    for j in range(0, len(messagejson[key])):
                        temperature  = messagejson["Temperature-O"][j][1]
                        humidity = messagejson["Humidity-O"][j][1]
                        humidity = humidity/100
                        FT = -0.0625*temperature**3+2.9974*temperature**2-37.865*temperature+141.68
                        FH = 316.88*humidity-216.88
                        FT =FT/100
                        FH =FH/100
                        FO =FT*FH*100
                        totalvaluemean = totalvaluemean + FO
                    totalvaluemean = totalvaluemean/int(sqllimit)
                    #print(totalvaluemean)
                    if(totalvaluemean < 80.0):
                        message= (message + "蟲害可能發生率 (%): " + '%.4f'%totalvaluemean + ", \n")
                    else:
                        message= (message + "蟲害可能發生率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意, \n")
                
        lineNotifyMessage(token, message)

@sched.scheduled_job('cron', minute='*/30')
def scheduled_job():
    print('========== APScheduler CRON =========')
    # 馬上讓我們瞧瞧
    print('This job runs every day */30 min.')
    # 利用datetime查詢時間
    #print(f'{datetime.datetime.now().ctime()}')
    print(f'{datetime.now().ctime()}')
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    #print('UTC \t%s\nUTC+8\t%s'%(dt1,dt2))
    #print(dt2.strftime("%Y-%m-%d %H:%M:%S")) # 將時間轉換為 string
    print('========== APScheduler CRON =========')
    url = "https://argitalklinenotify.herokuapp.com/"
    conn = urllib.request.urlopen(url)
    lineNotifyJob()
    
scheduled_job()
sched.start()