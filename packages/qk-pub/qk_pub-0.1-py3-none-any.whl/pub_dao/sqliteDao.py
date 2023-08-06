from onoffline.entity.onofflineDO import OnoffLineRecodeDo, LogFileRecordDo
from pubUtils import dateUtil
from pubUtils.sqliteUtil import SqliteDb

sqliteClient: SqliteDb = None


# 数据化使用
def init_sqlite_db(client: SqliteDb):
    global sqliteClient
    sqliteClient = client


class OnoffLineRecordDao:
    @staticmethod
    def addOnoffLineRecordTable():
        sql = """
            create table if not exists onoff_line_record
            (
                id                integer
                    constraint id
                        primary key autoincrement,
                start_time        text not null,
                agv_code          text,
                event_type        TEXT,
                session_id        text,
                cached_session_id text,
                point_code        text,
                create_time       text,
                update_time       text,
                unique   (start_time, agv_code)
            );    
        """
        sqliteClient.create_new_table(sql)

    @staticmethod
    def save(record: OnoffLineRecodeDo):
        try:
            data = record.to_array()
            curr_date = dateUtil.currData()
            data.append(curr_date)
            data.append(curr_date)
            sql = "insert  or ignore into onoff_line_record('start_time','agv_code','event_type','session_id','cached_session_id','point_code','create_time','update_time') values (?,?,?,?,?,?,?,?)"
            sqliteClient.insert(sql=sql, data=data)
            return True
        except:
            return False

    @staticmethod
    def truncate():
        sql = "delete from onoff_line_record "
        sqliteClient.executescript(sql)


class LogFileDao:
    @staticmethod
    def addLogFileTable():
        if LogFileDao.tableExist():
            return
        sql = """
            create table if not exists log_file_record
            (
                id                integer
                    constraint id
                        primary key autoincrement,
                file_path        text not null ,
                content        text,
                create_time       text,
                update_time       text,
                unique (file_path)
            );    
        """
        sqliteClient.create_new_table(sql)

    @staticmethod
    def tableExist():
        sql = "select name from sqlite_master where name = 'log_file_record'"
        return sqliteClient.sql_select_one(sql)

    @staticmethod
    def insert(record: LogFileRecordDo):
        try:
            data = record.to_array()
            sql = "insert  or ignore into log_file_record('file_path','content','create_time','update_time') values (?,?,?,?)"
            sqliteClient.insert(sql=sql, data=data)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def batchInsert(records: list):
        try:
            datas = [record.to_array() for record in records]
            sql = "insert  or ignore into log_file_record('file_path','content','create_time','update_time') values (?,?,?,?)"
            sqliteClient.batchInsert(sql=sql, datas=datas)
            return True
        except:
            return False

    @staticmethod
    def queryByfilePath(file_path):
        sql = "select * from log_file_record where file_path = '{}'".format(file_path)
        return sqliteClient.sql_select_many(sql=sql)

    @staticmethod
    def allFilePaths():
        sql = "select file_path from log_file_record"
        return sqliteClient.sql_select_many(sql=sql)

    @staticmethod
    def exist(file_path):
        sql = "select * from log_file_record where file_path = '{}' limit 1".format(file_path)
        return sqliteClient.sql_select_one(sql=sql)

    @staticmethod
    def deleteByFilePath(file_path):
        sql = "delete from log_file_record where file_path ='{}'".format(file_path)
        sqliteClient.executescript(sql)
