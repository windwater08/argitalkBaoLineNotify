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
    response = requests.get("https://sdsql.iottalk.tw/demo/datas/bao1?limit="+sqllimit+"&token=bao1")
    #print(response.json())
    messagejson= json.dumps(response.json())
    messagejson= response.json()
    """
    message="交大寶山農場, 當前資訊如下"
    for key in messagejson:
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
    """
    message="交大寶山農場, 最近72小時的平均資訊如下"
    for key in messagejson:
        totalvaluemean =0.0
        for value in messagejson[key]:
            totalvaluemean = totalvaluemean + value[1]
        totalvaluemean = totalvaluemean/int(sqllimit)
        #print(totalvaluemean)
        message= (message + ", 感測內容: " + key + 
        ", 感測數值: " + '%.4f'%totalvaluemean + ",\n")
    token = '7QyeLrwmlZhQnutG6hijKkps0kYDqMBYmhsM05GeqQk'
    lineNotifyMessage(token, message)
    
    
    time.sleep(3600)