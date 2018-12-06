from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json

class Kafka_consumer():
    '''
    使用Kafka—python的消费模块
    '''

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid,
                                      bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
                                              kafka_host=self.kafkaHost,
                                              kafka_port=self.kafkaPort))

    def consume_data(self):
        try:
            for message in self.consumer:
                # print json.loads(message.value)
                yield message
        except KeyboardInterrupt as e:
            print(e)

def Comsume():
    '''
    测试consumer和producer
    :return:
    '''
    consumer = Kafka_consumer('127.0.0.1', 9092, "zhang_test_3", 'test-python-zhang_test')
    message = consumer.consume_data()
    for i in message:

        print(i.value)
        print('partition=',i.partition)
        print('offset=',i.offset)





class Kafka_producer():
    '''
    使用kafka的生产模块
    '''

    def __init__(self, kafkahost,kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort
            ))


    def sendjsondata(self,params):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            future = producer.send(topic=self.kafkatopic, value=parmas_message.encode('utf-8'))
            record_metadata = future.get(timeout=10)
            producer.flush()

            print('topic : {0}'.format(record_metadata.topic))
            print('partition : {0}'.format(record_metadata.partition))
            print('offset : {0}'.format(record_metadata.offset))
            print(parmas_message)


        except KafkaError as e:
            print(e)


def Produce():
    '''
    测试consumer和producer
    :return:
    '''
    ##测试生产模块
    producer = Kafka_producer("127.0.0.1", 9092, "zhang_test_3")
    for i in range(6):
       params = '{abetst}:---'+str(i)
       producer.sendjsondata(params)

if __name__ == '__main__':
    Produce()
    Comsume()