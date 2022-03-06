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

DataDict["field"] = ["南庄農場","富良田農場","花壇鄉"]
DataDict["token"] = ["ZTe5KnneRuHVnY1Nx7BcejgaD55Fd2sCmOypAdbA0NW","U1LK4sv4fpcjsnSIqqSlO2GPlnyVvTo9Rz9BTQXZpax","uzxo3DCpZa8vEOkEieZ7oZQSmUNVZl4Rz3UpRV5LlU1"]
DataDict["url"] = ["https://sql.iottalk.tw/api/demo/datas/NanM21?limit="+sqllimit+"&token=4ce2db7c-ce27-43fe-b99b-e52d09c15c1f",
                  "https://dash1.iottalk.tw/demo/datas/FuLiangTian_M2?limit="+sqllimit+"&token=FuLiangTian_M2",
                  "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-017?Authorization=CWB-8537B68D-F394-4E1E-809B-2E347389BDFB&limit=1&format=JSON&locationName=%E8%8A%B1%E5%A3%87%E9%84%89&elementName=T,RH&sort=time&timeFrom="]
DataDict["Ovum"] = [0,1,2]
DataDict["Spore"] = [0,1,2]
"""
DataDict["field"] = ["花壇鄉"]
DataDict["token"] = ["uzxo3DCpZa8vEOkEieZ7oZQSmUNVZl4Rz3UpRV5LlU1"]
DataDict["url"] = ["https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-017?Authorization=CWB-8537B68D-F394-4E1E-809B-2E347389BDFB&limit=1&format=JSON&locationName=%E8%8A%B1%E5%A3%87%E9%84%89&elementName=T,RH&sort=time&timeFrom="]
DataDict["Ovum"] = [2]
DataDict["Spore"] = [2]
"""
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

def lineNotifyJob(field):

#for index in range(0, len(DataDict["field"])):
    index = DataDict["field"].index(field)
    nowtime = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    compartime = nowtime.strftime("%Y-%m-%d %H:%M:%S")
    nowtime = nowtime.strftime("%Y-%m-%dT%H:%M:%S")
    print(nowtime)
    token = DataDict["token"][index];
    # 你要傳送的訊息內容
    #response = requests.get("https://sdsql.iottalk.tw/demo/datas/bao1?limit="+sqllimit+"&token=bao1")
    #response = requests.get("https://sql.iottalk.tw/api/demo/datas/NanM21?limit="+sqllimit+"&token=4ce2db7c-ce27-43fe-b99b-e52d09c15c1f")
    if(DataDict["Ovum"][index] != 2):
        response = requests.get(DataDict["url"][index])
    else:
        response = requests.get(DataDict["url"][index]+nowtime)
    #print(response.json())

    messagejson= json.dumps(response.json())
    messagejson= response.json()
    """
    message="提醒您當前" + DataDict["field"][index] + "感測資訊如下： \n"
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
    message="提醒您當前" + DataDict["field"][index] + "， \n"
    for key in messagejson:
        totalvaluemean =0.0
        if DataDict["Spore"][index] == 0:
            if key == "Ovum-O":
                if len(messagejson[key]) == 0:
                    continue
                for value in messagejson[key]:
                    totalvaluemean = totalvaluemean + value[1]
                totalvaluemean = totalvaluemean/int(sqllimit)
                #print(totalvaluemean)
                if(totalvaluemean < 80.0):
                    message= (message + "蟲害可能發生率 (%): " + '%.4f'%totalvaluemean + "。 \n")
                else:
                    message= (message + "蟲害可能發生率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意。 \n")
            if key == "Spore-O":
                if len(messagejson[key]) == 0:
                    continue
                for value in messagejson[key]:
                    totalvaluemean = totalvaluemean + value[1]
                totalvaluemean = totalvaluemean/int(sqllimit)
                #print(totalvaluemean)
                if(totalvaluemean < 80.0):
                    message= (message + "病害可能發生率 (%): " + '%.4f'%totalvaluemean + "。 \n")
                else:
                    message= (message + "病害可能發生率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意。 \n")
        elif DataDict["Spore"][index] == 1:
            if key == "Temperature-O":
                if len(messagejson["Temperature-O"]) != int(sqllimit):
                    continue
                if len(messagejson["Humidity-O"]) != int(sqllimit):
                    continue
                for j in range(0, len(messagejson[key])):
                    temperature  = messagejson["Temperature-O"][j][1]
                    humidity = messagejson["Humidity-O"][j][1]
                    humidity = humidity/100
                    FT = -0.0078*temperature**3+0.2806*temperature**2+1.6665*temperature+0.27
                    FH = 0.1143*math.exp(6.6027*humidity)
                    FT =FT/100
                    FH =FH/100
                    FO =FT*FH*100
                    totalvaluemean = totalvaluemean + FO
                totalvaluemean = totalvaluemean/int(sqllimit)
                #print(totalvaluemean)
                if(totalvaluemean < 80.0):
                    message= (message + "病害可能發生率 (%): " + '%.4f'%totalvaluemean + "。 \n")
                else:
                    message= (message + "病害可能發生率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意。 \n")
        elif DataDict["Spore"][index] == 2:
            i = 0
            if key == "records":
                #print('messagejson["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][0]["elementValue"][0]["value"]:'+
                #        json.dumps(messagejson["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][0]["elementValue"][0]["value"]))
                #print('messagejson["records"]["locations"][0]["location"]["weatherElement"]:'+messagejson["records"]["locations"][0]["location"]["weatherElement"])
                print(DataDict["url"][index]+nowtime)
                predictdateline = messagejson["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][i]["dataTime"]
                if time.mktime(datetime.strptime(compartime, "%Y-%m-%d %H:%M:%S").timetuple()) >= time.mktime(datetime.strptime(predictdateline, "%Y-%m-%d %H:%M:%S").timetuple()):
                    print("in time if")
                    i = i+1
                    predictdateline = messagejson["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][i]["dataTime"]
                temperature  = messagejson["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][i]["elementValue"][0]["value"]
                temperature = int(temperature);
                humidity = messagejson["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"][i]["elementValue"][0]["value"]
                humidity = int(humidity);
                humidity = humidity/100
                FT = -0.0078*temperature**3+0.2806*temperature**2+1.6665*temperature+0.27
                FH = 0.1143*math.exp(6.6027*humidity)
                FT =FT/100
                FH =FH/100
                FO =FT*FH*100
                
                print('預報時間:'+predictdateline)
                print('temperature:'+str(temperature))
                print('humidity:'+str(humidity))
                print('FO:'+str(FO))
                if(FO < 80.0):
                    message= (message + "預計病害可能發生率 (%): " + '%.4f'%FO + ", \n")
                else:
                    message= (message + "預計病害可能發生率 (%): " + '%.4f'%FO + ", 已經越過安全值請注意, \n")
                message = message + "本預報有效期間至" + predictdateline + "為止。"
    lineNotifyMessage(token, message)

@sched.scheduled_job('cron', minute='*/15')
def scheduled_job():
    print('========== APScheduler CRON =========')
    # 馬上讓我們瞧瞧
    print('This job runs every day */15 min.')
    # 利用datetime查詢時間
    #print(f'{datetime.datetime.now().ctime()}')
    #print(f'{datetime.now().ctime()}')
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    #print('UTC \t%s\nUTC+8\t%s'%(dt1,dt2))
    print(dt2.strftime("%Y-%m-%d %H:%M:%S")) # 將時間轉換為 string
    print('========== APScheduler CRON =========')
    url = "https://argitalklinenotify.herokuapp.com/"
    conn = urllib.request.urlopen(url)
    hour   = dt2.hour
    minute = dt2.minute
    if hour==8 and minute < 15:
        lineNotifyJob("南庄農場")
        lineNotifyJob("富良田農場")
    if hour==20 and minute < 15:
        lineNotifyJob("南庄農場")
        lineNotifyJob("富良田農場")
    if (hour % 3 == 0) and minute < 15:
        lineNotifyJob("花壇鄉")
    
#lineNotifyJob("花壇鄉")
scheduled_job()
sched.start()