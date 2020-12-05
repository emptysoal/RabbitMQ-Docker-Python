# Python 调用 RabbitMQ 入门简介

## 项目介绍

共有 3 个项目，包含了如何构建环境，以及 python 如何调用 RabbitMQ，区别如下：

- example: 单一生产者对单一消费者；

- round_robin_dispatch: 一个生产者对多个消费者，循环分发模式；
- fair_dispatch: 一个生产者对多个消费者，公平分发模式

其中循环分发和公平分发在代码上的区别只有一行，在消费者的代码中，调用回调函数前多加如下代码：

```python
channel.basic_qos(prefetch_count=1)
```

