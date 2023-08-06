dbConn = None


def init_wcs_db(dbAdaptor):
    global dbConn
    dbConn = dbAdaptor.wcs_db_cli


def queryBySql(sql):
    if not sql:
        print("sql不能为空：{}".format(sql))
        return
    try:
        return dbConn.sql_select_many(sql)
    except Exception as e:
        print("sql异常：{}".format(e))
        return
