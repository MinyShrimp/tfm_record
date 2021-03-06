#import sqlite3
import pymysql
import re
import json
from datetime import datetime, date, time, timedelta

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
    def __connect(self):
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
    def get_company_names(self):
        _datas = []
        try:
            self.__connect()
            self.cur.execute("select * from TFM_COMPANY;")
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas
    
    def get_company_names_by_name(self, name):
        _datas = []
        try:
            if is_regular([name]) is False:
                raise TypeError

            self.__connect()
            self.cur.execute("select * from TFM_COMPANY where Name like '%{}%';".format(name))
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas
    
    def get_user(self, id):
        _datas = []
        try:
            if is_regular([str(id)]) is False:
                raise TypeError

            self.__connect()
            self.cur.execute("select * from user where ID={};".format(id))
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas
    
    def get_user_by_name(self, name):
        _datas = []
        try:
            if is_regular([name]) is False:
                raise TypeError

            self.__connect()
            self.cur.execute("select * from user where UserName='{}';".format(name))
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas

    def get_users(self):
        _datas = []
        try:
            self.__connect()
            self.cur.execute("select * from user where Amount!=0 ORDER BY AverageRank, AverageScore;")
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas

    def get_users_plus(self):
        _datas = []
        try:
            self.__connect()
            self.cur.execute("select * from user where Amount=0 ORDER BY UserName;")
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas

    def get_user_names(self):
        _datas = []
        try:
            self.__connect()
            self.cur.execute("select ID, UserName from user;")
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas
    
    def get_user_names_by_name(self, name):
        _datas = []
        try:
            if is_regular([name]) is False:
                raise TypeError

            self.__connect()
            self.cur.execute("select ID, UserName from user where UserName like '%{}%';".format(name))
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas
    
    def get_record(self, startT, endT, name, ext, is_sort=False):
        _datas = []
        try:
            self.__connect()
            self.cur.execute("select * from TFM where DATE_TIME between {} and {} and Users like '%{}%' and Extension like '%{}%' AND isDelete=FALSE ORDER BY DATE_TIME {};".format(startT, endT, name, ext, "" if is_sort else "DESC"))
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas
    
    def get_record_by_id(self, id):
        _datas = []
        try:
            self.__connect()
            self.cur.execute("select * from TFM where id={} AND isDelete=FALSE;".format(id))
            _datas = self.cur.fetchall()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return _datas

    def insert_user(self, name):
        try:
            if is_regular([name]) is False:
                print(name)
                raise TypeError
            
            self.__connect()
            self.cur.execute("insert into user (UserName, AverageRank, AverageScore, GenRank, Amount, Rank_1, Rank_2, Rank_3, Rank_4) values ('{}', 0, 0, 0, 0, 0, 0, 0, 0);".format(name))
            self.db.commit()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()

    def insert_imrovements(self, data):
        isSuccess = False
        try:
            _data = """
                {}, '{}', '{}', {}
            """.format(data['uID'], data['uName'], data['Contents'], data['DATE_TIME'])

            if is_regular([_data]) is False:
                print(_data)
                raise TypeError
            
            self.__connect()
            self.cur.execute("insert into Improvements (uID, uName, Contents, DATE_TIME) values ({});".format(_data))
            self.db.commit()

            isSuccess = True
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
        return isSuccess
    
    def insert_record(self, user_datas, extension):
        try:
            _time = int(datetime.now().timestamp())

            data = """
                {}, '{}', {}, {}, '{}', 
                {}, '{}', {}, {}, '{}', 
                {}, '{}', {}, {}, '{}', 
                {}, '{}', {}, {}, '{}', 
                {}, '{}', '{}', '{}', FALSE
            """.format(
                user_datas[0][0], user_datas[0][1], user_datas[0][4], user_datas[0][2], user_datas[0][3], 
                user_datas[1][0], user_datas[1][1], user_datas[1][4], user_datas[1][2], user_datas[1][3], 
                user_datas[2][0], user_datas[2][1], user_datas[2][4], user_datas[2][2], user_datas[2][3], 
                user_datas[3][0], user_datas[3][1], user_datas[3][4], user_datas[3][2], user_datas[3][3], 
                _time, extension, 
                user_datas[0][1]+user_datas[1][1]+user_datas[2][1]+user_datas[3][1],
                user_datas[0][3]+user_datas[1][3]+user_datas[2][3]+user_datas[3][3],
            )

            if is_regular(data) is False:
                print(data)
                raise TypeError
            
            self.__connect()
            self.cur.execute(
                """insert into TFM (
                    UserID_1, UserName_1, Score_1, CompanyID_1, Company_1, 
                    UserID_2, UserName_2, Score_2, CompanyID_2, Company_2, 
                    UserID_3, UserName_3, Score_3, CompanyID_3, Company_3, 
                    UserID_4, UserName_4, Score_4, CompanyID_4, Company_4, 
                    DATE_TIME, Extension, Users, Companys, isDelete
                ) values ({});""".format(data)
            )
            self.db.commit()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()

    def update_user(self, data):
        try:
            tmp = ""
            for _ in list(data.values()):
                tmp += str(_)
            
            if is_regular(tmp) is False:
                print(data)
                raise TypeError

            self.__connect()
            self.cur.execute("""
                UPDATE user 
                SET AverageRank={}, AverageScore={}, Amount={}, Rank_1={}, Rank_2={}, Rank_3={}, Rank_4={}
                where ID={};""".format(data['AverageRank'], data['AverageScore'], data['Amount'], data['Rank_1'], data['Rank_2'], data['Rank_3'], data['Rank_4'], data['ID'])
            )
            self.db.commit()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()
    
    def delete_record(self, id):
        try:
            if is_regular([str(id)]) is False:
                print(id)
                raise TypeError

            self.__connect()
            self.cur.execute("""
                UPDATE TFM 
                SET isDelete=TRUE
                where ID={};""".format(id)
            )
            self.db.commit()
        except Exception as e:
            print("파일 연결 실패", e)  
        finally:
            self.__close()