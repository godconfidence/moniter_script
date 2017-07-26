#-*-coding:utf-8-*-

import itchat
import time
from itchat.content import *


newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=True, statusStorageDir='test.pkl')

@newInstance.msg_register([TEXT],isGroupChat=False)
def reply(msg):
    print msg.text
    # return 'aaa'
pass

@newInstance.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # print 'haha'
    # # 消息来自于哪个群聊
    # chatroom_id = msg['FromUserName']
    # # 发送者的昵称
    # username = msg['ActualNickName']
    # print msg
    # print chatroom_id
    # print username
    print msg
 
    # if msg['Type'] == TEXT:
    #     content = msg['Content']
    # elif msg['Type'] == SHARING:
    #     content = msg['Text']
    
    # print content

    # # 根据消息类型转发至其他需要同步消息的群聊
    # if msg['Type'] == TEXT:
    #     for item in chatrooms:
    #         if not item['UserName'] == chatroom_id:
    #             itchat.send('%s\n%s' % (username, msg['Content']), item['UserName'])
    # elif msg['Type'] == SHARING:
    #     for item in chatrooms:
    #         if not item['UserName'] == chatroom_id:
    #             itchat.send('%s\n%s\n%s' % (username, msg['Text'], msg['Url']), item['UserName'])

    # if msg['isAt']:
        # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

# while True:
#     print 'begin'
#     login_name = newInstance.web_init()['User']['NickName']
#     print u'当前登录用户是%s:' % login_name
#     mpsList = newInstance.get_chatrooms(update=True)
#     print(u'群聊的数目是%d' % len(mpsList))
#     time.sleep(5)
#     pass

#开启心跳包
newInstance.start_receiving()
newInstance.run()