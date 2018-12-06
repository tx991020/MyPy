import json
from bson.objectid import ObjectId
from pymongo import MongoClient




f=open('config.json','r',encoding='utf8')
json_config=json.load(f)

CONN_ADDR1 = json_config['mongo']["CONN_ADDR1"]
CONN_ADDR2 = json_config['mongo']["CONN_ADDR2"]
REPLICAT_SET = json_config['mongo']["REPLICAT_SET"]

username = json_config['mongo']["username"]
password = json_config['mongo']["password"]



class MongoCollecton:
    def __init__(self):
        # 设置mongodb连接
        self.client = MongoClient([CONN_ADDR1, CONN_ADDR2], replicaSet=REPLICAT_SET)
        self.client.admin.authenticate(username, password)
        self.db =self.client

    def get_messsage_and_id(self, message,project=None):
        #判断字段中有无 project 字段
        if '_id' in message.keys() and 'project' in message.keys():

            id_next = message['_id']
            message.pop('_id')
            if project != None:
                message["project"] = project
                return id_next, message,True
            else:
                return 0,message,False

    def mongo_collection(self):
        return self.db

    def mongo_query(self,id_min):
        print(id_min)
        if id_min == None:
            return {}
        else:
           return {'_id': {"$gt": ObjectId(id_min.decode())}}

    def mongo_move(self,dbname,collectionname,message):
        self.db[dbname][collectionname].save(message)

    def get_db_names(self):
        #返回数据库的列表
        dbnames=self.client.database_names()
        ret=[i for i in dbnames if  i not in ["admin","local"]]
        return ret

    def get_db_collections(self,dbname):
        #获得指定result 的collection
        return  self.client[dbname].collection_names()



if __name__ == '__main__':
    a = MongoCollecton()
    print(111,a.mongo_collection())