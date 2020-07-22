#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika

class Connector:
    def __init__(self,
                 username,
                 password,
                 host,
                 port,
                 virtual_host
                 ):
        """ RMQ 连接器.

        :param str username:用户名
        :param str password:密码
        :param host: 服务器地址
        :param port: 服务器端口
        :param virtual_host: 虚拟主机

        """
        parameters = pika.ConnectionParameters(host=host,
                                               port=port,
                                               virtual_host=virtual_host,
                                               credentials=pika.PlainCredentials(username=username,password=password))
        self.connection = pika.BlockingConnection(parameters)
        self.sendchannel = self.connection.channel()
        self.consumechannel = self.connection.channel()


    def Send(self,message=None,queue=None):
        self.sendchannel.queue_declare(queue=queue)
        self.sendchannel.basic_publish(exchange='',routing_key=queue,body=message)

    def Close(self):
        self.connection.close()

    def Consume(self,consumer_callback,queue=None):
        self.consumechannel.basic_consume(consumer_callback,queue=queue,no_ack=True)
        self.consumechannel.start_consuming()