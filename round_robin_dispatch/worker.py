# -*- coding:utf-8 -*-

"""
    RabbitMQ 消费者
"""

import time
import json
import pika
import random

credentials = pika.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='169.254.207.36', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)  # durable为True，消息队列持久化
print("Waiting for message. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print("Received %s" % json.loads(body.decode()))
    # 模拟数据处理过程
    # time.sleep(round(random.uniform(2, 3), 2))  # worker实力相当
    time.sleep(round(random.uniform(1, 8), 2))  # worker实力差别大
    print("Done")
    # 手动对消息进行确认
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume("task_queue", callback)
channel.start_consuming()
