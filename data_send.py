import schedule
import time
import datetime
]
    
schedule.every(30).seconds.do()

while True:
    if datetime.datetime.now().strftime("%H:%M") == '08:55':
        print(True)
    schedule.run_pending()
    time.sleep(1)