#import sqlite3
import pymysql
import re
import json
from datetime import date

def is_regular(_strs):
    p = re.compile('SELECT|UPDATE|UNION|DELETE|INSERT|WHERE|HAVING|OR|COMMIT', re.I)
    for _ in _strs:
        if p.search(_) != None:
            return False
    else:
        return True

class DB:
    def __init__(self):
        self.__init()

    def __del__(self):
        self.__close()

    ##########################################################################################################
    ## private functions 
    ##########################################################################################################
    def __init(self):
        self.db = None
        self.db_name = ""
    
    #def __connect(self, name):
    def __connect(self, isDict):
        while True:
            if self.db == None:
                self.db = pymysql.connect(
                    host= '35.229.221.45',
                    port=3306,
                    user='root',
                    passwd='alsl1203',
                    db='RECORDS',
                    charset='utf8'
                )
                self.cur = self.db.cursor(pymysql.cursors.DictCursor)

                return True
    
    def __close(self):
        if self.db != None:
            self.db.close()
            self.__init()
    
    ##########################################################################################################
    ## public functions
    ##########################################################################################################
    def get_users(self):
        _datas = []
        try:
            self.__connect(False)
            self.cur.execute("select * from user;")
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas
    
    def get_today_record(self):
        _datas = []
        try:
            self.__connect(True)

            today = str(date.today())
            today = int(today.replace('-', ''))

            self.cur.execute("select * from TFM where DATE_TIME between {} and {};".format(today-1, today))
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas