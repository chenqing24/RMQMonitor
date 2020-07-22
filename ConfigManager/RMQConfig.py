#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import os
from CommonUtil import switch

class ConfigDifinationException(Exception):
    pass

class Property():
    def __init__(self,key,value=None):
        self.__key = key
        self.__value = value

    @property
    def Key(self):
        return self.__key
    @Key.setter
    def Key(self,key):
        self.__key = key

    @property
    def Value(self):
        return self.__value
    @Value.setter
    def Value(self,value):
        self.__value=value


class ConfigSection():
    def __init__(self,cfgpath):
        self._host = Property(key='host')
        self._port = Property('port')
        self._username=Property('user_name')
        self._password=Property('password')
        self._virtualhost =Property('virtual_host')
        self._queue=Property('queue')
        self._notifytype=Property('notifytype')
        self._sendfrequency=Property('send_frequency')
        self._latency=Property('latency')
        self._comsumeralarmwait=Property('comsumeralarmwait')
        self._notify=Property('smsnotify')
        #self._notify=Property('mailnotify')
        self._name = ''
        self._cf = ConfigParser.ConfigParser()
        #检查配置文件是否存在
        if not (os.path.exists(cfgpath)):
            raise ConfigDifinationException("找不到配置文件")
        #读取配置文件，读取失败抛出异常
        try:
            self._cf.read(cfgpath)
        except Exception,e:
            raise e


    @property
    def Name(self):
        return self._name

    def getSectionProperties(self,sectionname):
        self._name = sectionname
        self._host.Value = self._cf.get(sectionname,self._host.Key)
        self._port.Value = self._cf.get(sectionname,self._port.Key)
        self._username.Value = self._cf.get(sectionname,self._username.Key)
        self._password.Value = self._cf.get(sectionname,self._password.Key)
        self._virtualhost.Value = self._cf.get(sectionname,self._virtualhost.Key)
        self._queue.Value = self._cf.get(sectionname,self._queue.Key)
        self._notifytype.Value = self._cf.get(sectionname,self._notifytype.Key)

        for case in switch(self.NotifyType):
            if case('sms'):
                self._notify = Property('smsnotify')
                break
            if case('mail'):
                self._notify= Property('mailnotify')
                break
        self._notify.Value = self._cf.get('COMMON',self._notify.Key)
        self._sendfrequency.Value = self._cf.get('COMMON',self._sendfrequency.Key)
        self._latency.Value = self._cf.get('COMMON',self._latency.Key)
        self._comsumeralarmwait.Value = self._cf.get('COMMON',self._comsumeralarmwait.Key)
        #self.PrintProperties()


    def PrintProperties(self):
        print '----------'+self._name+'-----------'
        print self._host.Key+' = '+ self._host.Value
        print self._port.Key+' = '+ self._port.Value
        print self._username.Key+' = '+ self._username.Value
        print self._password.Key+' = '+ self._password.Value
        print self._virtualhost.Key+' = '+ self._virtualhost.Value
        print self._notifytype.Key+' = '+ self._notifytype.Value
        print self._notify.Key+' = '+ self._notify.Value



    @property
    def Host(self):
        return self._host.Value

    @property
    def Port(self):
        return self._port.Value

    @property
    def UserName(self):
        return self._username.Value

    @property
    def Password(self):
        return self._password.Value

    @property
    def VirtualHost(self):
        return self._virtualhost.Value

    @property
    def Queue(self):
        return self._queue.Value

    @property
    def NotifyType(self):
        return self._notifytype.Value

    @property
    def Notify(self):
        return self._notify.Value

    @property
    def SendFrequency(self):
        return self._sendfrequency.Value

    @property
    def Latency(self):
        return self._latency.Value

    @property
    def ComsumerAlarmWait(self):
        return self._comsumeralarmwait.Value
