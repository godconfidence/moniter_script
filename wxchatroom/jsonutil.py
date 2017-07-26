# -*- coding: utf-8 -*-

import json
import os
import time

class JsonUtil(object):

    def __init__(self,filename):

        '''
        初始化filename
        '''

        if filename is None or str(filename)==0:
            raise Exception('filename can not be none')

        self.filename=filename

    pass

    def load(self):

        try:

            with open(self.filename,'r') as json_file:
                data = json.load(json_file)#从文件中序列化
                # json.loads 从内存中序列化
                return data

        except Exception as e:
            # print e
            return None

    pass

    def __store(self,data):

        with open(self.filename, 'w') as f:
            f.write(json.dumps(data,ensure_ascii=False))

    pass

    def add_json(self,val):

        '''
        添加到文件中
        '''
        # print type(val)
        data = self.load()
        if data is None:data = []
        if val is None:
            raise Exception('参数不能为空')
        
        if type(val) is list:
            data[0:0]=val
        else:
            data.append(val)

        self.__store(data)
    pass



pass
