import sqlite3
import threading


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteDb:
    def __init__(self):
        self.initSqliteDb()
        self.lock = threading.RLock()


    def initSqliteDb(self):
        conn = sqlite3.connect(database="D:/universal_tool.db", check_same_thread=False)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur

    def batchInsert(self, sql, datas):
        try:
            self.lock.acquire()
            # self.initSqliteDb()
            self.cur.executemany(sql, datas)
            self.conn.commit()
            # self.closeConn()
            self.lock.release()
        except Exception as e:
            print("{}执行异常param:{} e:{}".format(sql, datas, e))
            # self.conn.rollback()
            # self.closeConn()
            self.lock.release()

    def insert(self, sql, data):
        try:
            self.lock.acquire()
            # self.initSqliteDb()
            self.cur.execute(sql, data)
            self.conn.commit()
            # self.closeConn()
            self.lock.release()
        except Exception as e:
            print("{}执行异常param:{} e:{}".format(sql, data, e))
            # self.conn.rollback()
            # self.closeConn()
            self.lock.release()

    def sql_select_many(self, sql):
        try:
            # self.lock.acquire()
            # self.initSqliteDb()
            self.cur.execute(sql)
            res = self.cur.fetchall()
            # self.closeConn()
            # self.lock.release()
            return res
        except Exception as e:
            print("{}执行异常 e:{}".format(sql, e))
            # self.closeConn()
            # self.lock.release()
    def sql_select_one(self, sql):
        try:
            # self.lock.acquire()
            # self.initSqliteDb()
            self.cur.execute(sql)
            res = self.cur.fetchone()
            # self.closeConn()
            # self.lock.release()
            return res
        except Exception as e:
            # self.closeConn()
            print("{}执行异常 e:{}".format(sql, e))
            # self.lock.release()

    def tableisExist(self):
        try:
            self.lock.acquire()
            # self.initSqliteDb()
            sql = """
            SELECT count(*) num FROM sqlite_master WHERE type='table' AND name in ('grid','grid_detail','container_slot_relation');
            """
            self.cur.execute(sql)
            res = self.cur.fetchone()
            # self.closeConn()
            self.lock.release()
            return res
        except Exception as e:
            print("sql执行异常 e:{}".format(e))
            # self.closeConn()
            self.lock.release()

    def create_new_table(self, sql):
        if not sql:
            print("创建表失败 sql为空")
        try:
            self.lock.acquire()
            # self.initSqliteDb()
            self.cur.executescript(sql)
            self.conn.commit()
            # self.closeConn()
            self.lock.release()
        except Exception as e:
            # self.conn.rollback()
            # self.closeConn()
            print("{}执行异常 e:{}".format(sql, e))
            self.lock.release()

    def initTables(self):
        create__table_sql = """
                create  table grid(container_code TEXT , grid_code TEXT,good_code TEXT,manage_type NUMBER,product_num NUMBER,state NUMBER,create_time TEXT,update_time TEXT );
                create  table grid_detail(container_code TEXT , grid_code TEXT,good_code TEXT,product_code TEXT,create_time TEXT,update_time TEXT );
                create  table container_slot_relation(container_code TEXT ,bucket_id TEXT,slot_code TEXT,state NUMBER,create_time TEXT,update_time TEXT);
                create  table wh_order(order_no TEXT,container_code TEXT,param_detail TEXT,create_time TEXT);
                create table c_cache_slot_scan(id integer constraint c_cache_slot_scan_pk primary key autoincrement,bucket_code int not null,state int,create_time text,update_time text);
                create table c_cache_slot_scan_item
                    (
                        id                 integer
                            constraint c_cache_slot_scan_item_pk
                                primary key autoincrement,
                        bucket_code        TEXT    not null,
                        source_slot_code   TEXT    not null,
                        source_slot_point  TEXT    not null,
                        source_slot_height INTEGER not null,
                        target_slot_code   TEXT    not null,
                        target_slot_point  TEXT    not null,
                        target_slot_height integer not null,
                        state              int     not null,
                        "index"            integer not null,
                        create_time        text,
                        update_time        text,
                        agv_code           text    not null,
                        job_id             TEXT    not null,
                        container_code     TEXT    not null
                    );
                -- 货位/料箱码盘点报表导出
                CREATE TABLE slot_container_code_scan_excel (
                    id INTEGER CONSTRAINT slot_container_code_scan_excel_pk PRIMARY KEY autoincrement,
                    job_id text,
                    warehouse_id text,
                    zone_code text,
                    area_code text,
                    slot_code text,
                    decoded_slot_code text,
                    slot_decode_res text,
                    exist_container text,
                    container_code INT,
                    decoded_container_code text,
                    container_code_res INT,
                    create_time text
                );
                -- 货位/料箱码盘点任务生成
                CREATE TABLE slot_container_code_scan_job (
                    id INTEGER CONSTRAINT slot_container_code_scan_job_pk PRIMARY KEY autoincrement,
                    zone_code text,
                    area_code text,
                    sequence INT,
                    job_id text,
                    job_param text,
                    state INT DEFAULT 0,
                    parse_res int DEFAULT 0 ,
                    create_time text,
                    update_time text
                );




                
        """
        if self.tableisExist().get("num", 0) == 0:
            try:
                # self.lock.acquire()
                # self.initSqliteDb()
                self.cur.executescript(create__table_sql)
                self.conn.commit()
                # self.closeConn()
                # self.lock.release()
            except Exception as e:
                # self.conn.rollback()
                # self.closeConn()
                print("{}执行异常 e:{}".format(create__table_sql, e))
                # self.lock.release()
            print("初次加载 完成表创建")
        else:
            print("表已存在不需要初始化")


    def executescript(self, sql):
        try:
            self.lock.acquire()
            # self.initSqliteDb()
            self.cur.executescript(sql)
            self.conn.commit()
            # self.closeConn()
            self.lock.release()
        except Exception as e:
            # self.conn.rollback()
            # self.closeConn()
            print("{}执行异常 e:{}".format(sql, e))
            self.lock.release()

    def closeConn(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    db = SqliteDb()
    res = db.sql_select_many(sql="select * from grid")
    print(res)
