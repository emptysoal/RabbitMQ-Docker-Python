# -*- coding:utf-8 -*-

"""
    RabbitMQ 消费者
"""
import pika

credientials = pika.PlainCredentials(username='admin', password='admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='169.254.207.36', port=5672, virtual_host='/', credentials=credientials))
channel = connection.channel()
# 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
channel.queue_declare(queue='python-test', durable=False)


# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(body.decode())


# 告诉rabbitmq，用callback来接收消息
channel.basic_consume('python-test', callback)
# 开始接收消息，并进入阻塞状态，队列里有消息才会调用callback进行处理
channel.start_consuming()
