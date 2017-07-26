#-*-coding:utf-8-*- 

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )
 
import itchat
from itchat.content import *

# 自动回复文本等类别消息
# isGroupChat=False表示非群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
def text_reply(msg):

    print msg['Text']

    friend = itchat.search_friends(userName= msg['FromUserName'])
    print friend
    chatroom = itchat.search_chatrooms(name=msg['Text'])
    print chatroom
    r = itchat.add_member_into_chatroom(chatroom[0]['UserName'], [friend])
    print r

    # itchat.send('这是我的小号，暂无调戏功能，有事请加我大号：Honlann', msg['FromUserName'])


# 自动处理添加好友申请
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg(u'你好哇', msg['RecommendInfo']['UserName'])


def add_friend(chatroomUserName,friend):

    if r['BaseResponse']['ErrMsg'] == '':
        status = r['MemberList'][0]['MemberStatus']
        itchat.delete_member_from_chatroom(chatroom['UserName'], [friend])
        return { 3: u'该好友已经将你加入黑名单。',
            4: u'该好友已经将你删除。', }.get(status,
            u'该好友仍旧与你是好友关系。')

pass


itchat.auto_login(enableCmdQR=False, hotReload=True)
#开启心跳包
itchat.start_receiving()
itchat.run()
