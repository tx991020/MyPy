

import MySQLdb
# MySQL 建立连接
class MySQLPipeline(object):

    def __init__(self, host, port, user, password, db):
        self.mysql_host = host
        self.mysql_port = port
        self.mysql_user = user
        self.mysql_password = password
        self.mysql_db = db

        # 创建MYSQL数据库链接对象
        self.conn = MySQLdb.connect(host=self.mysql_host,
                                    user=self.mysql_user,
                                    password=self.mysql_password,
                                    db=self.mysql_db,
                                    charset="utf8")

    # 查询数据
    def searching(self, sql):
        try:
            with self.conn as cur:
                cur.execute(sql)
                logger.info("sql查询成功")

                return cur

    except Exception as e:
        print(e)
        logger.error(e)
        return None


# 增删改
def processing(self, sql):
    try:
        with self.conn as cur:
            cur.execute(sql)
            logger.info("sql处理成功")
    except Exception as e:
        print(e)
        logger.error(e)
        return None


if __name__ == '__main__':


    # def get_results():
    #     result = a.searching(query_sql)
    #
    #     if result:
    #         row = [row for row in result]
    #         word, id = row[0][0], row[0][1]
    #         return word, id
    #     else:
    #         print("查询为空")
