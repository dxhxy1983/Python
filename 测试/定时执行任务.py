#encoding=utf-8
from datetime import datetime
import time
import schedule
def job1(*args):    
    with open('tasks', 'a') as f:        
        f.write('[{}]{}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), 'msg'))# 每隔5秒执行一次job1
schedule.every(5).seconds.do(job1)# 每天9:30执行任务
schedule.every().day.at('09:30').do(job1)
if __name__ == '__main__':    
    while True:        
        schedule.run_pending()        
        