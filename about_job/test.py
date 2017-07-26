#-*-coding:utf-8-*-

# 安装步骤
# Pip install apscheduler==3.0.3

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import os
import logging
# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)

def log(msg):

    with open('test.txt', 'a') as f:
        f.write(msg+'\n')
pass

def tick():
    # log('Tick! The time is: %s' % datetime.now())
    # print('Sleep! The time is: %s' % datetime.now())
    # time.sleep(6)
    print('Tick! The time is: %s' % datetime.now())
pass


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(tick,'cron',second='*/3', hour='*')    
    scheduler.add_job(tick,'cron',second='*/2', hour='*')    
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown() 

pass

# scheduler = BlockingScheduler()
# @scheduler.scheduled_job('interval', seconds=3)
# def my_job():
#      print('Dada! The time is: %s' % datetime.now())
# pass

def main2():
    scheduler.start()
pass


def main5():

    scheduler = BlockingScheduler()
    #如果有多个任务序列的话可以给每个任务设置ID号，可以根据ID号选择清除对象，且remove放到start前才有效
    sched.add_job(myfunc, 'interval', seconds=2, id='my_job_id')
    sched.remove_job('my_job_id')

pass


def mian3():

    job = sched.add_job(my_job, 'interval', seconds=2 ,id='123')
    print sched.get_job(job_id='123')
    print sched.get_jobs()

pass


def main4():
    sched.shutdown()
    sched.shutdown(wait=False)
pass


if __name__ == '__main__':
    main()