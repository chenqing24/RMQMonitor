#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigManager import ConfigSection
from NotifyUtil import OpsAlerm,NotifySenderInfo
from RMQUtil import Connector
import os
import time
import threading
import thread
from InfluxDBClient import DBWriter

class RMQMonitor():

    def __init__(self,rmqname):
        configdir = os.path.split(os.path.realpath(__file__))[0]+'/config/'
        mqconfigfile = configdir+'RMQHeartBeat.cfg'
        notifyconfigfile = configdir+'notifyConfig.cfg'
        self._rmqc= ConfigSection(mqconfigfile)
        self._rmqc.getSectionProperties(rmqname)
        self._alerm = OpsAlerm(NotifySenderInfo(notifyconfigfile),self._rmqc._notifytype.Value)
        self._sendalarmcount = 0
        self._comsumeralarmcount=0
        self._comsumeralarmwait = self._rmqc.ComsumerAlarmWait
        self._comsumeralarmfirsttrigger = 0.00
        # influxdb投递地址
        self._influxdb = DBWriter(host='10.100.0.1',port=8086,username='test',password='influxdb123',database='mydb')

    def StartComsumer(self):
        print 'start consumer'
        ## 先打开消费监听
        connector = Connector(username=self._rmqc.UserName,
                            password=self._rmqc.Password,
                            host=self._rmqc.Host,
                            port=int(self._rmqc.Port),
                            virtual_host=self._rmqc.VirtualHost)
        connector.Consume(self.CallBack,queue=self._rmqc.Queue)

    def StartHeartBeat(self):
        print 'start heart beating'
        ###开始拨测

        connector = Connector(username=self._rmqc.UserName,
                            password=self._rmqc.Password,
                            host=self._rmqc.Host,
                            port=int(self._rmqc.Port),
                            virtual_host=self._rmqc.VirtualHost)
        while True:
            try:
                connector.Send(message=str(time.time()),queue=self._rmqc.Queue)
                if self._sendalarmcount > 0:
                    self._sendalarmcount = 0
            except Exception,e:
                self._sendalarmcount +=1
                if self._sendalarmcount <4:
                    message = '['+self._rmqc.Name+']:拨测报错,发送信息失败! 第'+str(self._sendalarmcount)+'次告警!'
                    self._alerm.Send(message=message,mobile=self._rmqc.Notify)

            threading._sleep(int(self._rmqc.SendFrequency))

    def CallBack(self,ch,mothod,properties,message):
        ### 记录消费消息时间,计算消费延迟时间
        recieve = time.time()
        reallatency=(recieve-float(message))*1000
        data = [
	    {
		    "measurement":"rabbitmq.comsumer.latency",
		    "fields" :{
			    "host":self._rmqc.Host,
			    "value":reallatency
		    }
	    }
	    ]
        self._influxdb.writ(data)

        duration = recieve-self._comsumeralarmfirsttrigger;
        #延迟告警触发后,告警三次, 然后静默一段时间后继续开启,
        if reallatency > float(self._rmqc.Latency):
            self._comsumeralarmcount +=1
            if self._comsumeralarmcount == 1:
                self._comsumeralarmfirsttrigger = time.time()
            if self._comsumeralarmcount < 4:
                if float(self._comsumeralarmwait) > (recieve-self._comsumeralarmfirsttrigger):
                    message = '['+self._rmqc.Name+']:信息消费延迟时间过大! 延迟 '+str(reallatency)+' 毫秒消费!第 '+str(self._comsumeralarmcount)+' 次告警!'
                    self._alerm.Send(message=message,mobile=self._rmqc.Notify)
            elif float(self._comsumeralarmwait) <= (recieve-self._comsumeralarmfirsttrigger):
                self._comsumeralarmcount = 0
                self._comsumeralarmfirsttrigger = time.time()

        #print '延迟:'+str(reallatency)
        #print '告警次数:'+ str(self._comsumeralarmcount)
        #print '持续时间:'+str(duration)

if __name__ == '__main__':

    ### inf Queue 监控
    m1 = RMQMonitor('CRM')
    ### 先启动comsumer, 自动在RMQ中建Q,等待2秒后启动心跳发送
    thread.start_new_thread(m1.StartComsumer,())
    threading._sleep(2)
    thread.start_new_thread(m1.StartHeartBeat,())
    while True:
        continue
