# 使用示例 - Docker+RabbitMQ+Python

## 环境构建

### RabbitMQ环境（rabbitMQ server端）

- 构建

```bash
$ docker pull rabbitmq:management
```

- 启动RabbitMQ

```bash
$ docker run -d --name rabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 15672:15672 -p 5672:5672 rabbitmq:management
```

**备注** : 15672是管理界面的端口，5672是服务的端口。这里顺便将管理系统的用户名和密码设置为admin admin 默认账号和密码是guest guest。

- Web管理界面

1. 打开浏览器输入 http://<本机IP>:15672；

2. 账号密码均输入 admin（启动时所设置的）

### python环境（rabbitMQ client端）

由于笔者本机 python 没有 ssl 认证，连接rabbitMQ会报错，所以使用的 docker 镜像中的 python 环境（这样就跳过了ssl认证，笔者真是个天才）

- 构建

找到一个包含python的docker环境，笔者的为 `general-python3.6:with-vim-v1`

```bash
$ docker run -it -v $PWD:/workspace general-python3.6:with-vim-v1 bash
# pip install pika -i https://pypi.tuna.tsinghua.edu.cn/simple
```

后续代码放到 $PWD(自己指定的路径) 下，并使用 docker 中的 python 环境执行。

## python客户端代码

### 生产者

- producer.py

```python
# -*- coding:utf-8 -*-

"""
    RabbitMQ 生产者
"""
import pika
import json

credentials = pika.PlainCredentials(username='admin', password='admin')  # mq用户名和密码
# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='169.254.207.36', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()
# 声明消息队列，消息将在这个队列传递，如不存在，则创建
result = channel.queue_declare(queue='python-test')

for i in range(10):
    message = json.dumps({'OrderID': '1000%s' % i})
    # 向队列插入数值 routing_key 是队列名
    channel.basic_publish(exchange='', routing_key='python-test', body=message)
    print(message)
connection.close()

```

### 消费者

- consumer.py

```python
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

```

## 监控

- RabbitMQ Web管理界面中 Overview 下即可看到消息的状态变化。

## 参考链接

`https://www.cnblogs.com/caijunchao/p/13864673.html`

