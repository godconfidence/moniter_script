#-*-coding:utf-8-*-

from apscheduler.schedulers.blocking import BlockingScheduler
import itchat
import re
import io
# from urllib import quote
# from urllib import *
import requests
import os
import sys
import json
import time
import traceback
import jsonutil
import collections
reload(sys)
sys.setdefaultencoding( "utf8" )
import codecs
sys.stdout = codecs.getwriter('gb18030')(sys.stdout)
import logging

# logger = logging.getLogger('xxx')

# class MoniterChatRooms(object):

# pass


headers = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
    'Accept-Language':
    'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
    'Content-Type':'application/json'
}

#群管理员微信名称
owner_name_global = u'田琪'
json_util = jsonutil.JsonUtil('repeat_user.json')
ignore_owner_name = {'夏至','乌云','仙女','星晴','冬哥','田琪','懒喵','大妮子','黄小林（乐巷）','赵紫琪',
'尼卡','周敏','迎风醉倒','马小','李昱星','阿美','Miss J','你后来没有遇到我','916','包子','丽丽','琳儿',
'中医调理师马鹏飞15857840521','晓逸 Lydia','小长宏'}

# ignore_owner_name = {'班哥静听','班弟静听'}


def log(msg):

    with open('test.txt', 'a') as f:
        f.write(msg+'\n')

pass


def clean_log(filename):
    with open(filename, 'w') as f:
        f.write('')
pass


def check_chatroomname(memberList,now_chatroomname):

    '''
    检查群聊是否改名，并返回相应信息

    params:

    return(
        是否改名，true改名，false没有改名
        信息
    )
    '''

    #通过挂机号获取小区名称
    if len(str(memberList['Self']['DisplayName'])) == 0:
        old_chatroom_name = '挂机号没有设置小区名'
    else:
        old_chatroom_name = memberList['Self']['DisplayName'].split('_')[0]

    if old_chatroom_name == now_chatroomname :
        return (False,'群聊名字没有更改')
    else:
        if old_chatroom_name == '挂机号没有设置小区名':
            # print '群聊:%s,挂机号没有设置小区名' % now_chatroomname
            return (False,'群聊:%s,挂机号没有设置小区名' % now_chatroomname)
        else:
            return (True,'%s可能改名,%s---->%s' % (now_chatroomname,old_chatroom_name,now_chatroomname))

pass


def get_owner(memberList):

    '''
    params:传入群列表

    return(
        管理员code
        管理员微信名称
    )
    '''

    try:

        if memberList.has_key('ChatRoomOwner'):
            # print memberList['ChatRoomOwner']
            owner_code = (str(memberList['ChatRoomOwner']),)
            chatrome_owner_user = itchat.search_friends(userName=memberList['ChatRoomOwner'])
            owner_name = ('not friend',) if chatrome_owner_user is None else (str(chatrome_owner_user['NickName']),)

        else:

            like_owner_user = [ user['UserName'] for user in memberList['MemberList'] if user['NickName']==owner_name_global]
            owner_code = ('none',) if like_owner_user is None or len(like_owner_user) !=1 else (like_owner_user[0],)
            owner_name = (owner_name_global,)

        return owner_code+owner_name

    except Exception as e:
        msg = traceback.format_exc() # 方式1
        print e
        print msg
        return None

pass


def post_db(request_data):

    if(len(request_data)>0):
        url = 'http://cw.diyiba.com/a/group'
        r = requests.post(url=url, headers=headers, data=json.dumps({"data":request_data}),verify=False)  # 最基本的GET请求
        print r.content
    else:
        print u'没有找到信息'

pass


def find_chatroom_users(memberList,char_room_code,char_room_name):


    user_detail_info = []
    user_info = []

    for x in memberList['MemberList']:

        # 记录用户详情
        user_detail_info.append({
            'key': str(x['UserName']),
            'val': str(x['NickName']),
            'char_room_name': char_room_name,
            'char_room_code': char_room_code
        })

        # 为用户hash值创建列表
        if str(x['NickName']) not in ignore_owner_name:
            user_info.append(str(x['UserName']))

        # username = []
        # username.append({'key':str(x['UserName']),'val':str(x['NickName'])})
        # usernames = ','.join(username)

    # json_val = {
    #     'char_room_name':char_room_name,
    #     'char_room_code':char_room_code,
    #     'char_room_users':[
    #         username
    #     ]
    # }

    return (
        user_info,
        user_detail_info,
        # json_val
    )

pass


def extract_repeat_user(chartroonusers_detail,chartroonusers):

    # users = json_util.load()

    extract_repeat = collections.Counter(chartroonusers)

    result_finaly = []
    for u in extract_repeat:

        if int(extract_repeat[u])<=1:
            continue

        tips = []
        user_name =''

        for u_sub in chartroonusers_detail:
            if u_sub['key'] == str(u):
                tips.append(u_sub['char_room_name'])
                user_name=u_sub['val']
        pass

        result_finaly.append('%s潜入了%s个群,群名:%s' % (user_name,extract_repeat[u],','.join(tips)))
        # print u'%s潜入了%s个群,群名:%s' % (user_name,extract_repeat[u],','.join(tips))
    pass

    if result_finaly is not None:
        json_util.add_json(result_finaly)

pass


def refresh_chatroom():

    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    mpsList = itchat.get_chatrooms(update=True)
    login_name = itchat.web_init()['User']['NickName']
    print u'当前登录用户是%s:' % login_name
    print(u'群聊的数目是%d' % len(mpsList))

    clean_log('repeat_user.json')

    #保存群聊信息
    # log(str(mpsList))
    # username = []
    request_data = []
    chartroonusers=[]
    chartroonusers_detail=[]

    for it in mpsList:

        time.sleep(3)
        if it.has_key('NickName')==False or it['NickName'] is None or len(str(it['NickName']))==0:
            continue

        chatroomname = it['NickName']
        # 获取群成员信息
        memberList = itchat.update_chatroom(it['UserName'])
        # 保存用户列表
        build_user_info=find_chatroom_users(memberList,it['UserName'],chatroomname)
        chartroonusers[0:0] = build_user_info[0] #等价于user_info.extend(build_user_info[1])
        chartroonusers_detail[0:0] = build_user_info[1]
        # json_util.add_json(build_user_info[2])
        # 获取管理员信息
        owner_info = get_owner(memberList)

        group_info = {
            "groupName":chatroomname,
            "counts":len(memberList['MemberList']),
            "groupManager":owner_info[1]
        }
        request_data.append(group_info)

        print u'群:%s,管理员为:%s,群聊人数为:%s ' % (chatroomname,owner_info[1],str(len(memberList['MemberList'])) )

    pass

    post_db(request_data)
    extract_repeat_user(chartroonusers_detail,chartroonusers)

pass


def start_job():

    scheduler = BlockingScheduler()
    # scheduler.add_job(refresh_chatroom, 'cron', year=2017,month = 03,day = 22,hour = 17,minute = 19,second = 07)
    scheduler.add_job(refresh_chatroom,'cron', minute='*/30', hour='*')
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

pass

def send_msg(text,desp):
    url = 'https://sc.ftqq.com/SCU10123T7fde81daf99c2f27874195d8bee93c6b596aca72e162d.send?text=%s&desp=%s' % (text,desp)
    requests.get(url=url)
pass

def log_out():
    print 'asdf'
    # user = itchat.search_friends(name='班哥静听')
    # print user
    # itchat.send_msg(msg='Test Message')
pass

def main():

    #获取群人数、重复人数
    # clean_log()
    pkl_name = 'test'
    print u'稍等，群聊人数多会比较慢......'
    logging.info('aaaaa')
    itchat.auto_login(enableCmdQR=False, hotReload=True,statusStorageDir=pkl_name+'.pkl',exitCallback=log_out)

    #显示所有的群聊，包括未保存在通讯录中的，如果去掉则只是显示在通讯录中保存的
    # itchat.dump_login_status()

    #开启心跳包
    # itchat.start_receiving(exitCallback=log_out)

    # start_job()

    itchat.run()

pass

if __name__ == '__main__':
    main()

# ===========================单个群聊调用接口===============================#
# data = {
#     "data":{
#         "counts":len(memberList['MemberList']),
#         "groupManager":owner_name
#     }
# }
# url = 'http://cw.diyiba.com/a/%s' % (it['NickName'])
# r = requests.post(url=url, headers=headers, data=json.dumps(data),verify=False)  # 最基本的GET请求
# print r.content
# ===========================单个群聊调用接口===============================#


# ===========================检查群聊是否改名，并返回相应信息==============================
# 检查群聊是否改名，并返回相应信息
# check_chatroomname_info = check_chatroomname(memberList,chatroomname)
# if check_chatroomname_info[0]:
# 如果群聊改名则通知管理员
# if owner_info[0] != 'none':
# itchat.send_msg(check_chatroomname_info[1],owner_info[0])
# else:
# print u'没有找到群管理员'

# print check_chatroomname_info[1]
# else:
# pass
# ===========================检查群聊是否改名，并返回相应信息==============================
