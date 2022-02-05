#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from bs4 import BeautifulSoup
import requests
import json

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    print(r.status_code)
    return r.status_code


# 你要傳送的訊息內容
response = requests.get("https://sdsql.iottalk.tw/demo/datas/bao1?limit=2&token=bao1")
print(response.json())
message= json.dumps(response.json())
# 將剛剛複製下來的Token取代以下''中的內容即可
token = 'DzzSaeYbqY2W3H5RaCFt2JNi1Ld3f3p707ci0AvkaRn'
lineNotifyMessage(token, message)

token = '7QyeLrwmlZhQnutG6hijKkps0kYDqMBYmhsM05GeqQk'
lineNotifyMessage(token, message)

token = 'EooumEM2JGSrp5o7XFktmO6edXh6dQwzSkCF2b2Esuu'
lineNotifyMessage(token, message)
