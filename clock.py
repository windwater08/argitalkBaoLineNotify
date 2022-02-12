from apscheduler.schedulers.blocking import BlockingScheduler
#import datetime
import urllib
import urllib.request
from datetime import datetime,timezone,timedelta

sched = BlockingScheduler()

@sched.scheduled_job('cron', minute='*/29')
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
    
sched.start()