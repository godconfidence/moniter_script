#-*-coding:utf-8-*-

# import itchat
# import re
# from urllib import quote
# from urllib import unquote
import sys
import time
# reload(sys)
# sys.setdefaultencoding( "utf8" )
# import argparse
# from selenium import webdriver
import os
import json
import logging
import logging.config

class Test(object):

    def __init__(self):

        logging.config.fileConfig("logger.conf")
        self.logger = logging.getLogger(__name__)
        # print dir(self.logger.handlers[1].handle)
    pass

    def funcname(self):
        self.logger.debug('This is debug message')
        self.logger.info('This is info message')
        self.logger.warning('This is warning message')
        self.logger.warning('This is warning message2')
    pass
    
    pass

def endWith(*endstring):

    ends = endstring
    def run(s):
            f = map(s.endswith,ends)
            if True in f: return s
    return run

def main():

    test = Test()
    test.funcname()
pass


if __name__ == '__main__':
    # main()
    list_file = os.listdir(sys.path[0])
    a = endWith('.txt','.pkl')
    f_file = filter(a,list_file)
    for i in f_file: print i,


# logging.basicConfig(level=logging.INFO,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='myapp.log',
#                 filemode='a')

# #################################################################################################
# #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
# # console = logging.StreamHandler()
# from logging.handlers import RotatingFileHandler
# #定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
# console = RotatingFileHandler('myappx.log', maxBytes=0,backupCount=5)
# console.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('test').addHandler(console)
# #################################################################################################
