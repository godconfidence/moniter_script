#-*-coding:utf-8-*-

from apscheduler.schedulers.blocking import BlockingScheduler
import itchat
import re
import io
import requests
import os
import sys
import json
import time
import datetime
import traceback
import jsonutil
import collections
import random
reload(sys)
sys.setdefaultencoding( "utf8" )
import codecs
sys.stdout = codecs.getwriter('gb18030')(sys.stdout)
import logging
import logging.config
import ConfigParser

class MoniterChatRooms(object):

    def __init__(self,pkl_name):

        '''
        初始化
        '''

        # file = sys.path[0]+r'\app.conf'
        file = 'app.conf'
        if os.path.exists(file):
            self.cp = ConfigParser.SafeConfigParser()
            self.cp.read(file)
            # with codecs.open(file, 'r', encoding='utf-8') as f:
            #     cp.readfp(f)
        else:
            raise Exception('not app.conf')

        self.pkl = pkl_name

        if pkl_name is None or len(pkl_name)==0:
            raise Exception('请传入session文件名')

        if self.cp.has_section(self.pkl) == False:
            raise Exception('配置文件缺失')

        if self.cp.has_option('DEFAULT','enableCmdQR') == False or self.cp.has_option(self.pkl,'owner_name') == False or self.cp.has_option(self.pkl,'ignore_owner_name') == False or self.cp.has_option(self.pkl,'talk_user') == False:
            raise Exception('配置文件缺失')

        print 'Init...'

        #显示所有的群聊，包括未保存在通讯录中的，如果去掉则只是显示在通讯录中保存的
        # itchat.dump_login_status()
        # itchat.start_receiving()

        itchat.auto_login(
            enableCmdQR=bool(self.cp.get('DEFAULT', 'enableCmdQR')),
            hotReload=True,
            statusStorageDir=pkl_name + '.pkl',
            exitCallback=self.log_out)

        self.headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
            'Accept-Language':
            'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Content-Type':'application/json'
        }

        self.scheduler = BlockingScheduler()

        #群管理员微信名称
        self.repeat_user_json_filename = self.pkl+'.json'
        self.owner_name_global = self.cp.get(self.pkl,'owner_name')
        self.json_util = jsonutil.JsonUtil(self.repeat_user_json_filename)
        self.ignore_owner_name = self.cp.get(self.pkl,'ignore_owner_name').split(',')
        self.talk_user = self.cp.get(self.pkl,'talk_user').split(',')
        logging.config.fileConfig("logger.conf")
        self.logger = logging.getLogger('commLogger')

    pass


    def log_out(self):

        # 默认情况下调度器会等待所有正在运行的作业完成后，关闭所有的调度器和作业存储。如果你不想等待，可以将wait选项设置为False。
        if self.scheduler.running == True:
            self.scheduler.shutdown(wait=False)

        # self.scheduler.get_job(job_id='xxx')
        # self.scheduler.get_jobs()
        # self.scheduler.remove_job(job_id='xxx')
        # self.scheduler.remove_all_jobs()

        text = self.pkl + ':退出登录'
        desp = str(datetime.datetime.now()) +':' +self.pkl + ':退出登录'
        url = 'https://sc.ftqq.com/%s.send?text=%s&desp=%s' % (self.cp.get('serverchan','key'), text,desp)
        requests.get(url=url)

    pass


    def clean_log(self,filename):
        with open(filename, 'w') as f:
            f.write('')
    pass


    def check_chatroomname(self,memberList,now_chatroomname):

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


    def get_owner(self,memberList):

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

                like_owner_user = [ user['UserName'] for user in memberList['MemberList'] if user['NickName']==self.owner_name_global]
                owner_code = ('none',) if like_owner_user is None or len(like_owner_user) !=1 else (like_owner_user[0],)
                owner_name = (self.owner_name_global,)

            return owner_code+owner_name

        except Exception as e:
            msg = traceback.format_exc() # 方式1
            print e
            print msg
            return None

    pass


    def post_db(self,request_data):

        if(len(request_data)>0):
            url = 'http://cw.diyiba.com/a/group'
            r = requests.post(url=url, headers=self.headers, data=json.dumps({"data":request_data}),verify=False)  # 最基本的GET请求
            print r.content
        else:
            print u'没有找到信息'

    pass


    def find_chatroom_users(self,memberList,char_room_code,char_room_name):

        '''
        解析群信息，保存群聊中所有用户hashcode、用户详细信息

        param:memberList(itchat返回的群聊用户)
        param:char_room_code(群聊hashcode)
        param:char_room_name(群聊名称)

        return:(
            user_info(用户hashcode),
            user_detail_info(用户详细信息)
        )
        '''

        user_info = []
        user_detail_info = []

        for x in memberList['MemberList']:

            # 记录用户详情
            user_detail_info.append({
                'key': str(x['UserName']),
                'val': str(x['NickName']),
                'char_room_name': char_room_name,
                'char_room_code': char_room_code
            })

            # 为用户hash值创建列表
            if str(x['NickName']) not in self.ignore_owner_name:
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


    def extract_repeat_user(self,chartroomusers_detail,chartroomusers):

        '''
        提取重复入群的用户

        param:chartroomusers_detail(所有用户信息)
        param:chartroomusers(所有用户hashcode)

        写入json文件
        '''

        # 统计出重复项和重复数量
        extract_repeat = collections.Counter(chartroomusers)

        result_finaly = []
        for u in extract_repeat:

            if int(extract_repeat[u])<=1:
                continue

            tips = []
            user_name =''

            for u_sub in chartroomusers_detail:
                if u_sub['key'] == str(u):
                    tips.append(u_sub['char_room_name'])
                    user_name=u_sub['val']
            pass

            result_finaly.append('%s潜入了%s个群,群名:%s' % (user_name,extract_repeat[u],','.join(tips)))
            # print u'%s潜入了%s个群,群名:%s' % (user_name,extract_repeat[u],','.join(tips))
        pass

        if result_finaly is not None:
            self.json_util.add_json(result_finaly)

    pass


    def talk(self):

        '''
        随机找好友聊天
        '''

        try:

            # 找到好友聊天
            # random.uniform(0,len(self.ignore_owner_name))
            user_index = random.randint(0,len(self.talk_user)-1)
            select_user = self.talk_user[user_index]
            # print select_user
            talk_user = itchat.search_friends(name=select_user)
            if talk_user is not None and len(talk_user)>0:
                print 'talk about...'
                # 获取聊天内容
                itchat.send_msg(msg='Hello'+talk_user[0]['NickName'],toUserName=talk_user[0]['UserName'])
            else:
                # print 'not found user'
                self.talk()

        except Exception,e:
            msg = traceback.format_exc() # 方式1
            print e
            print msg
            self.logger.error('talk error',exc_info=True)

    pass


    def refresh_chatroom(self):

        '''
        刷新微信群信息(统计群人数、统计重复入群)
        '''

        try:

            self.logger.info('同步群聊人数')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            mpsList = itchat.get_chatrooms(update=True)
            login_name = itchat.web_init()['User']['NickName']
            print u'当前登录用户是%s:' % login_name
            print(u'群聊的数目是%d' % len(mpsList))

            self.clean_log(self.repeat_user_json_filename)

            #保存群聊信息
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
                build_user_info = self.find_chatroom_users(memberList,it['UserName'],chatroomname)
                chartroonusers[0:0] = build_user_info[0] #等价于user_info.extend(build_user_info[1])
                chartroonusers_detail[0:0] = build_user_info[1]
                # self.all_users.add_json(build_user_info[2])

                # 获取管理员信息
                owner_info = self.get_owner(memberList)

                group_info = {
                    "groupName":chatroomname,
                    "counts":len(memberList['MemberList']),
                    "groupManager":owner_info[1]
                }
                request_data.append(group_info)

                print u'群:%s,管理员为:%s,群聊人数为:%s ' % (chatroomname,owner_info[1],str(len(memberList['MemberList'])) )

            pass

            self.post_db(request_data)
            self.extract_repeat_user(chartroonusers_detail,chartroonusers)

        except Exception as e:
            msg = traceback.format_exc() # 方式1
            self.logger.error('刷新微信群聊出错',exc_info=True)

    pass


    def endWith(self,*endstring):

        ends = endstring
        def run(s):
            f = map(s.endswith,ends)
            if True in f: return s
        return run
    pass


    def start_job(self):

        '''
        创建并开始job
        '''

        # list_file = os.listdir(sys.path[0])
        # a = endWith('.pkl')
        # f_file = filter(a,list_file)
        # for i in f_file: print i,

        print 'Start moniter job...'
        # sync_hour = 0
        # if self.cp.has_option(self.pkl,'sync_hour'):
        #     sync_hour = self.cp.get(self.pkl,'sync_hour')

        # scheduler.add_job(self.fixed_time_refresh,'cron',year=2017,month = 07,day = 24,hour = 16,minute = 17,second = 57)
        self.scheduler.add_job(self.refresh_chatroom,'cron',hour='0',id=self.pkl+'_refresh_chatroom')
        self.scheduler.add_job(self.talk,'cron', minute='*/30', hour='*',id=self.pkl+'_talk')

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    pass

pass


def main():

    if len(sys.argv) == 1:
        print u'请输入保存的session文件名'
        return

    try:

        moniter_chatroom = MoniterChatRooms(sys.argv[1])
        moniter_chatroom.start_job()

    except Exception as e:
        msg = traceback.format_exc() # 方式1
        print e
        print msg

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
