import threading
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import ast
from time import sleep
from .executer import ExecuterCaller
        
class MessageReciever:

    def __init__(self, group_id: str, executers_by_topic: dict, event: threading.Event) -> None:

        self.event = event
        self.consumer = None
        try:
            self.consumer = KafkaConsumer(
                                bootstrap_servers=['localhost:9092'],
                                auto_offset_reset='earliest',
                                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                group_id=group_id,
                            )
        except NoBrokersAvailable as e:
            print('Kafka NoBrokersAvailable!!')
            return
        
        self.topics = list(map(lambda x: x[0], executers_by_topic.items()))
        self.executers = executers_by_topic
        self.consumer.subscribe(self.topics)
        self._start_polling()

    def restart(self):
        if self.consumer:
            self.consumer.close()

    def get_thread(self):
        return self.thread
    
    def _polling(self):

        while True:

            if self.event.is_set():
                print('[MessageReciever is broken]')
                break

            try:
                results = self.consumer.poll(10.0)
            except Exception as e:
                sleep(10)
                continue

            if not results:
                sleep(5)
            
            for topic_partition, messages in results.items():
                for message in messages:
                    result_dict = self.parse_message(topic_partition.topic, message.value)

                    from . import app, zipkin
                    with app.app_context():

                        if zipkin:

                            header = result_dict['header']
                            trace_id = header.get('trace_id')
                            parent_span_id = header.get('span_id')

                            zipkin.create_span('Kafka_consumer.topic='+ topic_partition.topic,
                                               trace_id = trace_id,
                                               parent_span_id = parent_span_id,
                                               )
                            zipkin.update_tags(param=message.value)

                        rtn, comment = ExecuterCaller.instance().execute_command(result_dict)

                        if zipkin:
                            zipkin.update_tags(
                                param  = message.value,
                                result = comment,
                                )

    def _start_polling(self):

        self.thread = threading.Thread(target=self._polling)
        self.thread.name = '_kafka_consumer'
        self.thread.start()

    def parse_message(self, topic: str, message: dict):
        
        header = message.pop('header') if message.get('header') else {}

        result_dict =\
            dict(
                executer = self.executers[topic],
                initial_param = message,
                header = header
            )
        
        return result_dict
    
    def __del__(self):
        #if self.consumer:
        #    self.consumer.close()
        try:
            self.consumer.close()
        except Exception as e:
            pass