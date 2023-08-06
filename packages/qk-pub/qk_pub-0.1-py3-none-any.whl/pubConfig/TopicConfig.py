import enum


class TopicEnum(enum.Enum):
    INIT_DB = "init_db", "mysql数据库初h化完成"
    INIT_SQLITE_DB = "init_db", "sqlite数据库初h化完成"
    FILE_UPLOADED = "file_uploaded", "文件上传完成"


if __name__ == '__main__':
    print(TopicEnum.INIT_DB.name, type(TopicEnum.INIT_DB.name))
