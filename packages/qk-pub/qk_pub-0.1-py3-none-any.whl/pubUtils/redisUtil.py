import redis


class RedisClient:
    pool = None

    def __init__(self, ip, port=6379, db=1):
        self.ip = ip
        self.port = port
        self.db = db
        self.pool = self.init_pool(ip, port, db)

    def init_pool(self, serviceIp, port=6379, db=1):
        if not self.pool:
            self.pool = redis.ConnectionPool(host=serviceIp, port=port, db=db, decode_responses=True)
        print("redis：{}已初始化".format(serviceIp))
        return self.pool

    def client(self):
        return redis.Redis(connection_pool=self.pool)
