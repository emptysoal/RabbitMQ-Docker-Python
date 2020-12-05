# -*- coding:utf-8 -*-

"""
    RabbitMQ 生产者
"""

import pika
import json

credentials = pika.PlainCredentials(username='admin', password='admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='169.254.207.36', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)  # durable为True，消息队列持久化

for i in range(10):
    message = json.dumps({"OrderID": "1000%s" % i, "Content": "Hello"})
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # 消息持久化
    )
    print("Send %r" % message)

connection.close()
