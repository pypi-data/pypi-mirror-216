dbConn = None


def init_rcs_db(dbAdaptor):
    global dbConn
    dbConn = dbAdaptor.rcs_db_cli


def queryBySql(sql):
    if not sql:
        print("sql不能为空：{}".format(sql))
        return
    try:
        return dbConn.sql_select_many(sql)
    except Exception as e:
        print("sql异常：{}".format(e))
        return


# 查询AGV类型信息
def queryAgvTypeInfos():
    sql = "SELECT agv.agv_code,t.agv_type_code from basic_agv agv LEFT JOIN basic_agv_type t on agv.agv_type_id  = t.id;"
    return queryBySql(sql)
