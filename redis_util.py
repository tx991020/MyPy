import redis


class RedisPipline():

    def __init__(self):
        self.pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_password, db=redis_db)
        self.redis_conn = redis.Redis(connection_pool=self.pool)

    # set
    def set_data(self, key, data):
        self.redis_conn.set(key, data)

    # get
    def get_data(self, key):
        return self.redis_conn.get(key)

    # rpush
    def rpush_data(self, key, data):
        self.redis_conn.rpush(key, json.dumps(data))

    # lpop
    def lpop_data(self, key):
        self.redis_conn.lpop(key)

    # 删除key
    def delete_key(self, key):
        if self.redis_conn.exists(key):
            self.redis_conn.delete(key)
