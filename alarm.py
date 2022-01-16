import datetime
import threading
import time

t=datetime.datetime.now()
print(t.hour, t.minute, t.second)

alarm_list = ["3:25","3:26","3:27"]


hour = 15
minute = 35

def alarm_start(hour,minute):

    print("Alarm Set!")
    wait = True
    while wait == True:
        t = datetime.datetime.now()
        if t.hour == hour and t.minute == minute:
            print("Time to get up")
            wait = False


th = threading.Thread(target=alarm_start,args=[hour,minute])
th.start()

for i in range(5):
   print('Hi from Main Thread')
   time.sleep(1)

th.join()







