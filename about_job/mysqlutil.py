# -*- coding: utf-8 -*-

import MySQLdb
import sys
import ConfigParser
import os

class MysqlUtil(object):

    def __init__(self):

        file = sys.path[0]+r'\app.conf'
        if os.path.exists(file):
            cp = ConfigParser.SafeConfigParser()
            cp.read(file)

        self.conn = MySQLdb.connect(
            cp.get('db', 'host'),
            cp.get('db', 'user'),
            cp.get('db', 'passwd'), 
            cp.get('db', 'db'), 
            cp.getint('db', 'port')
        )
        self.conn.set_character_set(cp.get('db', 'chartset'))
        self.cur = self.conn.cursor()
    pass


    def select(self,sql):

        #获得表中有多少条数据
        aa = self.cur.execute(sql)
        if aa == 0:
            # self.close()
            return (aa,None)
        else:
            info = self.cur.fetchmany(aa)
            # self.close()
            return (aa,info)

    pass


    def executemany(self,sqli,sql_list):

        self.cur.executemany(sqli, sql_list)
        self.close()

    pass


    def execute_no_query(self,sqli):

        self.cur.execute(sqli)
        self.close()

    pass


    def close(self):

        """
        关闭数据库链接

        """

        try:

            self.cur.close()
            self.conn.commit()
            self.conn.close()

        except Exception as identifier:

            pass
        pass

    pass
