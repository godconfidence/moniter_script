#-*-coding:utf-8-*-

# 安装步骤
# Pip install apscheduler==3.0.3

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import os
import mysqlutil
import requests
import json


def send_msg(text,desp):

    url = 'https://sc.ftqq.com/SCU10123T7fde81daf99c2f27874195d8bee93c6b596aca72e162d.send?text=%s&desp=%s' % (text,desp)
    requests.get(url=url)

pass

def send_img(url):

    content="随机妹子图![pic](%s)" % url
    send_img('图片',content)

pass

def history_task():

    '''
    历史文章任务预警
    '''

    result=[]
    sql_util = mysqlutil.MysqlUtil()

    # 统计活跃客户端
    machine_five_minutes = time.time()-300
    machine_ten_minutes = time.time()-600
    machine_one_hour = time.time()-3600

    sql = "select count(distinct `client_machine`) from wxarticlelog.`pb_crawler_tasklog` where (`type` = 'AN' and `add_time` >= %s)"

    machine_five_minutes_res = sql_util.select(sql % (machine_five_minutes))
    machine_ten_minutes_res = sql_util.select(sql % (machine_ten_minutes))
    machine_one_hour_res = sql_util.select(sql % (machine_one_hour))

    # h1延迟率
    h1_delay_ten_minutes =time.time()-600
    h1_delay_thirty_minutes =time.time()-1800
    h1_delay_one_hour =time.time()-3600

    delay_count_sql = "select count(`id`) from wxarticlelog.`pb_crawler_tasklog` where (`client_type` = 'H1' and `task_pre_dotime` > 0 and `add_time` >= %s) and `task_pre_dotime` - `task_etime` < -60"
    delay_avg_sql = "select AVG(`task_pre_dotime` - `task_etime`) as avgdelay from wxarticlelog.`pb_crawler_tasklog` where (`client_type` = 'H1' and `task_pre_dotime` > 0 and `add_time` >= %s) limit 1"
    # delay_ratio_sql ="select count(`id`) as aggregate from `pb_crawler_tasklog` where (`client_type` = H1 and `task_pre_dotime` > 0 and `add_time` >= 1500257406) and `task_pre_dotime` - `task_etime` < -60"

    h1_delay_ten_minutes_res = sql_util.select(delay_count_sql % (h1_delay_ten_minutes))
    h1_delay_thirty_minutes_res = sql_util.select(delay_count_sql % (h1_delay_thirty_minutes))
    h1_delay_one_hour_res = sql_util.select(delay_count_sql % (h1_delay_one_hour))
    h1_delay_ten_minutes_avg_res = sql_util.select(delay_avg_sql % (h1_delay_ten_minutes))
    h1_delay_thirty_minutes_avg_res = sql_util.select(delay_avg_sql % (h1_delay_thirty_minutes))
    h1_delay_one_hour_avg_res = sql_util.select(delay_avg_sql % (h1_delay_one_hour))

    sql_util.close()

    msg_key = int(h1_delay_ten_minutes_avg_res[1][0][0])
    
    h1_info = {
        "notify_key": "AS文章抓取" if msg_key>0 else "AF文章抓取",
        "notify_value": {
            "A5M活跃数": int(machine_five_minutes_res[1][0][0]),
            "B10M活跃数": int(machine_ten_minutes_res[1][0][0]),
            "C1H活跃数": int(machine_one_hour_res[1][0][0]),
            "D10M延迟数": int(h1_delay_ten_minutes_res[1][0][0]),
            "E30M延迟数": int(h1_delay_thirty_minutes_res[1][0][0]),
            "F1H延迟数": int(h1_delay_one_hour_res[1][0][0]),
            "G10M均值": int(h1_delay_ten_minutes_avg_res[1][0][0]),
            "H30M均值": int(h1_delay_thirty_minutes_avg_res[1][0][0]),
            "I1H均值": int(h1_delay_one_hour_avg_res[1][0][0])
        }
    }

    print('Tick! The time is: %s' % datetime.now())

    return h1_info

pass


def get_notify_data():

    notify_info = []
    notify_info.append(history_task())
    # notify_info.append(xxx_task())

    # sort_keys是否对键值排序
    # 缩进数 优雅的json
    # separators对数据进行压缩
    # http://www.cnblogs.com/dasydong/p/4423345.html
    post_str = json.dumps(notify_info, ensure_ascii = False,sort_keys=True,indent=4,separators=(',',':'))
    # print post_str
    send_msg('历史任务监控',"```json\n\n"+post_str+"\n```")

pass

def test():
    print time.time()
pass

def main():

    scheduler = BlockingScheduler()
    scheduler.add_job(get_notify_data,trigger= 'cron', minute='*/60', hour='*',id='check_h5')
    # scheduler.add_job(test,trigger= 'cron', second='*/10', hour='*',id='check_hxx')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

pass


if __name__ == '__main__':
    main()
