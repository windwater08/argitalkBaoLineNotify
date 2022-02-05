#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import time

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    print(r.status_code)    
    return r.status_code

sqllimit = "12960"
#sqllimit = "2"
while 1: 

    # 你要傳送的訊息內容
    #response = requests.get("https://sdsql.iottalk.tw/demo/datas/bao1?limit="+sqllimit+"&token=bao1")
    response = requests.get("https://sql.iottalk.tw/api/demo/datas/NanM21?limit="+sqllimit+"&token=4ce2db7c-ce27-43fe-b99b-e52d09c15c1f")
    
    #print(response.json())
    messagejson= json.dumps(response.json())
    messagejson= response.json()
    
    message="南庄農場, 當前資訊如下"
    for key in messagejson:
        
        if key == "Ovum-O":
            continue
        if key == "Spore-O":
            continue
        if len(messagejson[key]) ==0:
            continue
        message= (message + ", 感測時間: " + messagejson[key][0][0] + 
        ", 感測內容: " + key + 
        ", 感測數值: " + str(messagejson[key][0][1]) + ",\n")
    
    #token = 'DzzSaeYbqY2W3H5RaCFt2JNi1Ld3f3p707ci0AvkaRn'
    #lineNotifyMessage(token, message)
    
    token = '7QyeLrwmlZhQnutG6hijKkps0kYDqMBYmhsM05GeqQk'
    lineNotifyMessage(token, message)
    
    #token = 'EooumEM2JGSrp5o7XFktmO6edXh6dQwzSkCF2b2Esuu'
    #lineNotifyMessage(token, message)
    
    time.sleep(5)
    
    message="南庄農場, 最近72小時的平均資訊如下"
    for key in messagejson:
        totalvaluemean =0.0
        if key == "Ovum-O":
            if len(messagejson[key]) ==0:
                continue
            for value in messagejson[key]:
                totalvaluemean = totalvaluemean + value[1]
            totalvaluemean = totalvaluemean/int(sqllimit)
            #print(totalvaluemean)
            if(totalvaluemean < 80.0):
                message= (message + ", 卵孵化率 (%): " + '%.4f'%totalvaluemean + ", 為安全值 \n")
            else:
                message= (message + ", 卵孵化率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意 \n")
        if key == "Spore-O":
            if len(messagejson[key]) ==0:
                continue
            for value in messagejson[key]:
                totalvaluemean = totalvaluemean + value[1]
            totalvaluemean = totalvaluemean/int(sqllimit)
            #print(totalvaluemean)
            if(totalvaluemean < 80.0):
                message= (message + ", 孢子發芽率 (%): " + '%.4f'%totalvaluemean + ", 為安全值 \n")
            else:
                message= (message + ", 孢子發芽率 (%): " + '%.4f'%totalvaluemean + ", 已經越過安全值請注意 \n")
        

    token = '7QyeLrwmlZhQnutG6hijKkps0kYDqMBYmhsM05GeqQk'
    lineNotifyMessage(token, message)
    
    
    time.sleep(3600)