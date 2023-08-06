dbConn = None


def init_basic_db(dbAdaptor):
    global dbConn
    dbConn = dbAdaptor.basic_db_cli


def queryBySql(sql):
    if not sql:
        print("sql不能为空：{}".format(sql))
        return
    try:
        return dbConn.sql_select_many(sql)
    except Exception as e:
        print("sql异常：{}".format(e))
        return


def queryOneBySql(sql):
    if not sql:
        print("sql不能为空：{}".format(sql))
        return
    try:
        return dbConn.sql_select_one(sql)
    except Exception as e:
        print("sql异常：{}".format(e))
        return


# 查询所有容器信息
def queryAllContainerInfos():
    global dbConn
    sql = "SELECT container_code,digital_code,slot_code,bucket_id from basic_container ;"
    return queryBySql(sql)


# 查询货架最大层数
def queryMaxFloorOfBucket():
    sql = """
        SELECT MAX(cast(SUBSTRING_INDEX(SUBSTRING_INDEX(slot_code,"-",-2),"-",1)as signed)) max_floor from basic_slot;
    """
    return queryOneBySql(sql)


if __name__ == '__main__':
    # queryAllContainerInfos()
    res = queryMaxFloorOfBucket()
    print(res)
