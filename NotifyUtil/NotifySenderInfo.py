#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
from ConfigManager import Property

class NotifySenderInfo():

    def __init__(self,configpath,sectionname='Production'):
        self.__cf = ConfigParser.ConfigParser()
        self.__cf.read(configpath)
        self.__section = sectionname

    def Load(self,notifytype='sms'):
        self.__host = Property(notifytype+'host')
        self.__port = Property(notifytype+'port')
        self.__url = Property(notifytype+'url')
        self.__account = Property(notifytype+'account')
        self.__password=Property(notifytype+'password')
        self.__host.Value = self.__cf.get(self.__section,self.__host.Key)
        self.__port.Value = self.__cf.get(self.__section,self.__port.Key)
        self.__url.Value = self.__cf.get(self.__section,self.__url.Key)
        self.__account.Value = self.__cf.get(self.__section,self.__account.Key)
        self.__password.Value = self.__cf.get(self.__section,self.__password.Key)

    def PrintProperties(self):
        print '---------- '+self.__section+' ----------'
        print self.Host
        print self.Port
        print self.Url
        print self.Account
        print self.Password

    @property
    def Host(self):
        return self.__host.Value

    @property
    def Port(self):
        return self.__port.Value

    @property
    def Url(self):
        return self.__url.Value

    @property
    def Account(self):
        return self.__account.Value

    @property
    def Password(self):
        return self.__password.Value
