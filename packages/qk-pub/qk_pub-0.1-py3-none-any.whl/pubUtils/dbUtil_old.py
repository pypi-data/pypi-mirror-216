import time

import pymysql
from dbutils.pooled_db import PooledDB
import threading

dbLock = threading.Lock()


def init_inventoryConn(service_ip, db_user="root", db_pwd="root123", db_port="3306"):
    try:
        dbConfig = {
            "host": service_ip,
            "user": db_user,
            "password": db_pwd,
            "db": "evo_wes_inventory",
            "port": int(db_port),
            "charset": "utf8",
            "connect_timeout": 3,
            "autocommit": True
        }
        return ConnMysql(dbConfig)
    except Exception as e:
        print("evo_wes_inventory初始化失败:{}".format(e))
        return None


def init_basicConn(service_ip, db_user="root", db_pwd="root123", db_port="3306"):
    try:
        dbConfig = {
            "host": service_ip,
            "user": db_user,
            "password": db_pwd,
            "db": "evo_basic",
            "port": int(db_port),
            "charset": "utf8",
            "connect_timeout": 3,
            "autocommit": True
        }
        return ConnMysql(dbConfig)
    except Exception as e:
        print("evo_basic初始化失败:{}".format(e))
        return None


def init_rcsConn(service_ip, db_user="root", db_pwd="root123", db_port="3306"):
    try:
        dbConfig = {
            "host": service_ip,
            "user": db_user,
            "password": db_pwd,
            "db": "evo_rcs",
            "port": int(db_port),
            "charset": "utf8",
            "connect_timeout": 3,
            "autocommit": True
        }
        return ConnMysql(dbConfig)
    except Exception as e:
        print("evo_rcs初始化失败:{}".format(e))
        return None


def init_wcsConn(service_ip, db_user="root", db_pwd="root123", db_port="3306"):
    try:
        dbConfig = {
            "host": service_ip,
            "user": db_user,
            "password": db_pwd,
            "db": "evo_wcs_g2p",
            "port": int(db_port),
            "charset": "utf8",
            "connect_timeout": 3,
            "autocommit": True
        }
        return ConnMysql(dbConfig)
    except Exception as e:
        print("evo_wcs_g2p初始化失败:{}".format(e))
        return None


class ConnMysql(object):
    __pool = None

    def __init__(self, dbConfig):
        # 构造函数，创建数据库连接、游标
        self.coon = ConnMysql.getmysqlconn(self, dbConfig)
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    def getmysqlconn(self, dbConfig):
        global __pool
        if ConnMysql.__pool is None:
            __pool = PooledDB(
                creator=pymysql,
                mincached=6,
                maxcached=10,
                maxconnections=10,
                maxshared=10,
                blocking=True,
                maxusage=None,
                setsession=[],
                ping=0,
                host=dbConfig['host'],
                user=dbConfig['user'],
                passwd=dbConfig['password'],
                db=dbConfig['db'],
                port=dbConfig['port'],
                charset=dbConfig['charset'],
                connect_timeout=dbConfig["connect_timeout"],
                autocommit=True
            )
        return __pool.connection()

    def getConn(self):
        self.coon = self.__pool.connection()
        self.cur = self.conn.cursor()

    def dispose(self):
        self.cur.close()
        self.coon.close()

    # 插入、修改、删除一条
    def sql_change_msg(self, sql):
        try:
            # self.getConn()
            # self.coon.ping()
            dbLock.acquire()
            change_sql = self.cur.execute(sql)
            self.coon.commit()
            dbLock.release()
            # time.sleep(1)
            return change_sql
        except Exception as e:
            # self.dispose()
            print("执行sql异常：{} e:{}".format(sql, e))
            return

    def sql_select_one(self, sql):
        self.cur.execute(sql)
        select_res = self.cur.fetchone()
        return select_res

    # 查询多条
    def sql_select_many(self, sql, count=None):
        try:
            # self.getConn()
            # self.coon.ping()
            dbLock.acquire()
            self.cur.execute(sql)
            self.coon.commit()
            dbLock.release()
            if count is None:
                select_res = self.cur.fetchall()
                # time.sleep(1)
            else:
                select_res = self.cur.fetchmany(count)
            return select_res
        except Exception as e:
            print("执行sql异常：{} e:{}".format(sql, e))
            # self.dispose()
            return None
